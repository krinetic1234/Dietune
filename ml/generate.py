#===========STEP 3: FOOD RECS (GENERATE) ===========
import os
import together

together.api_key = os.environ['TOGETHER_API_KEY']

data_path = "Dietune/data/foods.jsonl"
# resp1 = together.Files.check(file=data_path)
# resp2 = together.Files.upload(file=data_path)

id = "file-902956ff-9c50-4788-aab2-8162e0ba7622"
model = "togethercomputer/llama-2-7b"

# resp = together.Finetune.create(
#   training_file = id,
#   model = model,
#   n_epochs = 3,
#   n_checkpoints = 1,
#   batch_size = 4,
#   learning_rate = 1e-5,
#   suffix = 'food-finetune',
#   wandb_api_key = os.environ['WANDB_API_KEY']
# )

# fine_tune_id = resp['id']

# print(together.Models.list())

together.Models.start("togethercomputer/llama-2-7b")
together.Models.start("Krish/llama-2-7b-food-finetune-2023-10-28-04-59-52")

# output = together.Complete.create(
#   prompt = "Isaac Asimov's Three Laws of Robotics are:\n\n1. ", 
#   model = "Krish/llama-2-7b-food-finetune-2023-10-28-04-59-52/ft-e2fae7c2-7fa5-41ac-8792-58252a5ad77c-2023-10-28-00-20-36", 
# )
