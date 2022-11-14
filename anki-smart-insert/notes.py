from typing import (
    Optional,
)


class Headline():
    """Headline representing class. Used to store lines without bullets
    """
    def __init__(self, text: str = "", bold: bool = False):
        self.text = text
        self.bold = bold

    def set_text(self, text: str):
        self.text = text

    def get_text(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f'<Headline "{self.__str__()}">'

    def __str__(self):
        res = self.text
        if self.bold:
            res = f"<b>{res}</b><br>"
        return res


class Section():
    """Paragraph representing class. Used to store key points.
    """
    def __init__(self, symbol: Optional[str], text: Optional[str]):
        self.symbol = symbol
        self.text = text

    def add_text(self, text: str):
        self.text = self.text + " " + text

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} [{self.symbol}]"{self.__str__()}">'

    def __str__(self) -> str:
        res = f"{self.text}<br>"
        return res


class NumberedSection(Section):
    pass
