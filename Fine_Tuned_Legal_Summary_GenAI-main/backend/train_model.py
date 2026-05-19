# train_model.py

import os
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
)

from peft import get_peft_model, LoraConfig
from huggingface_hub import login

from dotenv import load_dotenv
load_dotenv(".env.local")

HF_TOKEN = os.getenv("HF_TOKEN")

login(HF_TOKEN)

MODEL_NAME = "distilgpt2"
SAVE_PATH = "saved_legal_model"

print("Loading dataset...")
ds = load_dataset("ChicagoHAI/CaseSumm")

print("Columns:", ds["train"].column_names)

# ✅ tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# ✅ preprocess
def preprocess(example):
    prompt = f"""
### Instruction:
Summarize the legal document.

### Input:
{example["opinion"]}

### Response:
{example["syllabus"]}
"""

    tokens = tokenizer(
        prompt,
        truncation=True,
        max_length=512,
        padding="max_length"
    )

    # 🔥 MUST exist
    tokens["labels"] = tokens["input_ids"]

    return tokens

# small dataset (safe)
train_ds = ds["train"].select(range(100)).map(preprocess)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="cpu"
)

# ✅ LoRA config (correct)
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# training args
training_args = TrainingArguments(
    output_dir=SAVE_PATH,
    per_device_train_batch_size=1,
    num_train_epochs=1,
    logging_steps=10,
    save_strategy="steps",
    save_steps=10,
    remove_unused_columns=False   
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds
)

print("Training started...")
trainer.train()

print("Saving model...")
model.save_pretrained(SAVE_PATH)
tokenizer.save_pretrained(SAVE_PATH)

print("✅ Training completed!")