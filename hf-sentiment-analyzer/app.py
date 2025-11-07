import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- IMPORTANT: For loading .env file from the PARENT directory ---
# This assumes your .env file is in the 'ai-portfolio' directory,
# and 'hf-sentiment-analyzer' is a subdirectory of 'ai-portfolio'.
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)
# --- End of .env loading section ---

# Retrieve the API token
API_TOKEN = os.getenv("HF_TOKEN")

# Define the Hugging Face Inference API URL and the model
API_URL = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query_sentiment_api(payload):
    """Sends a request to the Hugging Face sentiment analysis API."""
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


# --- Streamlit App Interface ---
st.set_page_config(layout="wide", page_title="Sentiment Analysis App")

st.title("Sentiment Analysis with Hugging Face 🤗")
st.markdown(
    """
    Enter some text below to analyze its sentiment (Positive/Negative).
    This app uses the `distilbert-base-uncased-finetuned-sst-2-english` model
    via the Hugging Face Inference API.
"""
)

user_input = st.text_area(
    "Enter text for sentiment analysis:", "I love using Hugging Face models!"
)

if st.button("Analyze Sentiment"):
    if user_input:
        try:
            st.info("Analyzing...")
            payload = {"inputs": user_input}
            api_response = query_sentiment_api(payload)

            # --- Displaying Results ---
            st.subheader("Analysis Result:")

            # The API response for this model is a list of lists of dictionaries.
            # Example: [[{'label': 'POSITIVE', 'score': 0.9998772144317627}]]
            if (
                api_response
                and isinstance(api_response, list)
                and isinstance(api_response[0], list)
                and api_response[0]
                and isinstance(api_response[0][0], dict)
            ):

                # For this specific model, we usually get one primary sentiment.
                # Some models might return scores for multiple labels.
                # We'll focus on the highest score if multiple are present,
                # or the first one if it's structured as a list of labels per input.

                # Find the label with the highest score
                # (Though distilbert-sst-2 usually returns one dominant label directly)
                # For this model, the structure is often [[{'label': 'POSITIVE', 'score': ...}]]
                # or [[{'label': 'NEGATIVE', 'score': ...}]]

                # Let's find the dominant sentiment
                dominant_sentiment = None
                highest_score = -1

                # The response is a list of results (usually one for single input)
                # Each result is a list of label-score dictionaries
                for label_score_pair in api_response[0]:
                    label = label_score_pair.get("label")
                    score = label_score_pair.get("score")

                    if label and score is not None:
                        st.write(f"Label: {label}, Score: {score:.4f}")
                        if score > highest_score:
                            highest_score = score
                            dominant_sentiment = label

                if dominant_sentiment:
                    if dominant_sentiment == "POSITIVE":
                        st.markdown(
                            f"**Overall Sentiment: <span style='color:green;'>{dominant_sentiment}</span> (Score: {highest_score:.4f})**",
                            unsafe_allow_html=True,
                        )
                    elif dominant_sentiment == "NEGATIVE":
                        st.markdown(
                            f"**Overall Sentiment: <span style='color:red;'>{dominant_sentiment}</span> (Score: {highest_score:.4f})**",
                            unsafe_allow_html=True,
                        )
                    else:  # Other labels, if any
                        st.markdown(
                            f"**Overall Sentiment: {dominant_sentiment} (Score: {highest_score:.4f})**"
                        )
                else:
                    st.warning(
                        "Could not determine the dominant sentiment from the response."
                    )

                with st.expander("View Raw API Response"):
                    st.json(api_response)
            else:
                st.error("Received an unexpected response format from the API.")
                st.json(api_response)  # Show the actual response for debugging

        except requests.exceptions.HTTPError as http_err:
            st.error(f"API Request HTTP error occurred: {http_err}")
            st.write(
                "Details:",
                http_err.response.text if http_err.response else "No response details",
            )
        except requests.exceptions.RequestException as req_err:
            st.error(f"API Request error occurred: {req_err}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter some text to analyze.")

st.sidebar.header("About")
st.sidebar.info(
    "This is Project 1 from the '4-Week AI Project Portfolio Action Plan'. "
    "It demonstrates calling a Hugging Face Inference API for sentiment analysis "
    "and displaying the results using a Streamlit UI."
)
