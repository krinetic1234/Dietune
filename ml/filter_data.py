import reflex as rx
import pandas as pd
import ast

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

df['nutrition'] = df['nutrition'].apply(ast.literal_eval)

df['fat'] = [PDV_fat_g * (i[1]/100) for i in df['nutrition']]  
df['protein'] = [PDV_protein_g * (i[4]/100) for i in df['nutrition']] 
df['carbs'] = [PDV_carbs_g * (i[6]/100) for i in df['nutrition']] 
df['calories'] = [i[0] for i in df['nutrition']] 

# give recommendation foods (target protein, fat, carbs --> list of Recommendation)
class Recommendation(rx.Base):
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float

og_df = df

def give_recommendations(calories, protein=None, fat=None, carbs=None, error_percentage=1, df=None):
    #recursion: make sure at least 5 values displayed
    if df is not None and len(df) >= 5:
        print(df)
        return
    
    print(error_percentage)
    df = og_df
    # Create an empty list to store matching Recommendation objects
    df = df[(df['calories'] >= (calories - (calories * error_percentage / 100)))]
    df = df[(df['calories'] <= (calories + (calories * error_percentage / 100)))]
    
    if protein:
        error_percentage *= 1.1
        df = df[(df['protein'] >= (protein - (protein * error_percentage / 100)))]
        df = df[(df['protein'] <= (protein + (protein * error_percentage / 100)))]
    
    if fat:
        error_percentage *= 1.1
        df = df[(df['fat'] >= (fat - (fat * error_percentage / 100)))]
        df = df[(df['fat'] <= (fat + (fat * error_percentage / 100)))]

    if carbs:
        error_percentage *= 1.1
        df = df[(df['carbs'] >= (carbs - (carbs * error_percentage / 100)))]
        df = df[(df['carbs'] <= (carbs + (carbs * error_percentage / 100)))]

    give_recommendations(calories, protein, fat, carbs, error_percentage, df)
        
    
    
    # # Iterate through each row in the DataFrame
    # for _, row in df.iterrows():
    #     # Extract the nutrition values from the row
    #     row_fat = row['nutrition'][1]
    #     row_protein = row['nutrition'][4]
    #     row_carbs = row['nutrition'][6]
        
    #     # Calculate the allowable error based on the error percentage
    #     fat_error = fat * error_percentage / 100
    #     protein_error = protein * error_percentage / 100
    #     carbs_error = carbs * error_percentage / 100
        
    #     # Check if the nutrition values are within the specified range
    #     if (
    #         (fat - fat_error <= row_fat <= fat + fat_error) and
    #         (protein - protein_error <= row_protein <= protein + protein_error) and
    #         (carbs - carbs_error <= row_carbs <= carbs + carbs_error)
    #     ):
    #         # Create a Recommendation object and append it to the list
    #         recommendation = Recommendation(
    #             name=row['name'],
    #             protein=row_protein,
    #             fat=row_fat,
    #             carbs=row_carbs
    #         )
    #         recommendations.append(recommendation)
    
    # return recommendations

give_recommendations(1219, 64, 49, 85)
