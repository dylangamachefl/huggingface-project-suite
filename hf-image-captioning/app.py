import streamlit as st
from PIL import Image
import io
from transformers import pipeline

st.set_page_config(layout="wide", page_title="Image Captioning Tool (Transformers)")


# --- Model Loading ---
@st.cache_resource
def load_captioning_pipeline():
    """Loads the image captioning pipeline from Transformers."""
    model_id = "Salesforce/blip-image-captioning-base"
    try:
        captioner = pipeline("image-to-text", model=model_id)
        return captioner
    except Exception as e:
        print(f"Error loading captioning model '{model_id}': {e}")
        return None


captioner = load_captioning_pipeline()

# --- Streamlit UI ---
st.title("🖼️ Image Captioning Tool (using Transformers)")

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

if uploaded_file is not None and captioner is not None:
    image_bytes = uploaded_file.getvalue()

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
