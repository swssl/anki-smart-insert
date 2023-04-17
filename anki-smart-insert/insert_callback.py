import re
from .notes import (
    Headline,
    Section,
    NumberedSection,
)
from aqt.qt import (
    QByteArray,
    QMimeData,
)
from . import config
from .ai_mode import process_ai_data


def on_insert(mime: QMimeData, *args, **kwargs):
    """Function that is called before something is pasted into any editor field

    Args:
        mime (QMimeData): Data to be inserted

    Returns:
        QMimeData: Edited clipboard data
    """
    try:
        # Test for valid data
        if not mime.hasText() or kwargs.get("internal", False):
            return mime
        bullets = config['bullets']
        filter_regex = config["numbered_lists"]["filter_regex"]
        enumeration_ref = config['numbered_lists']["enumeration_reference"]
        content_ref = config['numbered_lists']["content_reference"]
        ai_question_regex = config['ai']['front_regex']
        data = mime.text()
        text = data.split("\n")
        # Whenever we got a one-liner, return it as-is
        if len(text) == 1:
            return mime
        # When AI-generated questions are inserted, this should invoke special text processing
        if config['ai']['enabled'] and re.match(ai_question_regex, text[0]) is not None:
            print("AI mode!!")
            output_text = process_ai_data(text)
            result = QMimeData()
            result.setData("text/html", QByteArray(output_text.encode()))
            return result
        paragraphs = []
        for index, line in enumerate(text):
            while line[0] == " ":
                line = line[1:]
            if index == 0:
                if re.match(filter_regex, line):
                    # Add a new NumberedSection to paragraphs
                    paragraphs.append(NumberedSection(
                            symbol=re.sub(filter_regex, enumeration_ref, line),
                            text=re.sub(filter_regex, content_ref, line))
                            )
                elif line[0] in bullets:
                    # Add a new Section to paragraphs
                    paragraphs.append(Section(symbol=line[0], text=line[1:]))
                else:
                    paragraphs.append(Headline(line, bold=True))
            else:
                if re.match(filter_regex, line):
                    # Add new Numbered Section to paragraphs
                    paragraphs.append(NumberedSection(
                            symbol=re.sub(filter_regex, enumeration_ref, line),
                            text=re.sub(filter_regex, content_ref, line)))
                elif line[0] in bullets:
                    # Add new Section to paragraphs
                    paragraphs.append(Section(symbol=line[0], text=line[1:]))
                elif len(paragraphs) and isinstance(paragraphs[-1], Section):
                    # Add line to current paragraph
                    paragraphs[-1].add_text(line)
                else:
                    # Add Section without symbol to paragraphs
                    paragraphs.append(Section(symbol='', text=line))
        if paragraphs is []:
            # Whenever we didn't detect any text, return the initial data
            return mime
        # Format the parsed text objects for output
        output_text = ""
        for p in paragraphs:
            if isinstance(p, Headline):
                output_text = output_text + f"{p}"
            elif isinstance(p, NumberedSection):
                output_text = output_text + f"{p.symbol} {p}"
            elif isinstance(p, Section):
                if config["options"]["output"] not in ["", None]:
                    output_text = output_text + f"{config['options']['output']} {p}"
                else:
                    output_text = output_text + f"{p.symbol} {p}"
        # Create result object that overwrites the initial mime argument
        result = QMimeData()
        result.setData("text/html", QByteArray(output_text.encode()))
        return result
    except Exception as e:
        # Emergency exit: If any error occurs we just return the initial data
        if config['debug_mode']:
            raise e
        else:
            print(e)
        return mime