import streamlit as st
import requests

st.title("📝 AI User Story Generator (HuggingFace)")

st.write("Paste a raw requirement below and get a clear Agile user story.")

raw_input = st.text_area("Raw requirement:", placeholder="e.g. Notify users of updates")

def generate_user_story(prompt):
    api_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    
    payload = {
        "inputs": f"Convert this to a user story: {prompt}"
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0]['generated_text']
    else:
        return "⚠️ Error: API call failed."

if raw_input:
    story = generate_user_story(raw_input)
    st.subheader("✅ Rewritten User Story")
    st.markdown(f"> {story}")
