---
title: HF Sentiment Analyzer
emoji: 🤗 # You can choose an emoji
colorFrom: blue # Or any color
colorTo: green # Or any color
sdk: streamlit
app_file: app.py
# For Docker, you don't usually specify sdk_version directly here
# unless the template specifically requires it.
# If your Dockerfile handles Python/Streamlit versions, that's usually enough.
# If the Streamlit Docker Template implies a specific Dockerfile or setup,
# then 'sdk: docker' and 'app_file: app.py' are key.
# The template might also have set 'dockerfile: Dockerfile' if it expects one.
pinned: false
---

# Project 1: Hugging Face Sentiment Analyzer

## Overview
This project is a web application that performs sentiment analysis on user-provided text. It utilizes the Hugging Face Inference API to leverage a pre-trained sentiment analysis model (`distilbert/distilbert-base-uncased-finetuned-sst-2-english`). The user interface is built with Streamlit.

This is the first project in my [4-Week AI Project Portfolio Action Plan](https://github.com/dylangamachefl/dylangamachefl).

## Problem Solved
Provides a simple way to quickly determine the sentiment (Positive/Negative) of a piece of text without needing to set up a local model or manage complex infrastructure. Useful for quick checks, demonstrations, or as a component in a larger text processing pipeline.

## Skills Showcased
*   **AI/ML Implementation:** Using a pre-trained NLP model via an API.
*   **Python:** Core language for application development.
*   **API Integration:** Calling the Hugging Face Inference API (`requests` library).
*   **Data Handling:** Processing JSON responses from the API.
*   **Web Development/UI:** Building an interactive user interface with Streamlit.
*   **Environment Management:** Use of `.env` for API keys.
*   **Version Control:** Git & GitHub for code management.
*   **Documentation:** This README.
*   **(Soon) Deployment:** Deploying to Hugging Face Spaces.

## How it Works
1.  The user enters text into a Streamlit text area.
2.  Upon clicking "Analyze Sentiment," the Python backend (`app.py`) takes the input.
3.  It retrieves the Hugging Face API token from a secure `.env` file.
4.  A POST request is made to the Hugging Face Inference API endpoint for the `distilbert/distilbert-base-uncased-finetuned-sst-2-english` model, with the user's text as the payload.
5.  The API processes the text and returns a JSON response containing sentiment labels (e.g., "POSITIVE", "NEGATIVE") and their corresponding confidence scores.
6.  The application parses this JSON response.
7.  The most dominant sentiment and its score are displayed back to the user in the Streamlit interface.

## Technologies & Libraries
*   **Programming Language:** Python 3.x
*   **AI Model API:** Hugging Face Inference API
*   **Model Used:** `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
*   **Libraries:**
     *   `streamlit`: For the web user interface.
     *   `requests`: For making HTTP requests to the API.
     *   `python-dotenv`: For managing environment variables (API key).
*   **Cloud Service (for API):** Hugging Face
*   **Deployment (planned):** Hugging Face Spaces

## Setup and Usage Locally
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dylangamachefl/hf-sentiment-analyzer.git
    cd hf-sentiment-analyzer
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your Hugging Face API Token:**
    *   Go to your main project directory (e.g., `ai-portfolio` if this project is a subdirectory).
    *   Ensure you have a `.env` file in that parent directory containing your Hugging Face API token:
      ```
      HUGGING_FACE_API_TOKEN="your_actual_hf_api_token_here"
      ```
    *   The `app.py` is configured to look for the `.env` file in its parent directory.
5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
6.  Open your browser and go to `http://localhost:8501`.

## Screenshot
(It's a good idea to add a screenshot of your working application here later, once you're happy with it.)
<!-- Example: ![App Screenshot](path/to/your/screenshot.png) -->

## Future Improvements (Optional)
*   [Any ideas you have for making it better]