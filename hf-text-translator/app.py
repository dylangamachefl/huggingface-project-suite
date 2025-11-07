import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- Configuration ---
# Attempt to load .env file.
# Assumes .env is in the parent directory of this script's location (e.g., ../.env)
# If your app.py is in the root of your project (where .env also is),
# load_dotenv() without arguments might work.
# For Hugging Face Spaces, you'll set secrets directly in the Space settings.
dotenv_path = os.path.join(
    os.path.dirname(__file__), "..", ".env"
)  # Path to .env in parent directory
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    # Fallback if .env is in the current directory (less likely for multi-project setup)
    load_dotenv()


API_TOKEN = os.getenv("HF_TOKEN")
API_URL_BASE = "https://api-inference.huggingface.co/models/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Define available models (user-friendly name: model_id)
# You can find more models at https://huggingface.co/models?pipeline_tag=translation
# Filter by source language and target language.
TRANSLATION_MODELS = {
    "English to Spanish": "Helsinki-NLP/opus-mt-en-es",
    "English to French": "Helsinki-NLP/opus-mt-en-fr",
    "English to German": "Helsinki-NLP/opus-mt-en-de",
    "English to Chinese (Simplified)": "Helsinki-NLP/opus-mt-en-zh",
    "English to Japanese": "Helsinki-NLP/opus-mt-en-jap",  # Check model hub for exact ID if this doesn't work
    "Spanish to English": "Helsinki-NLP/opus-mt-es-en",
    "French to English": "Helsinki-NLP/opus-mt-fr-en",
    # Add more models/languages as desired
}


# --- Hugging Face API Call Function ---
def query_translation(text_to_translate, model_id):
    """
    Sends a request to the Hugging Face Inference API for translation.
    """
    if not API_TOKEN:  # Check if token was loaded
        st.error(
            "Hugging Face API Token not found. Please configure it in your .env file or Space secrets."
        )
        return None

    api_url = API_URL_BASE + model_id
    payload = {"inputs": text_to_translate}

    try:
        response = requests.post(
            api_url, headers=HEADERS, json=payload, timeout=30
        )  # Added timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        st.error(f"Translation API HTTP Error: {errh}")
        error_details = "No additional details from API."
        try:
            error_details = response.json().get("error", response.text)
        except ValueError:  # If response.text is not JSON
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
    except (
        ValueError
    ):  # If response is not JSON (should be caught by response.json() above but good to have)
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

# Check for API token at the beginning of UI rendering
if not API_TOKEN:
    st.error("Hugging Face API Token not configured. The application cannot function.")
    st.markdown(
        "Please ensure your `HUGGING_FACE_API_TOKEN` is set in a `.env` file "
        "in the root of your `ai-portfolio` project or as a secret if deploying on Hugging Face Spaces."
    )
    st.stop()  # Stop further execution of the script if token is missing

# Layout columns
col1, col2 = st.columns([2, 1])  # Text area takes 2/3, selectbox takes 1/3

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
        if not API_TOKEN:  # Redundant check, but good for safety
            st.error("API Token is missing. Cannot proceed.")
        else:
            with st.spinner(f"Translating to {selected_language_name}... Please wait."):
                translation_result = query_translation(text_input, model_id_to_use)

            if translation_result:
                # The API returns a list with a dictionary inside
                if (
                    isinstance(translation_result, list)
                    and len(translation_result) > 0
                    and "translation_text" in translation_result[0]
                ):
                    translated_text = translation_result[0]["translation_text"]
                    st.subheader("📜 Translation:")
                    st.success(translated_text)
                # Sometimes the API might return a dictionary directly with an error
                elif isinstance(translation_result, dict) and translation_result.get(
                    "error"
                ):
                    # Error is already displayed by the query_translation function
                    st.warning("Translation failed. See error message above.")
                else:
                    st.error(
                        "Translation failed or the API returned an unexpected format."
                    )
                    st.json(translation_result)  # Show the raw response for debugging
            # If translation_result is None, query_translation already showed an error
    else:
        st.warning("Please enter some text to translate.")

st.divider()
st.sidebar.header("ℹ️ About This App")
st.sidebar.info(
    "This tool demonstrates the use of the Hugging Face Inference API "
    "for text translation. It allows users to input text and select a target "
    "language, then displays the translated output."
    "\n\n**Key Skills Showcased:**"
    "\n- Python & Streamlit for UI"
    "\n- Hugging Face API Integration"
    "\n- Handling API responses & errors"
    "\n- Basic NLP application"
)
st.sidebar.markdown("---")
st.sidebar.markdown("Project for **AI Project Portfolio (4 Weeks)**")
