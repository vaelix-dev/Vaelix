import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Load model on startup
print("Loading Model...")
model_name = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    torch_dtype="auto", 
    device_map="cpu" # Use CPU for free tier
)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
print("Model Loaded.")

def chat(message, history):
    if not message:
        return ""
    
    messages = [{"role": "user", "content": message}]
    text = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = pipe.tokenizer(text, return_tensors="pt")
    
    outputs = pipe.model.generate(**inputs, max_new_tokens=200, temperature=0.7, do_sample=True)
    output_text = pipe.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    
    return output_text

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Vaelix Core (Server)")
    chatbot = gr.Chatbot(label="Vaelix Brain")
    with gr.Row():
        msg = gr.Textbox(placeholder="Ask me anything...", scale=4)
        btn = gr.Button("Send", variant="primary", scale=1)
    
    msg.submit(chat_fn=lambda m, h: chat(m, h), inputs=[msg, chatbot], outputs=[chatbot])
    btn.click(chat_fn=lambda m, h: chat(m, h), inputs=[msg, chatbot], outputs=[chatbot])

demo.launch(server_name="0.0.0.0", server_port=8000)
