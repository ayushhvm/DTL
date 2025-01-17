import streamlit as st
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import pandas as pd
from utils.analysis import analyze_ingredients
from utils.recommendations import get_recommendations

st.title("DERMA CHECK - AI-Powered Skincare Assistant")

# Sidebar for User Profile
st.sidebar.header("User Profile")
skin_type = st.sidebar.selectbox("Skin Type", ["Normal", "Oily", "Dry", "Sensitive", "Combination"])
allergies = st.sidebar.text_area("Known Allergies (comma-separated):")

# Upload a Product Label
uploaded_file = st.file_uploader("Upload a product label", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Label", use_container_width=True)
    img = Image.open(uploaded_file)
    text = pytesseract.image_to_string(img)

    st.subheader("Extracted Ingredients")
    st.write(text)

    # Analyze Ingredients
    if st.button("Analyze Ingredients"):
        analysis = analyze_ingredients(text, skin_type, allergies.split(","))
        st.dataframe(analysis)

        # Display Recommendations
        st.subheader("Recommended Products")
        recommendations = get_recommendations(analysis)
        st.write(recommendations)
        
    
