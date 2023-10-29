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
    "None": 0,
    "Lifting": 1,
    "Cardio": 2,
    "Sports": 3,
    "Everything": 4,
}

# inputs
age = float(input("Enter your age: "))
sex = input("Enter your sex (M/F): ")
weight = float(input("Enter your weight (pounds): "))
height = float(input("Enter your height (inches): "))
fitness_goal = input("Enter your fitness goal: ")
activity_goal = input("Describe your typical activity level: ")

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

# temporary calculation (use AI to figure how much they burnt from their activity description)
cal_burnt = 250 * activity_goal

cal_intake = int(cal_difference + cal_burnt + maintenance_cal)
print(f"Cal Intake: {cal_intake}")

#===========STEP 2: MACROS AMOUNT===========

# these ratios are grams/pound and they're based on studies available online
# need to adjust some of these values further
protein_ratio = 1 + 0.2 * (fitness_goal-2)
fat_ratio = 0.3 + 0.1 * (fitness_goal-2)

protein_cal_g = 4
carbs_cal_g = 4
fat_cal_g = 9 

protein = int(weight * protein_ratio)
fat = int(weight * fat_ratio)
carbs = int((cal_intake - (protein_cal_g * protein + fat_cal_g * fat)) / carbs_cal_g)
print(f"Protein (g): {protein}\nCarbs (g): {carbs}\nFat (g): {fat}")


