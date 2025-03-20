import streamlit as st
import requests

# from dotenv import load_dotenv
import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# # Load environment variables, including the Roboflow API Key
# load_dotenv()
#
# # Define your Roboflow API Key and model details
# ROBOFLOW_API_KEY = os.getenv(
#     "ROBOFLOW_API_KEY", "your-roboflow-api-key"
# )  # Replace with actual key

# Use Streamlit secrets to get the API key
ROBOFLOW_API_KEY = st.secrets["ROBOFLOW_API_KEY"]

# Defining the model details
ROBOFLOW_MODEL = "gemstones-2e1jx"
ROBOFLOW_VERSION = "3"

# Roboflow API Endpoint
ROBOFLOW_URL = (
    f"https://detect.roboflow.com/{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}"
)


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
        # Extract bounding box coordinates and gemstone classification
        x, y, width, height = (
            pred["x"],
            pred["y"],
            pred["width"],
            pred["height"],
        )
        gemstone_type = pred["class"]

        # Calculate the rectangle coordinates for the bounding box
        x0, y0 = x - width / 2, y - height / 2
        x1, y1 = x + width / 2, y + height / 2

        # Draw the bounding box and label
        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        draw.text((x0, y0 - 10), gemstone_type, fill="red")

    # Save the modified image to a buffer and return its bytes
    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG")
    return output_buffer.getvalue()


# Set Streamlit page configuration
st.set_page_config(
    page_title="Space Gem",
    page_icon="💎",
    layout="wide",
)

# Paths to images inside the 'images' folder
BACKGROUND_IMAGE_PATH = "images/background.png"  # Space background image
LOGO_IMAGE_PATH = "images/logo.png"  # Logo of the app


def set_background_color(apply_background=True):
    """
    Configures the app's background image and responsive CSS styling.
    """
    if apply_background:
        with open(BACKGROUND_IMAGE_PATH, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('data:image/jpeg;base64,{image_base64}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: white;
                height: 100%;
                padding: 0;
            }}
            .main {{
                max-width: 1000px;
                width: 90%;
                margin: 0 auto;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                color: #333;
                z-index: 1;
                min-height: 100vh;
                flex-direction: column;
                justify-content: space-between;
                # overflow-x: hidden; /* prevent horizontal scroll */
                # overflow-y: auto; /* prevent vertical scroll */
            }}
            h1, h4, p {{
                text-align: center;
                font-family: 'Arial', sans-serif;
            }}
            .spinner-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh; /* Take up full height of the viewport */ 
                text-align: center;rem;
            }}
            .processed-image {{
                display: block;
                margin: 0 auto;
                max-width: 50%; /* Adjust the width for responsiveness */
                height: auto;
                border-radius: 12px;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
            }}
            .prediction-text {{
                text-align: center;
                font-size: 1.2rem;
                font-weight: bold;
                margin-top: 10px;
            }}
            .stButton>button {{
                background-color: #4e73df;
                border-radius: 50px;
                color: white;
                font-weight: bold;
                padding: 10px 30px;
                transition: all 0.3s ease;
            }}
            .stButton>button:hover {{
                background-color: #2e59a3;
            }}
            /* Media Queries for responsiveness */
            @media (max-width: 768px) {{
                h1 {{
                    font-size: 2.5rem;
                }}
                h4 {{
                    font-size: 1.2rem;
                }}
                p {{
                    font-size: 1rem;
                }}
                .uploaded-image {{
                    max-width: 90%;
                }}
            }}
            /* Webkit Browsers (Chrome, Chromium, Safari, Edge) */
            ::-webkit-scrollbar {{
                width: 8px;
                height: 8px;
                background: rgba(255, 255, 255, 0.9); /* Background matches the content */
            }}
            ::-webkit-scrollbar-thumb {{
                background-color: rgba(255, 255, 255, 0.9); /* Thumb color matches the content */
                border-radius: 10px;
            }}
            ::-webkit-scrollbar-thumb:hover {{
                background-color: rgba(255, 255, 255, 0.7); /* Slightly darker on hover */
            }}
            ::-webkit-scrollbar-track {{
                background: rgba(255, 255, 255, 0);  /* Invisible track */
            }}
            
            /* Firefox */
            * {{
                scrollbar-width: thin;  /* Set the width of the scrollbar */
                scrollbar-color: rgba(255, 255, 255, 0.9) rgba(255, 255, 255, 0); /* Thumb and track color */
            }}
            *:hover {{
                scrollbar-color: rgba(255, 255, 255, 0.7) rgba(255, 255, 255, 0); /* Darker thumb on hover */
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


# Apply the background styling
set_background_color(apply_background=True)

# Logo and Title section
if os.path.exists(LOGO_IMAGE_PATH):
    with open(LOGO_IMAGE_PATH, "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()

st.markdown(
    f"""
        <div style="text-align: center; padding: 20px;">
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

# Separation line
# st.markdown("___")

# File uploader section with centered instructions
# st.markdown(
#     """
#     <div style="text-align: center;">
#         <h4 style="color: #333333; font-size: 1.5rem;">📸 Upload the Image of Your Gemstone</h4>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

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
            # Display an error if no gemstones are detected
            st.error(error)

# Footer (hidden)
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
