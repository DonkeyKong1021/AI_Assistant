from transformers import AutoModelForCausalLM, Conversation, AutoTokenizer
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

model_id = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.padding_side = 'left'
model = AutoModelForCausalLM.from_pretrained(model_id)

def process_command(text):
    conversation = Conversation(text)
    response = model(conversation, pad_token_id=tokenizer.eos_token_id)
    return response.generated_responses[-1]