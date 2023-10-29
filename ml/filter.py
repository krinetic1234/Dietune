import reflex as rx
import pandas as pd

file_path = "/Users/jaibhatia/Desktop/converted_word_lists.csv"

#  load database + filter
df = pd.read_csv(file_path)[['name', 'nutrition']]
# name                                     nutrition
# crab filled crescent snacks          [69.2, 3.0, 9.0, 6.0, 5.0, 4.0, 3.0]
# Nutrition information (calories (#), total fat (PDV), sugar (PDV) , sodium (PDV) , protein (PDV) , saturated fat (PDV) , and carbohydrate (PDV)


# convert PDV -> grams (source: https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels)
PDV_protein_g = 50
PDV_fat_g = 78
PDV_carbs_g = 275

for _, row in df.iterrows():
    eval(row['nutrition'])[1] *= PDV_fat_g
    eval(row['nutrition'])[4] *= PDV_protein_g
    eval(row['nutrition'])[6] *= PDV_carbs_g

# give recommendation foods (target protein, fat, carbs --> list of Recommendation)
class Recommendation(rx.Base):
    name: str
    protein: float
    fat: float
    carbs: float

def give_recommendations(df, protein, fat, carbs, error_percentage):
    # Create an empty list to store matching Recommendation objects
    recommendations = []
    
    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        # Extract the nutrition values from the row
        row_fat = row['nutrition'][1]
        row_protein = row['nutrition'][4]
        row_carbs = row['nutrition'][6]
        
        # Calculate the allowable error based on the error percentage
        fat_error = fat * error_percentage / 100
        protein_error = protein * error_percentage / 100
        carbs_error = carbs * error_percentage / 100
        
        # Check if the nutrition values are within the specified range
        if (
            (fat - fat_error <= row_fat <= fat + fat_error) and
            (protein - protein_error <= row_protein <= protein + protein_error) and
            (carbs - carbs_error <= row_carbs <= carbs + carbs_error)
        ):
            # Create a Recommendation object and append it to the list
            recommendation = Recommendation(
                name=row['name'],
                protein=row_protein,
                fat=row_fat,
                carbs=row_carbs
            )
            recommendations.append(recommendation)
    
    return recommendations
