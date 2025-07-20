import streamlit as st
import requests

st.title("📝 AI User Story Generator (Hugging Face)")

st.write("Paste a raw requirement below and get a clear Agile user story.")

raw_input = st.text_area("Raw requirement:", placeholder="e.g. Notify users of updates")

def generate_user_story(prompt):
    api_url = "https://api-inference.huggingface.co/models/mbien/ai-user-story-generator"
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    
    payload = {
        "inputs": f"{prompt}",
        "parameters": {"temperature": 0.7}
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]['generated_text']
        else:
            return "⚠️ No output received."
    elif response.status_code == 503:
        return """⏳ Model is loading — please wait 30 seconds and try again."""

