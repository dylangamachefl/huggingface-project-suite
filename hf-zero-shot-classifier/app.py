# app.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Assuming your .env file is in the parent 'ai-portfolio' directory
dotenv_path = os.path.join(
    os.path.dirname(__file__), "..", ".env"
)  # Navigate one level up to ai-portfolio
load_dotenv(dotenv_path=dotenv_path)

API_TOKEN = os.getenv("HF_TOKEN")

# Define the model API URL
# Model suggestion from the plan: facebook/bart-large-mnli
# You can also try smaller ones like 'valhalla/distilbart-mnli-12-3' if 'bart-large-mnli' is too slow/hits rate limits quickly
MODEL_ID = "facebook/bart-large-mnli"
# Alternative model: MODEL_ID = "valhalla/distilbart-mnli-12-3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

# Headers for the API request
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query_hf_api(payload):
    """
    Sends a request to the Hugging Face Inference API.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
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

# Input fields
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
        # Prepare labels: split string into a list and strip whitespace
        candidate_labels = [
            label.strip()
            for label in candidate_labels_input.split(",")
            if label.strip()
        ]  # Ensure labels are not empty

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
                        # The API returns 'labels' and 'scores' as parallel lists.
                        # For most zero-shot models, these are already sorted by score (highest first).

                        results_with_scores = list(
                            zip(result["labels"], result["scores"])
                        )

                        # Display them
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
                        st.json(result)  # Display the raw response for debugging

                except requests.exceptions.RequestException as e:
                    st.error(f"API Request Failed: {e}")
                    if e.response is not None:
                        st.error(
                            f"Response content: {e.response.text}"
                        )  # Show more details on API error
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

st.markdown("---")
