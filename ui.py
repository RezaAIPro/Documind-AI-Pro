import gradio as gr

from chat import ChatEngine
from memory import MemoryManager
from pdf_reader import PDFReader
from search import SearchEngine
from config import *


chat_engine = ChatEngine()
memory = MemoryManager()
pdf_reader = PDFReader()
search_engine = SearchEngine()
pdf_text = ""

chat_engine.history = memory.load()

def chat(message, history, model, language):
    print("chat function called")
    global pdf_text

    final_message = message

    if pdf_text:

        context = search_engine.search(
            pdf_text,
            message
        )

        final_message = f"""
Use ONLY the following context to answer.

Context:

{context}

Question:

{message}

If the answer is not found in the context,
say that the document does not contain enough information.
"""

    answer = chat_engine.chat(final_message, model, language)

    history.append({
        "role": "user",
        "content": message
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    memory.save(chat_engine.history)

    return "", history

def upload_pdf(file):
    global pdf_text

    if file is None:
        return "❌ No PDF selected"

    try:
        pdf_info = pdf_reader.read_pdf(file.name)

        pdf_text = pdf_info["text"]

        return f"""
✅ PDF Loaded Successfully

📄 File:
{pdf_info['name']}

📑 Pages:
{pdf_info['pages']}

📝 Words:
{pdf_info['words']}

💾 Size:
{pdf_info['size']} KB
"""

    except Exception as e:
        return f"❌ Error:\n{e}"

def clear_chat():
    global pdf_text

    pdf_text = ""

    chat_engine.clear()
    memory.clear()

    return []


with gr.Blocks(
    theme=gr.themes.Soft(),
    title=APP_TITLE,
    css="style.css"
) as demo:
    gr.Markdown("""
# 🧠 Documind AI Pro

### 📚 Local AI Assistant with Memory & PDF Chat

👤 **Memory:** Active  
🤖 **Default Model:** Gemma2
""")

    gr.Markdown(WELCOME_MESSAGE)

    with gr.Row():

       with gr.Column(scale=1):

        model = gr.Dropdown(
        choices=[
            "gemma2",
            "llama3.1",
            "mistral",
            "phi3"
        ],
        value="gemma2",
        label="AI Model"
    )

        language = gr.Dropdown(
        choices=LANGUAGES,
        value=DEFAULT_LANGUAGE,
        label="🌍 Language"
    )

        pdf_file = gr.File(
        label="📄 Upload PDF",
        file_types=[".pdf"]
            )

        pdf_status = gr.Textbox(
                label="PDF Status",
                interactive=False
            )
        clear = gr.Button(
             "🗑️ Clear Chat",
            variant="stop"
            )


        with gr.Column(scale=4):

           chatbot = gr.Chatbot(
            height=650,
            show_label=False,
                )
           
        msg = gr.Textbox(
    placeholder="💬 سوالت را بنویس و Enter بزن...",
    label="Chat",
    lines=1
)
   


    pdf_file.change(
        upload_pdf,
        inputs=pdf_file,
        outputs=pdf_status
    )


    msg.submit(
        chat,
     inputs=[
    msg,
    chatbot,
    model,
    language
] ,
        outputs=[
            msg,
            chatbot
        ]
    )


    clear.click(
        clear_chat,
        outputs=chatbot
    )


if __name__ == "__main__":
    demo.launch()