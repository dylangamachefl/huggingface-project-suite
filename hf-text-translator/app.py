import streamlit as st
import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()


API_TOKEN = os.getenv("HF_TOKEN")
API_URL_BASE = "https://api-inference.huggingface.co/models/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

TRANSLATION_MODELS = {
    "English to Spanish": "Helsinki-NLP/opus-mt-en-es",
    "English to French": "Helsinki-NLP/opus-mt-en-fr",
    "English to German": "Helsinki-NLP/opus-mt-en-de",
    "English to Chinese (Simplified)": "Helsinki-NLP/opus-mt-en-zh",
    "English to Japanese": "Helsinki-NLP/opus-mt-en-jap",
    "Spanish to English": "Helsinki-NLP/opus-mt-es-en",
    "French to English": "Helsinki-NLP/opus-mt-fr-en",
}


def query_translation(text_to_translate, model_id):
    """
    Sends a request to the Hugging Face Inference API for translation.
    """
    if not API_TOKEN:
        st.error(
            "Hugging Face API Token not found. Please configure it in your .env file or Space secrets."
        )
        return None

    api_url = API_URL_BASE + model_id
    payload = {"inputs": text_to_translate}

    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        st.error(f"Translation API HTTP Error: {errh}")
        error_details = "No additional details from API."
        try:
            error_details = response.json().get("error", response.text)
        except ValueError:
            error_details = response.text
        st.info(f"Details: {error_details}")
        return None
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Translation API Connection Error: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        st.error(f"Translation API Timeout Error: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        st.error(f"Translation API Request Error: {err}")
        return None
    except ValueError:
        st.error("Error: Received non-JSON response from translation API.")
        st.info(
            f"Raw Response: {response.text if 'response' in locals() else 'No response object'}"
        )
        return None


# --- Streamlit UI ---
st.set_page_config(page_title="🌍 Text Translator", layout="wide")

st.title("🌍 Text Translation Tool")
st.markdown(
    "Translate text into various languages using Hugging Face's Inference API. "
    "This app demonstrates API integration for NLP tasks."
)

if not API_TOKEN:
    st.error("Hugging Face API Token not configured. The application cannot function.")
    st.markdown(
        "Please ensure your `HUGGING_FACE_API_TOKEN` is set in a `.env` file "
        "in the root of your `ai-portfolio` project or as a secret if deploying on Hugging Face Spaces."
    )
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area(
        "Enter text to translate:",
        height=200,
        key="text_input_translate",
        placeholder="Type or paste your text here...",
    )

with col2:
    selected_language_name = st.selectbox(
        "Select target language:",
        options=list(TRANSLATION_MODELS.keys()),
        index=0,  # Default to the first language in the list
        key="lang_select",
    )
    model_id_to_use = TRANSLATION_MODELS[selected_language_name]
    st.caption(f"Using model: `{model_id_to_use}`")


if st.button("Translate Text", key="translate_button", type="primary"):
    if text_input:
        if not API_TOKEN:
            st.error("API Token is missing. Cannot proceed.")
        else:
            with st.spinner(f"Translating to {selected_language_name}... Please wait."):
                translation_result = query_translation(text_input, model_id_to_use)

            if translation_result:
                if (
                    isinstance(translation_result, list)
                    and len(translation_result) > 0
                    and "translation_text" in translation_result[0]
                ):
                    translated_text = translation_result[0]["translation_text"]
                    st.subheader("📜 Translation:")
                    st.success(translated_text)
                elif isinstance(translation_result, dict) and translation_result.get(
                    "error"
                ):
                    st.warning("Translation failed. See error message above.")
                else:
                    st.error(
                        "Translation failed or the API returned an unexpected format."
                    )
                    st.json(translation_result)
    else:
        st.warning("Please enter some text to translate.")

st.divider()
st.sidebar.header("ℹ️ About This App")
st.sidebar.info(
    "An interactive web application that translates text into various languages. Built with Python and Streamlit, it leverages the Hugging Face Inference API and Helsinki-NLP models to provide real-time translations."
)
