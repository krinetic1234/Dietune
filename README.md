# Welcome to Dietune!

We provide personalized dietary recommendations for you based on your fitness goals. 

========INPUTS========

[1] Background information
    [-] Age
    [-] Sex
    [-] Weight
    [-] Height
[2] Fitness goal
    [-] Fat Loss
    [-] Maintenance
    [-] Muscle Gain
[3] Usual Activity level
    [-] Sedentary: little or no exercise
    [-] Exercise 1-3 times/week
    [-] Exercise 4-5 times/week
    [-] Daily exercise or intense exercise 3-4 times/week
    [-] Intense exercise 6-7 times/week
    [-] Very intense exercise daily, or physical job

========OUTPUT========

[1] Calorie Intake
    [-] Use Mifflin-St Jeor formula to calculate maintenance calories
    [-] Add their calories burnt from 
[2] Daily Macros Suggestions (allow the user to alter these amounts)
    [-] Protein
    [-] Carbs
    [-] Fat
[3] Food Recommendations 
    [-] Filter from database (based on macros specifications)
    [-] Add additional food recs (use AI)
[4] Daily Meal Plan
    [-] Classify the food recommendations into (breakfast, lunch, dinner, snacks, sweets)
    [-] Pad/truncate each category to have exactly 3 diverse options (use AI)

========RELEVANT INFO========

Minimum protein level is 0.7 g/kg
“Active individuals” should shoot for is 1.2 to 1.7 g/kg
3500 calories deficit = 1 pound of fat

========ADDITIONAL FEATURES========

[-] teach an AI to map any user input value to a certain category (e.g. activity level, fitness goal, etc.)
[-] provide additional food recs based on what other users have purchased
[-] marketplace for individuals to buy those types of foods from the app itself