# Helper function

from helper_client_setup import client, model
from anthropic.types import Message

def add_user_message(messages,text):
    messages.append({
            "role": "user",
            "content": text.content if isinstance(text, Message) else text
        })

def add_assistant_message(messages,text):
    messages.append({
            "role": "assistant",
            "content": text.content if isinstance(text, Message) else text
        })

def chat(messages, system=None, temperature=0.0, stop_sequences=None):
    params = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    
    response = client.messages.create(**params)
    return response.content[0].text

# Get the response object back
def chat_response(messages, system=None, temperature=0.0, stop_sequences=None, tools=None):
    params = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": temperature
    }
    if tools:
        params["tools"] = tools
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    
    response = client.messages.create(**params)
    return response

def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])