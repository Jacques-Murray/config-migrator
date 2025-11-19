# Author: Jacques Murray
import json
from typing import Any


class JSSerializer:
    """
    Utility to serialize Python structures into ECMAScript Module (ESM) format.
    Does not use a JS engine; performs string manipulation for formatting.
    """

    @staticmethod
    def to_js_object_string(data: Any, indent: int = 2) -> str:
        """
        Converts a Python dict/list to a JavaScript object string.
        Replaces Python-specific keywords (None, True) with JS equivalents.
        """
        # Use JSON dump as a base
        json_str = json.dumps(data, indent=indent)

        # Post-process to make it look more like modern JS
        # Note: Keys remain quoted in standard JSON.
        # Unquoting keys requires a complex parser/lexer, keeping quotes is valid JS.

        # Convert null to null (JSON does this), True to true (JSON does this).
        # We mainly ensure it is exported correctly.
        return json_str

    @staticmethod
    def generate_esm_export(data: Any) -> str:
        """
        Wraps data in an ESM default export.
        """
        js_obj = JSSerializer.to_js_object_string(data)
        return f"export default {js_obj};\n"
