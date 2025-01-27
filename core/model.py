import logging

from utils import load_all_available_functions

import extensions
import extensions.ollama.example
from extensions.variables import variables

LOG = logging.getLogger(__name__)

from functools import reduce


class Model:
    def __init__(self):
        self.functions = load_all_available_functions(extensions)
        self.sections = self.get_sections()
        self.variables = variables

    def get_all_functions_flattened(self) -> dict[str, str]:
        return reduce(lambda x, y: {**x, **y}, self.functions.values(), {})

    def get_sections(self) -> dict[str, list[str]]:
        sections = {section: list(functions.keys()) for section, functions in self.functions.items()}
        sections["variables"] = list(variables.keys())

        return sections

    def process_text(self, section: str, function_name: str, input_text: str, **kwargs) -> str:
        if section == "variables":
            return self.variables[function_name]

        return self.functions[section][function_name](input_text, **kwargs)
