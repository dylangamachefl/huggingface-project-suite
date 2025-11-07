# app.py (for hf-image-captioning - using Transformers library)

import streamlit as st
from PIL import Image
import io

# NEW IMPORTS for Transformers
from transformers import pipeline
import torch

# --- Streamlit Page Configuration (MUST BE FIRST STREAMLIT COMMAND) ---
st.set_page_config(layout="wide", page_title="Image Captioning Tool (Transformers)")


# --- Model Loading (Cached) ---
@st.cache_resource
def load_captioning_pipeline():
    """Loads the image captioning pipeline from Transformers."""
    model_id = "Salesforce/blip-image-captioning-base"
    # We'll display success/error messages in the main app body after set_page_config
    try:
        captioner = pipeline("image-to-text", model=model_id)
        return captioner  # Return the captioner or None
    except Exception as e:
        # Instead of st.error here, we can log or print,
        # and handle the None return value in the main app body.
        print(f"Error loading captioning model '{model_id}': {e}")  # Log to console
        return None


# Load the pipeline
captioner = load_captioning_pipeline()

# --- Streamlit UI ---
st.title("🖼️ Image Captioning Tool (using Transformers)")

# Display model loading status here, after set_page_config
if captioner:
    st.success(
        f"Image captioning model '{captioner.model.name_or_path}' loaded successfully!"
    )
    st.markdown(
        f"""
    Upload an image and this app will generate a caption for it using the 
    `{captioner.model.name_or_path}` model loaded directly with the Transformers library.
    """
    )
else:
    st.error(
        "The image captioning model could not be loaded. Please check the console logs for details."
    )
    st.markdown(
        """
    Model loading failed. Captioning functionality will be unavailable.
    """
    )

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# ... (rest of the code remains the same) ...
if uploaded_file is not None and captioner is not None:
    # To read file as bytes:
    image_bytes = uploaded_file.getvalue()

    # Display the uploaded image
    try:
        image_pil = Image.open(io.BytesIO(image_bytes))
        st.image(image_pil, caption="Uploaded Image.", use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {e}")
        uploaded_file = None

if uploaded_file and captioner and st.button("Generate Caption"):
    with st.spinner(
        f"Generating caption with {captioner.model.name_or_path}... (This might take a moment)"
    ):
        try:
            result = captioner(image_pil)

            st.subheader("Generated Caption:")
            if isinstance(result, list) and result:
                caption = result[0].get(
                    "generated_text", "Caption not found in response."
                )
                st.success(caption)
            else:
                st.error("Received an unexpected response format from the model.")
                st.json(result)

        except Exception as e:
            st.error(f"An unexpected error occurred during captioning: {e}")

elif not captioner and uploaded_file:
    st.warning("Captioning model not loaded. Cannot generate caption.")


st.markdown("---")
st.markdown(
    "Developed as part of the AI Project Portfolio Action Plan. Now using local Transformers model."
)
