import os
import sys
import time
import requests

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtCore import QTimer

from toast import balloon_tip
from dotenv import load_dotenv

from app.ui import DragDropWindow
from app.mouse import detect_shake, get_cursor_pos
from app.explorer import get_selected_files, is_explorer_active

load_dotenv(override=True)

SUCCESS = "./_assets/check.ico"
ERROR = "./_assets/error.ico"


class MainWindow(DragDropWindow):
    def __init__(self, curX, curY):
        super().__init__(curX, curY)
        
        self.setAcceptDrops(True)
        self.show()
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Событие: файлы над окном."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Событие: файлы дропнуты в окно."""
        event.accept()
        print(event.mimeData().urls())
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        print(files)
        self.label.setText("✅")

        self.upload_files(files)

    def upload_files(self, file_paths):
        """Отправляет файл на сервер."""
        try:
            if not self.is_alive():
                self.server_error()
                self.close()
            
            # HOST = os.environ.get("HOST")
            HOME = os.environ.get("HOME")
            PORT = os.environ.get("PORT")
            url = f"http://{HOME}:{PORT}/send_files"
            files = {}
            total_size = 0
            idx = 0

            for file_path in file_paths:
                if os.path.isdir(file_path):  # Проверяем, является ли путь директорией
                    for root, _, filenames in os.walk(file_path):
                        for filename in filenames:
                            full_path = os.path.join(root, filename)
                            file_size = os.path.getsize(full_path)
                            total_size += file_size
                            # Формируем относительный путь для загрузки
                            relative_path = os.path.relpath(full_path, start=file_path)
                            files[f"file{idx}"] = (relative_path, open(full_path, "rb"))
                            idx += 1
                else:
                    # Если это не директория, обрабатываем файл
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    files[f"file{idx}"] = (os.path.basename(file_path), open(file_path, "rb"))
                    idx += 1
            # total_size = 0
            # for idx, file_path in enumerate(file_paths):
            #     file_size = os.path.getsize(file_path)  # Получаем размер файла
            #     total_size += file_size
            #     files[f"file{idx}"] = (os.path.basename(file_path), open(file_path, "rb"))

            base_timeout = 7
            additional_time = total_size / (5 * 1024 * 1024)
            timeout = base_timeout + additional_time
            response = requests.post(url, files=files, timeout=timeout)
            if response.status_code == 200:
                balloon_tip("Успех", 'Файлы загружены!', icon_path=SUCCESS)
                self.label.setText(f"Uploaded: {os.path.basename(file_path)}")
            else:
                balloon_tip("Ошибка", 'Ошибка при загрузке файлов!', icon_path=ERROR)
                self.label.setText(f"Failed to upload: {os.path.basename(file_path)}")
        # except HTTPError as e:
        #     self.server_error(e)
        # except TimeoutError as e:
        #     self.server_error(e)
        except Exception as e:
            self.server_error(e)
        finally:
            QTimer.singleShot(500, self.close)
    
    def is_alive(self, timeout: float = 2) -> bool:
        PORT = os.environ.get("PORT")
        HOME = os.environ.get("HOME")
        IS_ALIVE = os.environ.get("IS_ALIVE")
    
        url = f"http://{HOME}:{PORT}/{IS_ALIVE}"
        
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True
        return False

    def server_error(self, e: Exception | None = None):
        balloon_tip("Сервер недоступен", str(e), icon_path=ERROR)
        self.label.setText("🚫")
        if e:
            print(e)
        # time.sleep(0.1)
        return


def run_app():
    app = QApplication(sys.argv)

    while True:
        if is_explorer_active():
            if selected_files := get_selected_files():
                print(selected_files)
                if detect_shake():
                    x, y = get_cursor_pos()
                    window = MainWindow(x, y)
                    window.show()
                    # break
                    while window.isVisible():
                        app.processEvents()
            time.sleep(0.1)
        time.sleep(3)
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
