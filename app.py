import streamlit as st
import requests
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()
url = os.getenv("API_URL", "http://localhost:8501")  # Default fallback

# Set Streamlit page configuration
st.set_page_config(
    page_title="Space Gem",
    page_icon="💎",
    layout="wide",
)

# Paths to images inside the 'images' folder
BACKGROUND_IMAGE_PATH = "images/background.png"  # Space background image
LOGO_IMAGE_PATH = "images/logo.png"  # Logo of the app


# Function to apply space and gemstone background color and responsive styling
def set_background_color(apply_background=True):
    if apply_background:
        # Read and encode the space background image to base64_image
        with open(BACKGROUND_IMAGE_PATH, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode()

        # Inject the base64 string into the CSS for the background
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('data:image/jpeg;base64,{image_base64}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: white;
                height: 100vh;
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
                # overflow-x: hidden; /* prevent horizontal scroll */
                # overflow-y: auto; /* prevent vertical scroll */
            }}
            h1, h4, p {{
                text-align: center;
                font-family: 'Arial', sans-serif;
            }}
            .uploaded-image {{
                margin: 0 auto;
                display: block;
                max-width: 80%;
                height: auto;
                border-radius: 12px;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
            }}
            /* Styling for gemstone inspired buttons */
            .stButton>button {{
                background-color: #4e73df; /* Sapphire Blue */
                border-radius: 50px;
                color: white;
                font-weight: bold;
                padding: 10px 30px;
                transition: all 0.3s ease;
            }}
            .stButton>button:hover {{
                background-color: #2e59a3; /* Darker Sapphire Blue on hover */
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


# Apply space and gemstone-inspired background and colors
set_background_color(apply_background=True)

# Logo and Title Section
if os.path.exists(LOGO_IMAGE_PATH):
    with open(LOGO_IMAGE_PATH, "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()

    st.markdown(
        f"""
            <div style="text-align: center; padding: 20px;">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo Space Gem" width="200">
            </div>
            <div style="text-align: center; padding-top: 20px;">
                <h1 style="color: #333333; font-size: 3rem; margin: 10px;">Space Gem 💎</h1>
                <p style="color: #555555; font-size: 1.2rem;">Identify Your Precious Gemstone</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

# separation line
st.markdown("___")

# Separation line with cosmic sparkle
st.markdown(
    """
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

# Handle file upload and show result
if img_file_buffer is not None:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Analyzing the gemstone
        with st.spinner("✨ Analyzing the gemstone..."):
            img_bytes = img_file_buffer.getvalue()
            res = requests.post(url + "/upload_image", files={"img": img_bytes})

            # Show results
            if res.status_code == 200:
                st.image(
                    res.content,
                    caption="🔍 Identified Gemstone",
                    use_column_width=True,
                )
            else:
                st.markdown(
                    """
                        <div style="text-align: center;">
                            <p style="color: red; font-size: 1rem;">Oops! Something went wrong. Try again.</p>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Show uploaded image with styling
        st.markdown(
            """
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{base64_image}" alt="Uploaded Image" class="uploaded-image" />
                    <p style="color: #333333; font-size: 1rem; margin-top: 10px;">Uploaded Image ☝️</p>
                </div>
            """.format(
                base64_image=base64.b64encode(img_file_buffer.read()).decode()
            ),
            unsafe_allow_html=True,
        )

# Footer (hidden)
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
