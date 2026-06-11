import ollama

print("Starting...")

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Extract booking information from: My name is Nikisha and my email is test@gmail.com"
        }
    ]
)

print(response)