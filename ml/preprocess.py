import json
import pandas as pd

# Read CSV
columns = ['product_name', 'quantity', 'ingredients_text', 'allergens', 'traces_en', 'serving_size', 'additives_en', 'main_category_en', 'image_url', 'energy_100g', 'fat_100g', 'saturated-fat_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'proteins_100g', 'sodium_100g', 'calcium_100g', 'iron_100g']
df = pd.read_csv("Dietune/data/foods_modified.csv")

# Create JSON file from selected available data
column_name = 'ingredients_text'
ingredients = df[column_name].dropna().tolist()
json_file_path = 'Dietune/data/foods.jsonl'

# Format non-NaN values as a JSONL file
with open(json_file_path, 'w') as jsonl_file:
    for value in ingredients:
        json.dump({"text": value}, jsonl_file)
        jsonl_file.write('\n')
