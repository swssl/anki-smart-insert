# import the main window object (mw) from aqt
from aqt import mw, gui_hooks
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from aqt.editor import EditorWebView


def process_inserted_data(mime: QMimeData, editor_web_view: EditorWebView, internal: bool, extended: bool, drop_event: bool,):
    """Function that is called before something is pasted into any editor field

    Args:
        mime (QMimeData): Data to be inserted
        editor_web_view (EditorWebView): Some kind of editor instance
        internal (bool): true if the content is copied from inside anki
        extended (bool): ???
        drop_event (bool): True if it was a drag-and-drop event instead of ordinary ctrl+v???

    Returns:
        QMimeData: Edited clipboard data
    """
    # Test if data update should be applied
    if internal or not mime.hasText():
        return mime
    data = mime.text()
    result = QMimeData()

    result.setData("text/plain", QByteArray(f"Insert {data}".encode()))
    return result

gui_hooks.editor_will_process_mime.append(process_inserted_data)
