import win32com.client
from app.utils import get_explorer_pid, is_pid_active


def get_selected_files(shell=None):
    """Возвращает список выделенных файлов в проводнике."""
    if shell is None:
        shell = win32com.client.Dispatch("Shell.Application")

    try:
        selected_files = []
        for window in shell.Windows():
            if window and window.Document:
                selected_files.extend(
                    item.Path for item in window.Document.SelectedItems()
                )
        return selected_files
    except Exception:
        return []


def is_explorer_active():
    return is_pid_active(get_explorer_pid())
