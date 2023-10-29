import os
import together

# API key
together.api_key = os.environ['TOGETHER_API_KEY']

# Upload file
data_path = "Dietune/ml/foods.jsonl"
resp1 = together.Files.check(file=data_path)
resp2 = together.Files.upload(file=data_path)
file_id = "file-4f209c6c-1e17-48e2-ba56-692f8d9e2e56"

# Both open source model and fine-tuned model
m = "togethercomputer/llama-2-70b-chat"
m_finetune = "Krish/llama-2-7b-food-finetune-2023-10-28-04-59-52"

# Create a fine tuned instance
resp = together.Finetune.create(
  training_file = id,
  model = m,
  n_epochs = 3,
  n_checkpoints = 1,
  batch_size = 4,
  learning_rate = 1e-5,
  suffix = 'food-finetune',
  wandb_api_key = os.environ['WANDB_API_KEY']
)

fine_tune_id = resp['id']
print(fine_tune_id)

# Run the models
together.Models.start(m)
together.Models.start(m_finetune)

output = together.Complete.create(
  prompt = "Give me five breakast foods: ", 
  model = m_finetune
)

# Few shot learning
p = """
    Ensure the output has the same nutritional content as the input.

    input: 1. Lentil Breakfast Bowl, 2. Quinoa Breakfast Bowl
    output: 3. Potato Hash, 4. Kefir Smoothie, 5. Savory Oatmeal Bowl

    input: 1. Yogurt Almonds, 2. Spinach Eggs, 3. Banana Chia Oat, 4. PB Toast Strawberries
    output: 5. Avocado Muffin Eggs

    input: 1. Zucchini Noodles
    output: 2. Pork Lettuce Wraps, 3. Chorizo Burgers, 4. Chicken Fried Rice,  5. Greek Chicken Pasta

    input: 1. Garlic Soup, 2. Singaporian Noodles
    output: 3. Green Tea Noodles, 4. Coconut Fish Curry, 5. Salmon Bowl

    input: 1. BBQ Chicken Sandwich, 2. Roasted Veggie Bowl
    output:"""

output = together.Complete.create(
  prompt = p,
  model = m,
  max_tokens = 256,
  temperature = 0.4,
  top_k = 60,
  top_p = 0.6,
  repetition_penalty = 1.1,
  stop = ["input", "\n"]
)

print(output['output']['choices'][0]['text'])



