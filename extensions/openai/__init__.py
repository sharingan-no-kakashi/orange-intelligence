from extensions.openai.utils import _chat_completion_endpoint


def make_a_joke(text: str, **kwargs) -> str:
    prompt = f"Tell me a joke about {text}"

    return _chat_completion_endpoint(prompt)
