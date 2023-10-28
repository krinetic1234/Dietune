#===========STEP 3: FOOD RECS (FILTER) ===========
import pandas as pd

file_path = "data/foods.csv"
df = pd.read_csv(file_path)

default_values = {
    "quantity": 0,  # Default value for numeric columns
    "serving_size": 0,  # Default value for numeric columns
    "ingredients_text": "N/A",  # Default value for string columns
    "allergens": "N/A",  # Default value for string columns
    "traces_en": "N/A",  # Default value for string columns
    "additives_en": "N/A",  # Default value for string columns
    "main_category_en": "N/A",  # Default value for string columns
    "energy_100g": 0,  # Default value for numeric columns
    "fat_100g": 0,  # Default value for numeric columns
    "cholesterol_100g": 0,  # Default value for numeric columns
    "carbohydrates_100g": 0,  # Default value for numeric columns
    "sugars_100g": 0,  # Default value for numeric columns
    "fiber_100g": 0,  # Default value for numeric columns
    "proteins_100g": 0,  # Default value for numeric columns
    "sodium_100g": 0,  # Default value for numeric columns
    "calcium_100g": 0,  # Default value for numeric columns
    "iron_100g": 0,  # Default value for numeric columns
}

# using provided info about macros

# based on user input
user_input = {
    "proteins_100g": 50,
    "sugars_100g": 5,
}

mask = pd.Series(True, index=df.index)
for column, value in user_input.items():
    if column in default_values:
        threshold = value if value is not None else default_values[column]
        if column in df:
            column_values = df[column].apply(lambda x: float(x) if x != "N/A" else default_values[column])
            mask &= (column_values >= threshold)
filtered_df = df[mask]

items = {}
limit = 4

for i, row in filtered_df.iterrows():
    items[row['product_name']] = Item(**row.to_dict())