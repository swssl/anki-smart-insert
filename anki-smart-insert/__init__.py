import json
import re
import jsonschema
from aqt import (
    gui_hooks,
    mw,
)
from aqt.qt import (
    QByteArray,
    QMimeData,
)
from aqt.utils import (
    showWarning,
)
from .notes import (
    Headline,
    Section,
    NumberedSection,
)


try:
    config_path = f"{mw.addonManager.addonsFolder(__name__)}/config.json"
    _schema = json.load(open(
        f"{mw.addonManager.addonsFolder(__name__)}/config.schema")
        )
    _config = json.load(
        open(f"{mw.addonManager.addonsFolder(__name__)}/config.json")
        )
    # jsonschema.validate(schema=_schema, instance=_config)
except jsonschema.exceptions.ValidationError as e:
    msg = f"Failed to validate {e.json_path} configuration from {config_path}."
    showWarning(msg)
except FileNotFoundError:
    pass
finally:
    config = mw.addonManager.getConfig(__name__)
    print("Loaded config from config.json")


def on_insert(mime: QMimeData, *args):
    """Function that is called before something is pasted into any editor field

    Args:
        mime (QMimeData): Data to be inserted

    Returns:
        QMimeData: Edited clipboard data
    """
    try:
        print("anki-smart-insert invoked")
        # enumerations_filter = config["numbered_lists"]["filter_regex"]
        bullets = config['bullets']
        filter_regex = config["numbered_lists"]["filter_regex"]
        enumeration_ref = config['numbered_lists']["enumeration_reference"]
        content_ref = config['numbered_lists']["content_reference"]
        # Test if data update should be applied

        if not mime.hasText():
            return mime
        data = mime.text()
        text = data.split("\n")
        # Whenever we got a one-liner, return it as-is
        if len(text) == 1:
            return mime
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


# Register process_inserted_data as callback for the
# editor_will_process_mime hook
gui_hooks.editor_will_process_mime.append(on_insert)
