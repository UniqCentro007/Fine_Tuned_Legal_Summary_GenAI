# model_loader.py

import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel

MODEL_NAME = "distilgpt2"
MODEL_PATH = "saved_legal_model"

print("Checking model path...", MODEL_PATH)
model_exists = os.path.isdir(MODEL_PATH) and os.path.exists(MODEL_PATH)

print("Loading tokenizer from base model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

if model_exists:
    print("Loading base model and LoRA adapter...")
    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model = PeftModel.from_pretrained(base_model, MODEL_PATH)
    print("Loaded LoRA adapter from saved_legal_model.")
else:
    print("Saved legal model not found. Loading base model only.")
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

summarizer = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=250,
    do_sample=False,
)

print("✅ Model ready!")

def generate_summary(text):
    prompt = f"Summarize the legal text below:\n\n{text}\n\nSummary:"
    result = summarizer(prompt)[0]["generated_text"]
    return result.strip()