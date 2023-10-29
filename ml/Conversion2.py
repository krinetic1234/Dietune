#===========STEP 0: BASIC INPUTS===========

# mapping
sex_mapping = {
    "M": 1,
    "F": 0
}

fitness_goal_mapping = {
    "Fat Loss": 1,
    "Maintenance": 2,
    "Muscle Gain": 3
}

# change this mapping into something more meaningful
activity_mapping = {
    "None: Desk Job etc.": 0,
    "Light: sitting, standing, etc. ": 1,
    "Moderate: Lifting, continuous activity, etc. ": 2,
    "Cardio/Sports: couple hours a day": 3,
    "Heavy: very strenuous exercise daily": 4
}

diet_mapping = {
    "Low-Fat": 1,
    "Low-Carb": 2,
    "Ketogenic (High Fat)": 3
}

sodium_mapping = {
    "Low": 0,
    "High": 1
}
    
chronotype_mapping = {
    "Night Owl": 0,
    "Morning Lark": 1
}


# inputs
age = float(input("Enter your age: "))
sex = input("Enter your sex (M/F): ")
weight = float(input("Enter your weight (pounds): "))
height = float(input("Enter your height (inches): "))
fitness_goal = input("Enter your fitness goal: ")
activity_goal = input("Describe your typical activity level: ")
diet_goal = input("What are your dietary preferences:")

optional = input("Have you done a basic metabolic panel recently and would like to share your info for more detailed results? (Y/N) ")

if (optional == "Y"):

    fasting_glucose = float(input("Enter your fasting glucose (mg/dl) or 100000 if you don't have it: "))
    calcium = float(input("Enter your Calcium levels(mg/dl) or 100000 if you don't have it: "))
    Bicarbonate = float(input("Enter your Bicarbonate levels: "))
    Chloride = float(input("Enter your Chloride levels (mEq/L) or 100000 if you don't have it: "))
    Magnesium = float(input("Enter your Magnesium levels(mg/dl) or 100000 if you don't have it: "))
    Phosphorus = float(input("Enter your Phosphorus levels(mg/dl) or 100000 if you don't have it: "))
    Potassim = float(input("Enter your Potassium levels (mEq/L) or 100000 if you don't have it: "))
    Sodium = float(input("Enter your Sodium levels (mEq/L) or 100000 if you don't have it: "))
    BUN = float(input("Enter your Blood Urea Nitrogen levels(mg/dl) or 100000 if you don't have it: "))
    Creatinine = float(input("Enter your Creatinine levels(mg/dl) or 100000 if you don't have it: "))

    thyroid_level = float(input("Enter your TSH levels (mU/L): "))


vegetarian = input("Are you vegetarian (Y/N): ")
meal_count = float(input("How many meals do you eat in a single day?: "))

chronotype = 

under = 0
over = 0
#ok so low glucose means faster metabolism
if (fasting_glucose < 70):
    under += 1
elif (fasting_glucose > 99):
    over += 1
# if (calcium < 8.5):
#     under += 1
# elif(calcium > 10.2):
#     over += 1
if (Bicarbonate < 18):
    over += 1
elif (Bicarbonate > 30):
    under += 1
if (Chloride < 98):
    under += 1
elif (Chloride > 106):
    over += 1
if (Phosphorus < 3):
    under += 1
elif (Phosphorus > 4.5):
    over += 1
if (Magnesium < 1.8):
    under += 1
elif (Magnesium > 3.6):
    over += 1
if (Potassim < 3.5):
    under += 1
elif (Potassim > 5.5):
    over += 1
if (Sodium < 135):
    under += 1
elif (Sodium > 147):
    over += 1
if (BUN < 6):
    under += 1
elif (BUN > 20):
    over += 1
if (Creatinine < 0.7 and sex == 1) or (Creatinine < 0.6 and sex == 0):
    under += 1
elif (Creatinine > 1.3 and sex == 1) or (Creatinine < 1.1 and sex ==0):
    over += 1

if (thyroid_level < 0.4):
    under += 5
    sodium = 1
elif (thyroid_level > 4.0 and sex == 1) or (thyroid_level < 2.5 and sex == 0):
    over += 5
    sodium = 0



# # ==== DEFAULT VALUES ====
# age = 18
# sex = "M"
# weight = 160
# height = 71
# fitness_goal = "Fat Loss"
# activity_goal = "Sports"

# adjust input values
weight_kg = weight * 0.45359237 # kg/lb factor
height *= 2.54 # cm/in factor
sex = sex_mapping[sex]
fitness_goal = fitness_goal_mapping[fitness_goal]
activity_goal = activity_mapping[activity_goal]
diet_goal = diet_mapping[diet_goal]

#===========STEP 1: CALORIE INTAKE===========

cal_difference = 0
cal_intake = 0
cal_burnt = 0
maintenance_cal = 0
excercise_cal = 0

cal_difference = 500 * (fitness_goal-2) 

if sex == 1:
    maintenance_cal = 10 * weight + 6.25 * height - 5 * age + 5
else:
    maintenance_cal = 10 * weight + 6.25 * height - 5 * age - 161 

if (optional == "Y"):
    maintenance_cal *= 1 + (over - under) / 9

# temporary calculation (use AI to figure how much they burnt from their activity description)
cal_burnt = 250 * activity_goal

cal_intake = int(cal_difference + cal_burnt + maintenance_cal)
print(f"Cal Intake: {cal_intake}")

#===========STEP 2: MACROS AMOUNT===========

# these ratios are grams/pound and they're based on studies available online
# need to adjust some of these values further
protein_ratio = (1 + 0.2 * (fitness_goal-2))
fat_ratio = 0.25 * (diet_goal) + 0.1 * (fitness_goal-2)

# if (fitness_goal = 3):
#     protein_ratio = 1 + 0.35 * (cal_intake)
#     fat_ratio = 0.3 + 0.1 * (fitness_goal-2)
# if (fitness_goal = 1):
#     protein_ratio = 1 + 0.35 * (cal_intake)
#     fat_ratio = 0.3 + 0.1 * (fitness_goal-2)
    

protein_cal_g = 4
carbs_cal_g = 4
fat_cal_g = 9 

protein = int(weight * protein_ratio)
fat = int(weight * fat_ratio)
carbs = int((cal_intake - (protein_cal_g * protein + fat_cal_g * fat)) / carbs_cal_g)
print(f"Protein (g): {protein}\nCarbs (g): {carbs}\nFat (g): {fat}")
if sodium == 0 : 
    sodium_sort = "low-sodium content"
else:
    sodium_sort = "high-sodium content"
print(f"As your Thyroid levels indicate, your preferences are sorted based on having {sodium_sort} .")

