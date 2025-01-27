from config import CONFIG

from openai import OpenAI


def _chat_completion_endpoint(content: str) -> str:
    client = OpenAI(api_key=CONFIG["openai"]["api_key"])

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model=CONFIG["openai"]["default_model"],
    )

    return chat_completion.choices[0].message.content
