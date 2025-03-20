import streamlit as st
import requests
import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# Use Streamlit secrets to get the API key
ROBOFLOW_API_KEY = st.secrets["ROBOFLOW_API_KEY"]

# Define your Roboflow model details
ROBOFLOW_MODEL = "gemstones-2e1jx"
ROBOFLOW_VERSION = "3"
ROBOFLOW_URL = (
    f"https://detect.roboflow.com/{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}"
)

# Paths to images inside the 'images' folder
BACKGROUND_IMAGE_PATH = "images/background.png"  # Space background image
LOGO_IMAGE_PATH = "images/logo.png"  # Logo of the app


def detect_gemstones(image_bytes):
    """
    Sends the image to Roboflow YOLOv8 API for gemstone detection and classification.
    Returns predictions and an error message (if any).
    """
    response = requests.post(
        ROBOFLOW_URL,
        params={"api_key": ROBOFLOW_API_KEY},
        files={"file": image_bytes},
    )

    if response.status_code != 200:
        return None, "❌ Error: Unable to process image."

    result = response.json()
    if "predictions" not in result or len(result["predictions"]) == 0:
        return None, "⚠️ No gemstone detected in the image."

    return result, None


def draw_boxes(image_bytes, predictions):
    """
    Draws bounding boxes around detected gemstones with their classifications.
    Returns the modified image as bytes.
    """
    image = Image.open(BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)

    for pred in predictions:
        x, y, width, height = (
            pred["x"],
            pred["y"],
            pred["width"],
            pred["height"],
        )
        gemstone_type = pred["class"]

        # Calculate bounding box coordinates
        x0, y0 = x - width / 2, y - height / 2
        x1, y1 = x + width / 2, y + height / 2

        # Draw bounding box and label
        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        draw.text((x0, y0 - 10), gemstone_type, fill="red")

    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG")
    return output_buffer.getvalue()


page_element = """
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.wallpapersafari.com/88/75/cLUQqJ.jpg");
  background-size: cover;
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_element, unsafe_allow_html=True)

# Set Streamlit page configuration
st.set_page_config(
    page_title="Space Gem",
    page_icon="💎",
    layout="wide",
)


# Logo and Title section
if os.path.exists(LOGO_IMAGE_PATH):
    with open(LOGO_IMAGE_PATH, "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo Space Gem" width="200">
    </div>
    <div style="text-align: center; padding-top: 20px;">
        <h4 style="color: #333333; font-size: 1.5rem;">Identify Your Gemstone</h4>
    </div>
    <div style="text-align: center;">
        <h4 style="color: #333333; font-size: 1.5rem;">📸 Upload the Image of Your Gemstone</h4>
    </div>
    """,
    unsafe_allow_html=True,
)

# File uploader section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    img_file_buffer = st.file_uploader("", type=["png", "jpg", "jpeg"])

# Handle file upload and processing
if img_file_buffer is not None:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        img_bytes = img_file_buffer.getvalue()
        with st.spinner("✨ Analyzing the gemstone..."):
            result, error = detect_gemstones(img_bytes)

        if result:
            for pred in result["predictions"]:
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <h4>💎 Detected Gemstone:</h4>
                        <div>👉 {pred['class'].capitalize()} (Confidence: {pred['confidence']:.2f})</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Show the processed image with bounding boxes
            processed_image = draw_boxes(img_bytes, result["predictions"])
            st.markdown(
                f"""
                    <div style="text-align: center;">
                        <img src="data:image/png;base64,{base64.b64encode(processed_image).decode()}" class="processed-image" alt="Processed Gemstone Image">
                    </div>
                    """,
                unsafe_allow_html=True,
            )

        else:
            st.error(error)

# Close the main container div
st.markdown("</div>", unsafe_allow_html=True)

# Footer (hidden)
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
