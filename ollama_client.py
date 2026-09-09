from ollama import chat

MODEL_NAME = "roxanne"

# -----------------------
# Roxanne Functions
# -----------------------

def send_msg(messages):
    """
    Send conversation history to Roxanne and return Roxanne's response
    """
    response = chat(
        model = MODEL_NAME,
        messages = messages
    )

    return response.message.content

def create_title(message):
    """
    Roxanne summarizes response to create title for user
    """

    sys_prompt = """Read the user's message and generate a short title that summarizes the topic. Only output the title. Do not include quotation marks."""
    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.message.content







# #Conversational Functions with Roxanne
# def send_message(message):
#     response = chat(
#         model = MODEL_NAME,
#         messages = [
#             {
#                 "role": "user",
#                 "content": message
#             }
#         ]
#     )

#     return response.message.content


# def send_message_stream(message):
#     response = chat(
#         model=MODEL_NAME,
#         messages=[
#             {
#                 "role": "user",
#                 "content": message,
#             }
#         ],
#         stream=True
#     )

#     return response


