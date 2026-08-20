# Helper function

from helper_client_setup import client, model
from anthropic.types import Message

def add_user_message(messages,text):
    messages.append({
            "role": "user",
            "content": text.content if isinstance(text, Message) else text
        })

def add_user_message_longhand(messages,text):
    messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text.content if isinstance(text, Message) else text,
                    "cache_control": {
                        "type": "ephemeral"
                    }
                }
            ]
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

def chat_thinking_response(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024,
):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if thinking:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message

def chat_thinking_response_caching(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024,
):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if thinking:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        }

    if tools:
        tools_with_cache = []
        for i, tool in enumerate(tools):
            tool_dict = dict(tool) if hasattr(tool, '__iter__') else tool
            if i == len(tools) - 1:
                tool_dict["cache_control"] = {"type": "ephemeral"}
            tools_with_cache.append(tool_dict)
        params["tools"] = tools_with_cache

    if system:
        params["system"] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {
                    "type": "ephemeral"
                }
            }
        ]

    message = client.messages.create(**params)
    return message

def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])