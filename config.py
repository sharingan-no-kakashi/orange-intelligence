import os
import sys
import tempfile

LOGGING_LEVEL = "DEBUG"

CONFIG = {
    "app": {
        "name": "orange-ai",
        "icon": "assets/icon.png",
    },
    "variables": {
        "import_bash_profile": False,
    },
    "ollama": {
        "name": "ollama",
        "url": "https://ollama.com",
        "default_model": "llama3.1",
    },
    "openai": {"api_key": os.environ.get("OPENAPI_KEY"), "default_model": "gpt-3.5-turbo"},
    "logging": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {"format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"},
        },
        "handlers": {
            "stream": {
                "level": LOGGING_LEVEL,
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "detailed",
            },
            "file": {
                "level": LOGGING_LEVEL,
                "class": "logging.FileHandler",
                "filename": tempfile.NamedTemporaryFile(delete=False).name,
                "formatter": "detailed",
            },
        },
        "loggers": {
            "": {  # Root logger configuration
                "handlers": ["stream", "file"],
                "level": LOGGING_LEVEL,
                "propagate": True,
            },
        },
    },
}
