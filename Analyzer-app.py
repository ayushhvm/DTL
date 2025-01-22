import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from utils.analysis import analyze_ingredients
from utils.recommendations import get_recommendations

# Google Vision API details
API_KEY = "AIzaSyDav2dIn7bex9Cp9grQ-obeCHAJlvIv0bM"
VISION_API_URL = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

# Title of the App
st.title("DERMA CHECK - AI-Powered Skincare Assistant")

# Sidebar for User Profile
st.sidebar.header("User Profile")
skin_type = st.sidebar.selectbox("Skin Type", ["Normal", "Oily", "Dry", "Sensitive", "Combination"])
allergies = st.sidebar.text_area("Known Allergies (comma-separated):")

# Function to preprocess images
def preprocess_image(image_file):
    # Load image with OpenCV
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Increase contrast
    contrast = cv2.convertScaleAbs(gray, alpha=2, beta=0)
    # Perform thresholding
    _, thresholded = cv2.threshold(contrast, 120, 255, cv2.THRESH_BINARY)
    # Convert back to PIL format
    return Image.fromarray(thresholded)

# Function to call Google Vision API
def call_vision_api(image):
    # Convert PIL image to bytes
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    
    # Convert image to base64
    img_base64 = base64.b64encode(img_bytes).decode()
    
    # Prepare API payload
    request_payload = {
        "requests": [
            {
                "image": {"content": img_base64},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }
    
    # Send request to Vision API
    response = requests.post(VISION_API_URL, json=request_payload)
    return response.json()

# Main app functionality
uploaded_file = st.file_uploader("Upload a product label", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Label", use_container_width=True)
    
    # Preprocess the uploaded image
    preprocessed_img = preprocess_image(uploaded_file)
    st.image(preprocessed_img, caption="Preprocessed Image", use_container_width=True)
    
    # Call Vision API
    response = call_vision_api(preprocessed_img)
    
    if response.get("responses"):
        text_annotations = response["responses"][0].get("textAnnotations", [])
        if text_annotations:
            extracted_text = text_annotations[0]["description"]
            st.subheader("Extracted Ingredients")
            st.write(extracted_text)
            
            # Analyze Ingredients
            if st.button("Analyze Ingredients"):
                analysis = analyze_ingredients(extracted_text, skin_type, allergies.split(","))
                st.subheader("Analysis of Ingredients")
                st.dataframe(analysis)
        else:
            st.warning("No text detected in the uploaded image. Try preprocessing or using a different image.")
    else:
        st.error("Error in Vision API response. Check your API key and input.")

