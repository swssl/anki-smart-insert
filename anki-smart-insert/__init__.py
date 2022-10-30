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
    # Test if data update should be applied
    if internal or not mime.hasText():
        return mime
    data = mime.text()
    text = data.split("\n")
    paragraphs = []
    for index, line in enumerate(text):
        while line[0] == " ":
            line = line[1:]
        # Process first line
        if index == 0:
            if line[0] not in config['bullets']:
                # Create Headline if line doenst start with a bullet
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
                paragraphs[-1].text = f"{paragraphs[-1].text} {line}"
            else:
                paragraphs.append(Paragraph(symbol=line[0], text=line))
    output_text = ""
    for p in paragraphs:
        if isinstance(p, Headline):
            output_text + output_text + f"{p}\n"
        elif isinstance(p, Paragraph):
            output_text = output_text + f"{p.symbol} {p.text}\n"

        # line = apply_filter(line)
    # if config['symbols']['activate']:
    #     if isinstance(config['symbols']['input'], list):
    #         if config["symbols"]["include_whitespaced"]:
    #             for sym in config['symbols']['input']:
    #                 data = data.replace(f"{sym} ", f"{config['symbols']['output']} ")
    #         output = f"{config['symbols']['output']} " if config["symbols"]["add_whitespace"] else config['symbols']['output']
    #         for sym in config['symbols']['input']:
    #             data = data.replace(sym, output)
    # if isinstance(config['additional_replacements'], list) \
    #    and len(config['additional_replacements']):
    #     for setting in config['additional_replacements']:
    #         for sym in setting['input']:
    #             data = data.replace(sym, setting['output'])

    result = QMimeData()
    result.setData("text/plain", QByteArray(output_text.encode()))
    return result


gui_hooks.editor_will_process_mime.append(process_inserted_data)
