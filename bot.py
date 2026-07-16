import ollama

response = ollama.chat(
model="llama3.1",
messages=[
{
"role": "user",
"content": "hello, introduce yourself briefly"
}
]
)

print(response["message"]["content"])