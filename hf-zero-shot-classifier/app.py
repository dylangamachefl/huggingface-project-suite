import streamlit as st
import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

API_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "facebook/bart-large-mnli"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query_hf_api(payload):
    """
    Sends a request to the Hugging Face Inference API.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


st.set_page_config(layout="wide", page_title="Zero-Shot Text Classifier")

st.title("🎯 Zero-Shot Text Classifier")
st.markdown(
    f"""
This app uses the `{MODEL_ID}` Zero-Shot Classification model from Hugging Face 
to classify text into categories you define, even if the model hasn't been explicitly trained on those categories.
Enter a piece of text and a comma-separated list of potential labels.
"""
)

text_to_classify = st.text_area(
    "Enter text to classify:",
    "The new AI regulations will have a significant impact on technology startups.",
    height=100,
)
candidate_labels_input = st.text_input(
    "Enter candidate labels (comma-separated):",
    "politics, business, technology, sports, education, finance",
)

if st.button("Classify Text"):
    if not API_TOKEN:
        st.error(
            "Hugging Face API token not found. Please set HUGGING_FACE_API_TOKEN in your .env file."
        )
    elif not text_to_classify.strip():
        st.warning("Please enter some text to classify.")
    elif not candidate_labels_input.strip():
        st.warning("Please enter some candidate labels.")
    else:
        candidate_labels = [
            label.strip()
            for label in candidate_labels_input.split(",")
            if label.strip()
        ]

        if not candidate_labels:
            st.warning(
                "No valid candidate labels provided after parsing. Please ensure labels are separated by commas and are not empty."
            )
        else:
            payload = {
                "inputs": text_to_classify,
                "parameters": {"candidate_labels": candidate_labels},
            }

            with st.spinner(f"Asking the AI model ({MODEL_ID})..."):
                try:
                    result = query_hf_api(payload)

                    st.subheader("Classification Results:")

                    if (
                        isinstance(result, dict)
                        and "labels" in result
                        and "scores" in result
                    ):
                        results_with_scores = list(
                            zip(result["labels"], result["scores"])
                        )

                        for label, score in results_with_scores:
                            st.write(f"**Label:** {label} - **Score:** {score:.4f}")

                    elif isinstance(result, dict) and "error" in result:
                        st.error(f"API Error: {result['error']}")
                        if "estimated_time" in result:
                            st.info(
                                f"The model might be loading. Estimated time: {result['estimated_time']:.2f} seconds. Please try again shortly."
                            )
                    else:
                        st.error("Received an unexpected response format from the API.")
                        st.json(result)

                except requests.exceptions.RequestException as e:
                    st.error(f"API Request Failed: {e}")
                    if e.response is not None:
                        st.error(f"Response content: {e.response.text}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

st.markdown("---")
