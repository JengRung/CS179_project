import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit
from PySide2.QtCore import Qt, QTimer, QPropertyAnimation, QRect
import os
from tkinter import filedialog as fd
import numpy as np

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
        label = QLabel('Welcome, please select a task!')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        

        balance_button = QPushButton('Balance Task')
        balance_button.setMaximumSize(150, 50)
        balance_button.clicked.connect(self.start_balance)
        layout.addWidget(balance_button)

        transfer_button = QPushButton('Transfer Task')
        transfer_button.setMaximumSize(150, 50)
        transfer_button.clicked.connect(self.start_transfer)
        layout.addWidget(transfer_button)

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

    #[:+]-- changed 'start_app' to start balance, also added 'start_transfer;  one func
    def start_balance(self):
        # Create the block grid and add it to the stacked widget
        block_size = 96
        grid = BlockGrid(12, 9, block_size)
        self.canvas.addWidget(grid)
        self.canvas.setCurrentWidget(grid)

    def start_transfer(self):
        block_size = 64
        sizer= 0.7
        grid = TransferGrid(12, 9, 24, 4, block_size*sizer)
        self.canvas.addWidget(grid)
        self.canvas.setCurrentWidget(grid)

    def select_file(self):
        global FILE_NAME
        FILE_NAME = fd.askopenfilename()
        print(FILE_NAME)
        
    def login(self):
        self.canvas.setCurrentIndex(1) 

#[+:]-- BalanceGrid == BlockGrid
class BlockGrid(QWidget):
    def __init__(self, rows, cols, block_size, parent=None):
        super().__init__(parent)
        
        # Set a custon start and end block for testing, formate: (x,y)
        self._start_block = (4,5)
        self._end_block = (9,3)
        
        # 2 coordinates to track the path block
        self._track_block_x = self._start_block[0]
        self._track_block_y = self._start_block[1]
        
        # Create a canvas layout to hold the blocks and button 
        animation_page_layout = QHBoxLayout()
        self.setLayout(animation_page_layout)


        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        animation_page_layout.addLayout(grid_layout)

        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                label.setFixedSize(block_size, block_size)
                label.setProperty('row', row)
                label.setProperty('col', col)
                block_style = 'border: 1px solid black; '
                
                # Algor to convert cord: x-=1, y=9-y 
                if (row + 1, 9 - col) == self._start_block:
                    block_style += 'background-color: green;'
                elif (row + 1, 9 - col) == self._end_block:
                    block_style += 'background-color: red;'
                    
                label.setStyleSheet(block_style)
                grid_layout.addWidget(label, col, row)
                
        

        button = QPushButton('Next')
        animation_page_layout.addWidget(button, 2)
        
        self.setFixedSize(12 * block_size + 200, 9 * block_size)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(1000)

    def update_labels(self):
        # print(self._track_block_x, self._track_block_y)
        
        # Finish one cycle of path, clear the lable and update again
        if self._track_block_x == self._end_block[0] and self._track_block_y == self._end_block[1]:
            print("Finish one cycle")
            
            self._track_block_x = self._start_block[0]
            self._track_block_y = self._start_block[1]
            
            for label in self.findChildren(QLabel):
                row = label.property('row')
                col = label.property('col')
                
                block_style = 'border: 1px solid black; '
                if (row + 1, 9 - col) == self._start_block:
                    block_style += 'background-color: green;'
                elif (row + 1, 9 - col) == self._end_block:
                    block_style += 'background-color: red;'
                label.setStyleSheet(block_style)

        else:
            if self._track_block_y != self._end_block[1]:
                if self._track_block_y < self._end_block[1]:
                    self._track_block_y += 1
                else:
                    self._track_block_y -= 1
                
            elif self._track_block_x != self._end_block[0]:
                if self._track_block_x < self._end_block[0]:
                    self._track_block_x += 1
                else:
                    self._track_block_x -= 1
            
            for label in self.findChildren(QLabel):
                row = label.property('row')
                col = label.property('col')
                if (row + 1, 9 - col) == (self._track_block_x, self._track_block_y):
                    label.setStyleSheet('border: 1px solid black; background-color: red;')


