import streamlit as st
import requests
import os
import base64
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]
SPACE_GEM_URL = "https://spacegem-223626310523.europe-west1.run.app/predict/"


def detect_gemstones(image_bytes):
    """
    Sends the image to our API for gemstone detection and classification.
    Returns predictions and an error message (if any).
    """
    response = requests.post(
        SPACE_GEM_URL,
        files={"file": image_bytes},
    )

    if response.status_code != 200:
        return None, "❌ Error: Unable to process image."

    result = response.json()

    # Handle single gemstone response (string format)
    if isinstance(result, str):
        return [result], None  # Return the gemstone name as a list

    # Handle multiple gemstone response
    if isinstance(result, dict):
        gemstones = {gem: count for gem, count in result.items() if count > 0}
        if gemstones:
            return gemstones, None

    return None, "⚠️ No gemstone detected in the image."


# Set Streamlit page configuration
st.set_page_config(
    page_title="Space Gem",
    page_icon="💎",
    layout="wide",
)

# Paths to images inside the 'images' folder
BACKGROUND_IMAGE_PATH = "images/background.png"
LOGO_IMAGE_PATH = "images/logo.png"


# @st.cache_resource
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
                padding-top: 5vh;
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
set_background_color(apply_background=False)

# Logo and Title section
if os.path.exists(LOGO_IMAGE_PATH):
    with open(LOGO_IMAGE_PATH, "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()

st.markdown(
    f"""
        <div style="text-align: center; padding: 20px;">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo Space Gem" width="250" style="border-radius: 4%; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
        </div>
        <div style="text-align: center; padding-top: 20px;">
            <h4 style="font-size: 1.5rem; ">Identify Your Gemstone</h4>
        </div>
        <div style="text-align: center;">
            <h4 style="font-size: 1.5rem;">📸 Upload the Image of Your Gemstone</h4>
        </div>
        """,
    unsafe_allow_html=True,
)


def ask_gem_AI(prediction):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert gemologist.
                I will send you a list of gem names and capitalize the first letter of the gemstone.
                Respond in a user-friendly manner.
                Open with the sentense: Congratulations on finding
                if it's only one gemstone then
                if the name of the gemstone starts with a consonant use the article a
                if the name of the gemstone starts with a vowel use the article an

                if it's a list of gemstones then open with the sentence Congratulations on finding: list_of_gemstones in bold

                AND give the following information for each gem on the list and keep the format below AND in a markdown format:
                An explanation of a maximum 50 words about the stone
                How rare is the gem?
                Where in the world can these be found
                Price range in euros in numbers with the euros sign €
                A short explanation of how to preserve it""",
            },
            {"role": "user", "content": prediction},
        ],
        temperature=0,  # Ensures deterministic responses
    )
    # Return the AI response
    return response["choices"][0]["message"]["content"]


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
            prediction, error = detect_gemstones(img_bytes)

        if prediction:
            # Check if the prediction is a single gemstone or multiple gemstones
            if isinstance(prediction, list):  # Single gemstone
                gemstone_name = prediction[0]

                # st.markdown(f"💎**Gemstone:** {gemstone_name}")
                st.markdown(f"### 💎 Gemstone Detected: {gemstone_name}")
                with st.spinner("✨ Generating Gemstone Details..."):
                    output = ask_gem_AI(gemstone_name)
                    # st.markdown(output)

                    # Use Streamlit columns to display content side by side
                    col1, col2 = st.columns(
                        [1, 1]
                    )  # Adjust column width ratios as needed

                    with col1:
                        st.markdown(
                            """
                        <style>
                        /* Flex container for the image and text */
                        .responsive-container {
                            display: flex;
                            flex-wrap: wrap; /* Allows wrapping for smaller screens */
                            justify-content: center;
                            align-items: center;
                            gap: 20px; /* Adds space between the image and text */
                        }

                        /* Styling for the processed image */
                        .processed-image {
                            max-width: 100%; /* Ensure it scales within its container */
                            width: 300px; /* Set a default width */
                            height: auto; /* Maintain aspect ratio */
                            border-radius: 12px;
                            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
                        }

                        /* Responsive rules for smaller screens */
                        @media (max-width: 768px) {
                            .responsive-container {
                                flex-direction: column; /* Stack items vertically */
                            }
                            .processed-image {
                                width: 80%; /* Adjust the image width for small screens */
                            }
                        }
                        </style>
                        """,
                            unsafe_allow_html=True,
                        )

                        # Display the processed image
                        st.markdown(
                            f"""
                            <div style="text-align: center; padding-top: 6vh;" class="responsive-container">
                                <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" class="processed-image" alt="Processed Gemstone Image">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col2:
                        # Display the AI output
                        st.markdown(output)

            elif isinstance(prediction, dict):  # Multiple gemstones
                st.markdown("### 💎 List of Gemstones Detected:")
                gemstone_list = ", ".join(
                    f"{gem} (x{count})" for gem, count in prediction.items()
                )
                # st.markdown(f"**Gemstones:** {gemstone_list}")
                st.markdown(f"### ✨{gemstone_list}")

                with st.spinner("✨ Generating Gemstone Details..."):
                    gemstone_names = ", ".join(prediction.keys())
                    output = ask_gem_AI(gemstone_names)
                    # st.markdown(output)

                    # Use Streamlit columns to display content side by side
                    col1, col2 = st.columns(
                        [1, 1]
                    )  # Adjust column width ratios as needed

                    with col1:
                        st.markdown(
                            """
                        <style>
                        /* Flex container for the image and text */
                        .responsive-container {
                            display: flex;
                            flex-wrap: wrap; /* Allows wrapping for smaller screens */
                            justify-content: center;
                            align-items: center;
                            gap: 20px; /* Adds space between the image and text */
                        }

                        /* Styling for the processed image */
                        .processed-image {
                            max-width: 100%; /* Ensure it scales within its container */
                            width: 300px; /* Set a default width */
                            height: auto; /* Maintain aspect ratio */
                            border-radius: 12px;
                            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
                        }

                        /* Responsive rules for smaller screens */
                        @media (max-width: 768px) {
                            .responsive-container {
                                flex-direction: column; /* Stack items vertically */
                            }
                            .processed-image {
                                width: 80%; /* Adjust the image width for small screens */
                            }
                        }
                        </style>
                        """,
                            unsafe_allow_html=True,
                        )

                        # Display the processed image
                        st.markdown(
                            f"""
                            <div style="text-align: center; padding-top: 6vh;" class="responsive-container">
                                <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" class="processed-image" alt="Processed Gemstone Image">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col2:
                        # Display the AI output
                        st.markdown(output)

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
