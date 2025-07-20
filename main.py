import streamlit as st
import openai
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📝 AI User Story Generator")

st.write("Paste a raw requirement below and get a clean Agile user story.")

# Input box
raw_input = st.text_area("Raw requirement:", placeholder="e.g. Notify users of updates")

# Load OpenAI key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_user_story(requirement):
    prompt = f"Convert this into an Agile user story:\n\n'{requirement}'\n\nUse the format: As a [user], I want to [do something], so that [benefit]."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

    
    return response.choices[0].message['content'].strip()

if raw_input:
    story = generate_user_story(raw_input)
    st.subheader("✅ Rewritten User Story")
    st.markdown(f"> {story}")
