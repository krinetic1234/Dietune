import reflex as rx
import pandas as pd
import ast

# give recommendation foods (target protein, fat, carbs --> list of Recommendation)
class Recommendation(rx.Base):
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    error: float

#  load database + filter
def load_data(file_path, calories, protein, fat, carbs):
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
    df['error'] = None


    return give_recommendations(df, calories, protein, fat, carbs)

def give_recommendations(og_df, calories, protein=None, fat=None, carbs=None, error_percentage=1, df=None, prev_error_len=0):
    #recursion: make sure at least 5 values displayed
    if df is not None and len(df) >= 5:
        list_to_return = []
        errors = [i for i in list(og_df["error"]) if i is not None][:-1]
        df = df.reset_index()
        df.drop(columns=["index"], inplace=True)
        for index in range(len(df)):
            list_to_return.append(Recommendation(name=df.loc[index]['name'], 
                                                calories=round(df.loc[index]['calories'], 2),
                                                protein=round(df.loc[index]['protein'], 2),
                                                fat=round(df.loc[index]['fat'], 2),
                                                carbs=round(df.loc[index]['carbs'], 2),
                                                error=round(errors[index], 2)))
        return list_to_return[0:5]

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

    lower = prev_error_len
    upper = len(df)
    # print(error_percentage, lower, upper)
    og_df.loc[lower:upper, "error"] = error_percentage
    # print(list(og_df["error"]), len(list(og_df["error"])))

    return give_recommendations(og_df, calories, protein, fat, carbs, error_percentage, df, upper)

# print(give_recommendations(232, 18, 24, 34))