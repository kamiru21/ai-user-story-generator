import streamlit as st
import openai

st.title("📝 AI User Story Generator")

st.write("Paste a raw requirement below and get a clean Agile user story.")

# Input box
raw_input = st.text_area("Raw requirement:", placeholder="e.g. Notify users of updates")

# Load OpenAI key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_user_story(requirement):
    prompt = f"Convert this into an Agile user story:\n\n'{requirement}'\n\nUse the format: As a [user], I want to [do something], so that [benefit]."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )
    
    return response.choices[0].message['content'].strip()

if raw_input:
    story = generate_user_story(raw_input)
    st.subheader("✅ Rewritten User Story")
    st.markdown(f"> {story}")
