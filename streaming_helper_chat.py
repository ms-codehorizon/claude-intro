# Helper function

from helper_client_setup import client, model

def add_user_message(messages,text):
    if isinstance(text, list):
        user_message = {
                "role": "user",
                "content": text
            }
    else:
        user_message = {
            "role": "user",
            "content": [{"type": "text", "text": text}]
        }
    messages.append(user_message)

def add_assistant_message(messages, text):
    if isinstance(text, list):
        assistant_message = {
            "role": "assistant",
            "content": text,
        }
    elif hasattr(text, "content"):
        content_list = []
        for block in text.content:
            if block.type == "text":
                content_list.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                content_list.append(
                    {
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    }
                )
        assistant_message = {
            "role": "assistant",
            "content": content_list,
        }
    else:
        # String messages need to be wrapped in a list with text block
        assistant_message = {
            "role": "assistant",
            "content": [{"type": "text", "text": text}],
        }
    messages.append(assistant_message)

def chat_stream(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    tool_choice=None,
    betas=[],
):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tool_choice:
        params["tool_choice"] = tool_choice

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    if betas:
        params["betas"] = betas

    return client.beta.messages.stream(**params)


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])