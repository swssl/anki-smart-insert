from typing import (
    Optional,
)


class Headline():
    def __init__(self, text: str = "", bold: bool = False):
        self.text = text
        self.bold = bold

    def set_text(self, text: str):
        self.text = text

    def get_text(self) -> str:
        return self.text

    def __str__(self):
        res = self.text
        if self.bold:
            res = f"<b>{res}</b>"
        return res


class Paragraph():
    def __init__(self, symbol: Optional[str], text: Optional[str]):
        self.symbol = symbol
        self.text = text

    def add_text(self, text: str):
        self.text.concat(text)
