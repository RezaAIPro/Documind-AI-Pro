import gradio as gr
import ollama
import logging

# Professional logging setup
logging.basicConfig(level=logging.INFO)

class GlobalAIApp:
 def init(self):
# Memory for the conversation
  self.history = []

def respond(self, user_input, chat_history, model_name):
"""
Handles the conversation logic with error handling.
"""
if not user_input:
 return "", chat_history
try:# 
Add user message to internal memory
self.history.append({"role": "user", "content": user_input})

# Call Ollama API with the selected model
response = ollama.chat(
model=model_name,
messages=self.history,
)

# Extract the response content
answer = response["message"]["content"]

# Add assistant response to memory to maintain context
self.history.append({"role": "assistant", "content": answer})

# Update UI chatbot component
chat_history.append((user_input, answer))

return "", chat_history

except Exception as e:
logging.error(f"Error: {e}")
error_msg = f"❌ Error: {str(e)}. Please ensure Ollama is running and the model '{model_name}' is installed."
chat_history.append((user_input, error_msg))
return "", chat_history

def reset_memory(self):
 """Clears the conversation history."""
self.history = []
return None

# Initialize the app logic
ai_app = GlobalAIApp()

# Design a Modern and Professional UI
with gr.Blocks(theme=gr.themes.Soft(), title="Global AI Assistant Pro") as demo:
 gr.Markdown(
"""
# 🚀 Global AI Assistant Pro
High-Performance Local LLM Interface | Powered by Ollama & Llama 3
---
### Instructions:

Make sure Ollama is installed and running on your machine.
Enter the model name (e.g., `llama3.2`, `mistral`, `phi3`) in the settings panel.
Start chatting!
"""
)

with gr.Row():
# Settings Panel
 with gr.Column(scale=1):
  gr.Markdown("### ⚙️ Configuration")
model_input = gr.Textbox(
value="llama3.2",
label="AI Model Name",
placeholder="e.g., llama3.2"
)
clear_btn = gr.Button("🗑️ Clear Chat History", variant="secondary")

# Chat Panel
with gr.Column(scale=4):
 chatbot = gr.Chatbot(height=550, show_label=False)
msg = gr.Textbox(
placeholder="Type your message here and press Enter...",
label="Your Message",
show_label=False
)

# Action Definitions
msg.submit(
ai_app.respond,
inputs=[msg, chatbot, model_input],
outputs=[msg, chatbot]
)

clear_btn.click(ai_app.reset_memory, outputs=None)

# Launch the application
if name == "main":
# server_name="0.0.0.0" allows access from other devices in the same network
 demo.launch(server_name="0.0.0.0", share=False)
```