import streamlit as st
import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

# Config
API_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query_sentiment_api(payload):
    """Sends a request to the Hugging Face sentiment analysis API."""
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


# --- Streamlit UI ---
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

            st.subheader("Analysis Result:")

            if (
                api_response
                and isinstance(api_response, list)
                and isinstance(api_response[0], list)
                and api_response[0]
                and isinstance(api_response[0][0], dict)
            ):
                dominant_sentiment = None
                highest_score = -1

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
                    else:
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
                st.json(api_response)

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
    "A simple web app for text sentiment analysis using Hugging Face Inference API and Streamlit."
)
