import json
import jsonschema
from aqt import (
    gui_hooks,
    mw,
)
from aqt.editor import EditorWebView
from aqt.qt import (
    QByteArray,
    QMimeData,
)
from aqt.utils import (
    showWarning,
)
from .notes import (
    Headline,
    Paragraph,
)


try:
    config_path = f"{mw.addonManager.addonsFolder(__name__)}/config.json"
    _schema = json.load(open(
        f"{mw.addonManager.addonsFolder(__name__)}/config.schema")
        )
    _config = json.load(
        open(f"{mw.addonManager.addonsFolder(__name__)}/config.json")
        )
    jsonschema.validate(schema=_schema, instance=_config)
except jsonschema.exceptions.ValidationError as e:
    msg = f"Failed to validate {e.json_path} configuration from {config_path}."
    showWarning(msg)
except FileNotFoundError:
    pass
finally:
    config = mw.addonManager.getConfig(__name__)
    print("Load config from config.json")


def apply_filter(input: str) -> str:
    return input


def process_inserted_data(mime: QMimeData,
                          editor_web_view: EditorWebView,
                          internal: bool,
                          extended: bool,
                          drop_event: bool,):
    """Function that is called before something is pasted into any editor field

    Args:
        mime (QMimeData): Data to be inserted
        editor_web_view (EditorWebView): Some kind of editor instance
        internal (bool): true if the content is copied from inside anki
        extended (bool): ???
        drop_event (bool): True if it was a drag-and-drop event instead of
        ordinary ctrl+v???

    Returns:
        QMimeData: Edited clipboard data
    """
    print("anki-smart-insert invoked")
    # Test if data update should be applied
    try:
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
            # Process first line
            if index == 0:
                if line[0] not in config['bullets']:
                    # Create Headline if line doesn't start with a bullet
                    paragraphs.append(Headline(line, bold=True))
                else:
                    # Create paragraph if there is a bullet
                    paragraphs.append(Paragraph(symbol=line[0], text=line[1:]))
                continue
            # Process the following [1:] lines
            if line[0] in config['bullets']:
                # Create a new Paragraph
                paragraphs.append(Paragraph(symbol=line[0], text=line[1:]))
            elif line[0] not in config["bullets"]:
                # If possible, concat line to latest Paragraph, otherwise create new
                if len(paragraphs) and isinstance(paragraphs[-1], Paragraph):
                    paragraphs[-1].add_text(line)
                else:
                    paragraphs.append(Paragraph(symbol=line[0], text=line))
        # Whenever we didn't detect any text, return the initial data
        if paragraphs is []:
            return mime
        # Format the parsed text objects for output
        output_text = ""
        for p in paragraphs:
            if isinstance(p, Headline):
                output_text = output_text + f"{p}"
            elif isinstance(p, Paragraph):
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
        print(e)
        return mime


# Register process_inserted_data as callback for the
# editor_will_process_mime hook
gui_hooks.editor_will_process_mime.append(process_inserted_data)
