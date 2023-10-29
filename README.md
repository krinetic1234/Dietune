# Welcome to Dietune!

We provide personalized dietary recommendations for you based on your fitness goals. 

<img width="1382" alt="Screenshot 2023-10-29 at 12 20 05 PM" src="https://github.com/krinetic1234/Dietune/assets/56781484/e72a12b1-12eb-4da4-9f89-d9c9d1a685c4">

<h1>Inspiration</h1>
We have a friend who is obsessed with dietary fitness. Every time he goes shopping, he seemingly buys anything that says "low calorie" or "high protein" in an attempt to stay healthy, which does not seem efficient or cheap whatsoever. As a result, we had the thought of building this web app in order to give people ideas for meals/foods to eat to stay aligned with their goals without excessively over purchasing or eating foods that don't help them stay healthy.

<h1>What it does</h1>
Our web app allows a user to input health biometrics such as height, weight, age, and sex, and fitness/dietary goals, and will output an assortment of different food options per meal that suits their lifestyle. If a user is unsatisfied or does not have enough options, they can generate more options.

<h1>How we built it</h1>
To start, we built a classifier that classified specific rows of foods as Breakfast(1), Lunch(2), or Dinner(3) items. This classifier utilized a neural network, where for text data such as description, steps, ingredients, and tags, we utilized a TFI-df to convert into numeric values, and then ran this data through an LSTM, and for numeric data such as fat, saturated fat, and protein, we ran data through a simple RNN. In the end, we combined both models, and achieved ~80% accuracy. Next, utilizing this classifier, we classified the remaining rows of food in our dataset as breakfast, lunch, or dinner items. This modified dataset was sent into Reflex. These values, alongside user input values such as age, sex, height, etc, are analyzed, and used to filter foods in our reflex web app, allowing specific foods to be outputted as recommended meal options for breakfast, lunch, and dinner. Moreover, each of these foods have an error bound attached to them that we developed through a complex recursive algorithm, based on their deviance from the user's lifestyle choices. If not enough food values are generated per meal, we utilized Together AI's LLM to generate new foods based on name commonalities and our nutrition/user input metrics.

<h1>Challenges we ran into</h1>
One of the biggest challenges we ran into was optimizing our classifier. Our dataset did not come previously labeled with breakfast, lunch, and dinner categories, and thus we had to manually label a training set with these values and thus build our model on a very small dataset. As a result, the likelihood of reaching optimal accuracy was extremely low to start, so we had to employ several model optimization methods that took hours of our time to reach a decent accuracy. Another massive challenge we faced was designing our error bound's recursive algorithm. Both fatigue and visualization of the problem were huge challenges. In terms of visualization, finding an optimal error bound efficiently was extremely challenging, as we had to both keep track of previous error bounds, and increase the size of our food list simultaneously. Lastly, utilizing Reflex proved to be a big challenge. We would have to consistently use their base class, and found the organization of their platform a bit challenging to understand, making it very difficult for us to adeptly use the platform.

<h1>Accomplishments that we're proud of</h1>
One accomplishment we are very proud of was our recursive error bound algorithm. We found it to be a very creative and useful feature of our web app that helped differentiate us, and we are proud of its quick efficiency. Another accomplishment we are proud of is being able to effectively use Reflex. Eventually, once we understood Reflex's nuances, we found the data streaming and hosting process to be very seamless, making for a very nice web app.

<h1>What we learned</h1>
One thing that held us back was our lackluster planning. We seemed to change our course of action every hour due to platform limitations or new ideas, making it challenging to produce a cohesive product. Being formulaic and sticking to a cohesive plan would have led to more success.

<h1>What's next for Dietune</h1>
Ideally, we would like to increase our classifier's accuracy dramatically to provide better food recommendations. Additionally, we would like to potentially integrate further biometrics, such as body fat percentage, and health metrics such as sodium/sugar levels, so that our web app can be multi-faceted and utilized for a variety of purposes, from a person looking to get into shape, to a sick patient looking to improve their health. Moreover, we had the idea of potentially integrating the web app into a calendar-esque platform, where we had an algorithm that suggested meals for a person while also putting the meals at set times on the calendar based on the individual's circadian rhythm and meal down-times. Lastly, we would like to potentially acquire a better and more comprehensive food database to expand our reach to different types of cuisines.
