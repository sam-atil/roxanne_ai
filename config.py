from ollama import chat
from ollama import ChatResponse

stream = chat(model='gemma3:4b',
                             messages=[
                                 {
                                     "role": "user",
                                     "content": "How vast is your knowledge base?"
                                 }
                             ],
                             stream=True)

for chunk in stream:
    print(chunk.message.content, end='', flush=True)
