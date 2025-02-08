from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton


class CloseButton(QPushButton):
    def __init__(self, parent):
        super(CloseButton, self).__init__(parent)
        self.setAcceptDrops(True)

        self.setGeometry(QRect(5, 5, 20, 20))
        self.setText("x")

        self.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(54, 54, 54, 0.5);
                color: white;
                border: none;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: red;
            }
            """
        )


class DragDropWindow(QMainWindow):
    def __init__(self, curX: int, curY: int):
        super().__init__()

        self.setWindowTitle("Drop Files")
        self.setGeometry(curX+50, curY-50, 100, 100)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.label = QLabel("Drop files here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            """
            color: white;
            """
        )
        layout.addWidget(self.label)

        self.round_widget = QWidget(self)
        self.round_widget.resize(100, 100)

        self.round_widget.setStyleSheet(
            """
            background:rgb(30, 30, 30);
            border-radius: 10px;
            border: 2px solid rgb(54, 54, 54);
            """
        )

        self.close_button = CloseButton(self)
        self.close_button.clicked.connect(self.close)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.close_button.raise_()