#[+:]--
class TransferGrid(QWidget):
    def __init__(self, mainRows, mainCols, buffRows, buffCols,  block_size, parent=None):
        super().__init__()
        self.clk= 0
        self.clkLim= 100
        self.mainStartPt = (0,0)
        self.mainEndPt = (4,4)
        self.mainMidPt = (self.mainEndPt[0], self.mainStartPt[1])
        self.buffStartPt = (0,0)
        self.buffEndPt = (4,4)
        self.buffMidPt = (self.buffEndPt[0], self.buffStartPt[1])
        buffGrid = QGridLayout()
        buffGrid.setSpacing(5)
        for row in range(buffRows):
            for col in range(buffCols):
                #[+]-- cells are labled by coordinates, should change to weight later
                # label = QLabel("({0},{1})".format(row, col))
                # label.setAlignment(Qt.AlignCenter)

                #[+]-- the labels are the colored boxes the represent the containers
                box = QLabel("({0},{1})".format(row, col))
                box.setAlignment(Qt.AlignCenter)
                box.setFixedSize(block_size, block_size)
                box.setProperty('row', row)
                box.setProperty('col', col)
                blockStyle = 'border: 7px solid black; '
                

                if (row , col) == self.buffStartPt:
                    blockStyle += 'background-color: yellow;'
                elif (row, col) == self.buffEndPt:
                    blockStyle += 'background-color: purple;'
                    
                box.setStyleSheet(blockStyle)
                buffGrid.addWidget(box, col, row)
                # buffGrid.addWidget(label, col, row)
                
        mainGrid = QGridLayout()
        mainGrid.setSpacing(5)
        for row in range(mainRows):
            for col in range(mainCols):
                box = QLabel("({0},{1})".format(row, col))
                box.setAlignment(Qt.AlignCenter)
                box.setFixedSize(block_size, block_size)
                box.setProperty('row', row)
                box.setProperty('col', col)
                blockStyle = 'border: 7px solid black; '

                if (row , col) == self.mainStartPt:
                    blockStyle += 'background-color: cyan;'
                elif (row, col) == self.mainEndPt:
                    blockStyle += 'background-color: red;'
                    
                box.setStyleSheet(blockStyle)
                mainGrid.addWidget(box, col, row)


        transGrid = QGridLayout()
        transGrid.addLayout(mainGrid, 0, 0)
        transGrid.addLayout(buffGrid, 0, 1)
        self.setLayout(transGrid)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(self.clkLim)
    def update(self):
        self.clk+=1
        if self.clk>8: self.clk=1
        curBoxMain= self.mainStartPt
        # print(self.clk)
        for box in self.findChildren(QLabel):
            row = box.property('row')
            col = box.property('col')
            # #[+]-- the labels are the colored boxes the represent the containers
            # box = QLabel()
            # box.setFixedSize(block_size, block_size)
            # box.setProperty('row', row)
            # box.setProperty('col', col)
            blockStyle = 'border: 7px solid black; '
            if (row , col) == self.buffStartPt:
                blockStyle += 'background-color: yellow;'
            elif (row, col) == self.buffEndPt:
                blockStyle += 'background-color: purple'

            elif (row)==self.mainEndPt[0]:
                if (col+self.clk)<=self.mainEndPt[1]:
                    blockStyle += 'background-color: magenta'
            box.setStyleSheet(blockStyle)


    






      



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

        sizer= 2.25
        window_size = (16 * 96*sizer*1.1, 9 * 96*sizer + 50)
        self.setFixedSize(*window_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = Canvas()
    canvas.show()
    sys.exit(app.exec_())




# [::] -- Todo --
#     - [ ] Add page for the transfer task
#     - [ ] User log comments
#     - [ ] log file
#     - [ ] manifest checkist for transfer task
#     - [ ] display instructions for moving containers
#     - [ ] reminder prompt