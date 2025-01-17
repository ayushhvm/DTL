import pandas as pd

def analyze_ingredients(ingredient_text, skin_type, allergies):
    ingredients = ingredient_text.split("\n")
    analysis = []

    for ingredient in ingredients:
        risk = "Low"
        if any(allergy.strip().lower() in ingredient.lower() for allergy in allergies):
            risk = "High"
        analysis.append({"Ingredient": ingredient.strip(), "Risk Level": risk})

    return pd.DataFrame(analysis)
