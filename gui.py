import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QFont
import os
from tkinter import filedialog as fd

from grid import BlockGrid

FILE_NAME = ""
USERNAME = ""

class MainPage(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)

        self.canvas = canvas
        
        # Create a vertical layout to hold the widgets
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Add a label to the layout
        label = QLabel('Welcome to the the APP!')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Add a button to start the game
        start_button = QPushButton('Start')
        start_button.setMaximumSize(150, 50)
        start_button.clicked.connect(self.start_app)
        layout.addWidget(start_button)

        # Add a button to select file
        file_button = QPushButton('Select File')
        file_button.setMaximumSize(150, 50)
        file_button.clicked.connect(self.select_file)
        layout.addWidget(file_button)
        
        # Add a button to login
        login_button = QPushButton('Login')
        login_button.setMaximumSize(150, 50)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

    def start_app(self):
        # Create the block grid and add it to the stacked widget
        block_size = 96
        grid = BlockGrid(12, 9, block_size)
        self.canvas.addWidget(grid)

        # Switch to the game widget
        self.canvas.setCurrentWidget(grid)

    def select_file(self):
        global FILE_NAME
        FILE_NAME = fd.askopenfilename()
        print(FILE_NAME)
        
    def login(self):
        self.canvas.setCurrentIndex(1) 


class LoginPage(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        
        self.canvas = canvas
        
        layout = QVBoxLayout()
        
        # Create a QLineEdit widget to hold the text
        text_box = QLineEdit()
        
        # Create a button to confirm login
        confirm_login = QPushButton('Log In')
        confirm_login.setMaximumSize(150, 50)
        confirm_login.clicked.connect(lambda: self.login(text_box.text()))
        
        # Add widgets to the layout
        layout.addWidget(text_box)
        layout.addWidget(confirm_login)
        self.setLayout(layout)
        
    def login(self, username):
        if username != '':
            print(username)
            USERNAME = username
            self.canvas.setCurrentIndex(0)
                    
class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the stacked widget to hold the pages
        self.stacked_widget = QStackedWidget(self)
        
        # Create the first page widget and add it to the stacked widget
        main_page = MainPage(self.stacked_widget)
        self.stacked_widget.addWidget(main_page)
        
        # Create the login page widget and add it to the stacked widget
        login_page = LoginPage(self.stacked_widget)
        self.stacked_widget.addWidget(login_page)

        # Add the stacked widget to the canvas layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Set the size of the window, 96 is the block size, y + 50 to give extra space
        window_size = (16 * 96, 9 * 96 + 50)
        self.setFixedSize(*window_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the canvas widget
    canvas = Canvas()

    # Show the window
    canvas.show()

    sys.exit(app.exec_())
