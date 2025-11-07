---
title: HF Text Translator
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

# 🌍 Hugging Face Text Translation Tool

An interactive web application that translates text into various languages using Hugging Face's state-of-the-art translation models via the Inference API. This project is part of a 4-week AI project portfolio building challenge.

**Live Demo:** [Link to your Deployed App on Hugging Face Spaces]

**Project Repository:** `https://github.com/dylangamachefl/hf-text-translator`

## 📖 Overview

This application provides a simple and intuitive interface for users to:
1.  Input text they wish to translate.
2.  Select a target language from a predefined list.
3.  Receive the translated text, processed by powerful models hosted on Hugging Face.

The primary goal is to demonstrate the ability to integrate with external AI services (Hugging Face Inference API) and build a functional NLP application with a user-friendly UI.

## 🎯 Problem Solved

In an increasingly globalized world, language barriers can hinder communication and access to information. This tool offers a quick and accessible way to translate text, helping to bridge these gaps. It showcases how pre-trained AI models can be leveraged to build practical solutions for common language-related tasks.

## ✨ Skills Showcased

*   **AI/ML Implementation:** Utilizing pre-trained NLP models for a specific task (translation).
*   **Python:** Core programming language for backend logic and API interaction.
*   **ML Libraries (Conceptual):** Understanding the role and use of Hugging Face Transformers (even if used via API).
*   **API Integration:** Connecting to and consuming the Hugging Face Inference API.
*   **Data Handling:** Sending text data to the API and parsing JSON responses.
*   **NLP (using APIs):** Practical application of Natural Language Processing for translation.
*   **Web Development (UI):** Building an interactive user interface with Streamlit.
*   **Environment Management:** Use of `.env` for API keys.
*   **Version Control:** Git and GitHub for project management.
*   **Deployment:** Deploying the application to Hugging Face Spaces.
*   **Documentation:** Creating clear and concise project documentation (this README).

## 🛠️ How It Works

1.  **User Input:** The user types or pastes the text they want to translate into a text area.
2.  **Language Selection:** The user selects the desired target language from a dropdown menu. Each language option is mapped to a specific Hugging Face translation model ID (primarily from the Helsinki-NLP group, e.g., `Helsinki-NLP/opus-mt-en-es` for English to Spanish).
3.  **API Call:** When the "Translate" button is clicked:
    *   The Python backend (using the `requests` library) constructs a POST request to the Hugging Face Inference API endpoint for the selected model.
    *   The input text is sent in the JSON payload.
    *   The Hugging Face API token (loaded securely from environment variables) is included in the request headers for authentication.
4.  **Processing:** The Hugging Face infrastructure runs the inference on the chosen translation model.
5.  **Response Handling:** The application receives the API's JSON response, which contains the translated text (typically within a list and dictionary structure like `[{'translation_text': '...'}]`).
6.  **Display Output:** The translated text is extracted from the response and displayed to the user in the Streamlit interface. Error handling is implemented to manage API issues or unexpected responses.

## 💻 Technologies Used

*   **Programming Language:** Python 3.x
*   **AI Models/API:**
    *   Hugging Face Hub
    *   Hugging Face Inference API (Free Tier)
    *   Helsinki-NLP Translation Models (e.g., `opus-mt-*`)
*   **Python Libraries:**
    *   `streamlit`: For building the web application UI.
    *   `requests`: For making HTTP requests to the Hugging Face API.
    *   `python-dotenv`: For managing environment variables (like the API token) locally.
*   **Version Control:** Git & GitHub
*   **Deployment:** Hugging Face Spaces
*   **Development Environment:** Visual Studio Code (or your preferred IDE), Python Virtual Environment (`venv`)

## 🚀 Setup and Local Development

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/[Your GitHub Username]/hf-text-translator.git
    cd hf-text-translator
    ```

2.  **Set up a Python virtual environment:**
    (Assuming you have a shared `venv` in a parent `ai-portfolio` directory as per the overall plan)
    ```bash
    # From within hf-text-translator directory:
    # For macOS/Linux:
    source ../venv/bin/activate
    # For Windows (Git Bash or PowerShell):
    # source ../venv/Scripts/activate
    # For Windows (Command Prompt):
    # ..\venv\Scripts\activate
    ```
    If you don't have the shared venv or prefer a dedicated one for this project:
    ```bash
    python -m venv venv
    # Activate it:
    # macOS/Linux: source venv/bin/activate
    # Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Hugging Face API Token:**
    *   Create a `.env` file in the root of your main `ai-portfolio` project directory (i.e., one level above this `hf-text-translator` project).
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

## 🔮 Future Enhancements (Optional)

*   **Auto-detect source language:** Implement a feature to automatically detect the language of the input text.
*   **Support more languages:** Expand the list of available target languages by adding more Helsinki-NLP models.
*   **Batch translation:** Allow users to upload a file for translating multiple pieces of text.
*   **Improved UI/UX:** Further refine the user interface for better aesthetics and usability.

## 🙏 Acknowledgements

*   The Hugging Face team for their incredible models, Inference API, and Spaces platform.
*   The developers of Streamlit for making web app creation in Python so accessible.

---