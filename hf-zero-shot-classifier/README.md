---
title: Zero-Shot Text Classifier
emoji: 🎯 # Or any emoji you like
colorFrom: purple # Example color
colorTo: indigo  # Example color
sdk: streamlit
app_file: app.py
pinned: false 
---

# 🎯 Zero-Shot Text Classifier

An interactive web application that classifies input text into user-defined categories using Hugging Face's zero-shot classification models via the Inference API. This project is part of a 4-week AI project portfolio building challenge.

**Live Demo:** [Link to your Deployed App on Hugging Face Spaces]

**Project Repository:** `https://github.com/dylangamachefl/hf-zero-shot-classifier`

## 📖 Overview

This application provides a simple interface for users to:
1.  Input any piece of text.
2.  Provide a comma-separated list of candidate labels (categories).
3.  Receive a ranked list of these labels based on how well they apply to the input text, as determined by a zero-shot classification model.

The primary goal is to demonstrate the ability to leverage powerful, general-purpose NLP models for flexible text categorization without needing to train a model on specific categories beforehand.

## 🎯 Problem Solved

Traditional text classification often requires training a model on a predefined set of categories with labeled data. This can be time-consuming and inflexible if categories change or new ones emerge. Zero-shot classification addresses this by allowing classification against arbitrary labels at inference time. This tool showcases a practical application of this capability, offering on-the-fly text categorization.

## ✨ Skills Showcased

*   **AI/ML Implementation:** Utilizing pre-trained NLP models for zero-shot classification.
*   **Python:** Core programming language for backend logic and API interaction.
*   **ML Libraries (Conceptual):** Understanding the role and use of Hugging Face Transformers (even if used via API).
*   **API Integration:** Connecting to and consuming the Hugging Face Inference API.
*   **Data Handling:** Sending text and label data to the API and parsing JSON responses.
*   **NLP (using APIs):** Practical application of Natural Language Processing for dynamic text classification.
*   **Web Development (UI):** Building an interactive user interface with Streamlit.
*   **Environment Management:** Use of `.env` for API keys.
*   **Version Control:** Git and GitHub for project management.
*   **Deployment:** Deploying the application to Hugging Face Spaces.
*   **Documentation:** Creating clear and concise project documentation (this README).

## 🛠️ How It Works

1.  **User Input:**
    *   The user types or pastes the text they want to classify into a text area.
    *   The user provides a comma-separated list of candidate labels (e.g., "technology, sports, finance").
2.  **API Call Preparation:** When the "Classify Text" button is clicked:
    *   The Python backend (using the `requests` library) prepares a payload. This payload includes the input text and the list of candidate labels.
3.  **Hugging Face API Interaction:**
    *   A POST request is made to the Hugging Face Inference API endpoint for a selected zero-shot classification model (e.g., `facebook/bart-large-mnli` or `valhalla/distilbart-mnli-12-3`).
    *   The Hugging Face API token (loaded securely from environment variables) is included in the request headers for authentication.
4.  **Zero-Shot Classification:** The Hugging Face model processes the input text against the provided candidate labels, calculating a relevance score for each label. It does this without having been explicitly trained on these specific labels beforehand.
5.  **Response Handling:** The application receives the API's JSON response, which typically contains the input sequence, the list of labels, and a corresponding list of scores, often sorted by relevance.
6.  **Display Output:** The labels and their scores are extracted from the response and displayed to the user in the Streamlit interface, ranked by score. Error handling is implemented for API issues or unexpected responses.

## 💻 Technologies Used

*   **Programming Language:** Python 3.x
*   **AI Models/API:**
    *   Hugging Face Hub
    *   Hugging Face Inference API (Free Tier)
    *   Zero-Shot Classification Models (e.g., `facebook/bart-large-mnli`, `valhalla/distilbart-mnli-12-3`)
*   **Python Libraries:**
    *   `streamlit`: For building the web application UI.
    *   `requests`: For making HTTP requests to the Hugging Face API.
    *   `python-dotenv`: For managing environment variables (like the API token) locally.
*   **Version Control:** Git & GitHub
*   **Deployment:** Hugging Face Spaces
*   **Development Environment:** Visual Studio Code (or your preferred IDE), Python Virtual Environment (`venv` or `conda`)

## 🚀 Setup and Local Development

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/[Your GitHub Username]/hf-zero-shot-classifier.git
    cd hf-zero-shot-classifier
    ```

2.  **Set up a Python virtual environment:**
    (Assuming you have a shared `venv` or `conda` environment in a parent `ai-portfolio` directory as per the overall plan)
    ```bash
    # From within hf-zero-shot-classifier directory:
    # Example for venv:
    # For macOS/Linux:
    source ../venv/bin/activate 
    # For Windows (Git Bash or PowerShell):
    # source ../venv/Scripts/activate
    # For Windows (Command Prompt):
    # ..\venv\Scripts\activate

    # Example for conda (if your shared env is named 'ai_env'):
    # conda activate ai_env 
    ```
    If you don't have the shared environment or prefer a dedicated one:
    ```bash
    python -m venv venv # Or: conda create -n hf_zero_shot_env python=3.9
    # Activate it:
    # macOS/Linux: source venv/bin/activate
    # Windows: venv\Scripts\activate
    # Conda: conda activate hf_zero_shot_env
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Hugging Face API Token:**
    *   Ensure you have a `.env` file in the root of your main `ai-portfolio` project directory (i.e., one level above this `hf-zero-shot-classifier` project).
    *   Add your Hugging Face API token to the `.env` file:
        ```
        HUGGING_FACE_API_TOKEN="your_hf_api_token_here"
        ```
    *   *Note: The `app.py` is configured to look for `.env` in the parent directory. If your `.env` file is elsewhere, you might need to adjust the `load_dotenv()` path in `app.py`.*

5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application should open in your web browser.

## 🖼️ Screenshot

<!-- Add your screenshot here -->
![Application Screenshot](images/zero-shot-classifier-screenshot.png) 
<!-- Make sure to create an 'images' folder and add your screenshot, 
     or adjust the path if it's different. -->

## 🔮 Future Enhancements (Optional)

*   **Multi-label classification option:** Allow the model to predict multiple relevant labels if appropriate (some models support this via parameters).
*   **Adjustable threshold:** Allow users to set a confidence threshold for displayed labels.
*   **Model selection:** Allow users to choose from a few different zero-shot classification models.
*   **Example use cases:** Provide example texts and label sets to demonstrate capabilities.

## 🙏 Acknowledgements

*   The Hugging Face team for their incredible models, Inference API, and Spaces platform.
*   The developers of Streamlit for making web app creation in Python so accessible.

---