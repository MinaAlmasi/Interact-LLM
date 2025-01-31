from dataclasses import dataclass
from typing import Dict

@dataclass
class Language:
    code: str
    name: Dict[str, str]

supported_languages = [
    Language(
        code="es",
        name={
            "english": "Spanish",
            "danish": "Spansk",
            "native": "Español"
        }
    ),
    Language(
        code="de",
        name={
            "english": "German",
            "danish": "Tysk",
            "native": "Deutsch"
        }
    )
]

if __name__ == "__main__":
    print("[INFO:] Supporting:")
    for i, lang in enumerate(supported_languages):
        print("{0}. {1} ({2})".format(i+1, lang.name["english"], lang.code))