import json
import re
import jsonschema
from aqt import (
    gui_hooks,
    mw,
)
from aqt.webview import (
    AnkiWebView,
    AnkiWebViewKind,
)
from aqt.editor import (
    Editor,
    EditorWebView,
)
from aqt.qt import (
    QByteArray,
    QMimeData,
    QPushButton,
)
from aqt.utils import (
    showWarning,
    showInfo,
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



# Register process_inserted_data as callback for the
# editor_will_process_mime hook
from .insert_callback import on_insert
gui_hooks.editor_will_process_mime.append(on_insert)

from .ai_mode import on_field_change, on_editor_init
gui_hooks.editor_did_focus_field.append(on_field_change)
gui_hooks.editor_did_init.append(on_editor_init)

# def on_editor_load(buttons: list[str], editor: Editor):
#     def testFunction(*args, **kwargs) -> None:
#         # get the number of cards in the current collection, which is stored in
#         # the main window
#         print("AI mode toggled")

#     btn = editor.addButton(func=testFunction, id="ai_mode_button", label="AI", cmd="ai_mode", icon=None, rightside=False, toggleable=True)
#     buttons.append(btn)
# gui_hooks.editor_did_init_buttons.append(on_editor_load)

# def mytest(editor_web_view: EditorWebView):
#     if editor_web_view.kind != AnkiWebViewKind.EDITOR:
#         return
#     editor_web_view.
#     editor_web_view.eval(
#         """"""
#     )

# gui_hooks.editor_web_view_did_init.append(mytest)
