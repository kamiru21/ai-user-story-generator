import os
import requests
import streamlit as st

st.title("📝 AI User Story Generator (Hugging Face)")

st.write("Paste a raw requirement below and get a clear Agile user story.")

raw_input = st.text_area("Raw requirement:", placeholder="e.g. Notify users of updates")

hf_token = st.secrets.get("HF_TOKEN") or os.getenv("HF_TOKEN")


def _error_detail(response):
    try:
        parsed = response.json()
        if isinstance(parsed, dict) and parsed.get("error"):
            return f" ({parsed['error']})"
    except ValueError:
        pass

    text = response.text.strip()
    return f" ({text})" if text else ""


def generate_user_story(prompt, token):
    if not token:
        return "🔒 Missing Hugging Face token. Add HF_TOKEN to .streamlit/secrets.toml."

    api_url = "https://api-inference.huggingface.co/models/mbien/ai-user-story-generator"
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "inputs": f"{prompt}",
        "parameters": {"temperature": 0.7}
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
    except requests.RequestException as exc:
        return f"❌ API call failed: {exc}"

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]['generated_text']
        else:
            return "⚠️ No output received."
    elif response.status_code == 503:
        return "⏳ Model is loading — please wait 30 seconds and try again."
    elif response.status_code == 401:
        return "🔒 Invalid Hugging Face token. Check your secrets."
    elif response.status_code == 410:
        return f"📴 Model endpoint unavailable (410 Gone){_error_detail(response)}"
    else:
        return f"❌ API call failed: {response.status_code}{_error_detail(response)}"


if not hf_token:
    st.info(
        "Add HF_TOKEN to .streamlit/secrets.toml (see README.md) or set an HF_TOKEN "
        "environment variable before calling the API."
    )
elif raw_input:
    with st.spinner("Contacting the model..."):
        story = generate_user_story(raw_input, hf_token)
    st.subheader("✅ Rewritten User Story")
    st.markdown(f"> {story}")
