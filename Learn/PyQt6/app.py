import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
# When you subclass a Qt class you must always 
# call the super __init__ function to allow Qt to set up the object
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!") #Here add self for 2nd part
        self.setFixedSize(QSize(400, 300)) #or use .setMinimumSize() and .setMaximumSize()

        button.setCheckable(True) #Here add self for 2nd part

        #When 1st part is active, 2nd part is not required and vice-versa
        #only for 2nd part self is added everywhere else it was for windowtitle and central widget
        #1st part
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)

        #2nd part
        # self.button.released.connect(self.the_button_was_released)
        # self.button.setChecked(self.button_is_checked)

        # Set the central widget of the Window.
        self.setCentralWidget(button) #Here add self for 2nd part

    #1st part
    def the_button_was_clicked(self):
        print('clicked!')

    def the_button_was_toggled(self, checked):
        print('checked?', checked)
        self.button_is_checked = checked       
    
    #2nd part
#     def the_button_was_released(self):
#         self.button_is_checked = self.button.isChecked()
#         print(self.button_is_checked)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()