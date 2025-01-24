import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from random  import choice

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0
        
        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.setFixedSize(QSize(400, 300))
        self.button.clicked.connect(self.the_button_was_clicked)
        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        # 1st part
        # self.button.setText("You already clicked me.")
        # self.button.setEnabled(False)

        # 2nd part
        print('clicked')
        new_window_title = choice(window_titles)
        print(f"Setting title:  {new_window_title}")
        self.setWindowTitle(new_window_title)

        self.n_times_clicked = self.n_times_clicked + 1
        print(self.n_times_clicked)
        
        # 1st part
        # Also change the window title.
        # self.setWindowTitle("My Oneshot App")

    # 2nd part
    def the_window_title_changed(self, window_title):
        print(f"Window title changed: {window_title}")

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()