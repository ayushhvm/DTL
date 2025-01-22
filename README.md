
# DermaCheck (DTL)

This repository hosts the **Skincare Recommendation Engine**, an application designed to help users discover the best skincare products tailored to their needs. Using data-driven insights, the system evaluates product ingredients and matches them to user preferences and skincare goals.

## Features

- **Personalized Recommendations**: Suggests skincare products based on ingredient analysis.
- **Ingredient Matrix**: Evaluates and matches ingredients to user requirements.
- **Data Insights**: Leverages a dataset of skincare products for recommendations.
- **Web Application Interface**: Provides a user-friendly interface for seamless interaction.

## Ingredients Insights
<img width="960" alt="{AEE646E8-4C3A-4EB2-94AE-6032A738C058}" src="https://github.com/user-attachments/assets/9b34aa7c-84ea-4817-b92e-d14de0031f77" />

## Skincare Recommendations
<img width="959" alt="{9EB683A6-EB99-40EB-A0FB-F2E02B1A187C}" src="https://github.com/user-attachments/assets/818a35f5-6a67-45af-9d12-19b743b81cf7" />

<img width="959" alt="{FC5DFF8E-A46C-4879-8B6C-11CA66DD97C3}" src="https://github.com/user-attachments/assets/aa2721b9-7867-4b26-9104-3bd65fdebd95" />

## Project Files

- **`skincare-recommendation-engine.ipynb`**: The core logic and implementation of the recommendation system.
- **Data Files**:
  - `data.pkl`: Processed data used by the recommendation engine.
  - `ingred_matrix.pkl`: Ingredient mapping for product recommendations.
  - `skincare_products_clean.csv`: Cleaned dataset of skincare products.
- **`App.py`**: Web application interface for user interaction.
- **`requirements.txt`**: Python dependencies required to run the project.

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/ayushhvm/DTL.git
   cd DTL
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the application:
   ```bash
   streamlit run App.py
   ```
4. Access the app at `http://localhost:5000` (default).

## Dataset Overview

The dataset contains detailed information on skincare products, including:
- Product names
- Ingredient lists
- Categories and types
- Other relevant attributes

## How It Works

1. **Ingredient Analysis**: The system evaluates product ingredients for compatibility.
2. **Recommendations**: Displays a curated list of recommended products.

## Future Enhancements

- Improved ingredient filtering for sensitive skin.
- Expanded dataset with user reviews and ratings.
- Integration with popular e-commerce platforms for seamless product purchases.

 
