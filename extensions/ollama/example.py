import logging

from config import CONFIG

from ollama import ChatResponse, chat

LOG = logging.getLogger(__name__)


def ollama(prompt: str) -> str:
    response: ChatResponse = chat(
        model=CONFIG["ollama"]["default_model"],
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    # or access fields directly from the response object
    LOG.debug(response.message.content)
    return response.message.content


def improve_grammar(input_text: str, **kwargs) -> str:
    prompt = (
        "Improve the grammar of this sentence. Return only the improved sentence, do not add anything else. "
        + input_text
    )
    return ollama(prompt)


def translate_to_english(input_text: str, **kwargs) -> str:
    prompt = (
        "Translate this sentence to English. Return only the translated sentence, do not add anything else. "
        + input_text
    )
    return ollama(prompt)


def make_it_polite(input_text: str, **kwargs) -> str:
    prompt = (
        "Convert this sentence to a polite one. Return only the converted sentence, do not add anything else. "
        + input_text
    )
    return ollama(prompt)
