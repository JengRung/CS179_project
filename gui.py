import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton
# import PySide2.QtWidgets
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QTimer, QPropertyAnimation, QRect
import os
from tkinter import filedialog as fd
import numpy as np

FILE_NAME = ""
USERNAME = ""



indexTionary= {
    'main': 0,
    'login': 1,
    'transfer': 2,
}

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
        # block_size = 64
        # sizer= 0.7
        # grid = TransferGrid(12, 9, 24, 4, block_size*sizer)
        # self.canvas.addWidget(grid)
        # self.canvas.setCurrentWidget(grid)
        
        # transApp= QWidget()
        # self.setCentralWidget(transApp)
        # window= QVBoxLayout(transApp)

        self.canvas.setCurrentIndex(indexTionary['transfer']) 

    def select_file(self):
        global FILE_NAME
        FILE_NAME = fd.askopenfilename()
        print(FILE_NAME)
        
    def login(self):
        self.canvas.setCurrentIndex(1) 

#[+:]-- BalanceGrid == BlockGrid
class BlockGrid(QWidget):
    # def __init__(self, rows, cols, block_size, parent=None):
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
    #---TOdo--:
        #- [ ] Process input into numbers for output into algo
        #- [ ] refactor for better readabilty
        #- [ ] Parse manifest
        #- [ ] Replace manifest list with checklist
        
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas= canvas
#-[:+:]===============================Transfer CheckList =========================================\\

        #[::]-- Holds the two columns in a single box:---\\
        #--[[load][unload]]--------------------------\\
        colContainer = QtWidgets.QHBoxLayout(self)
        loadCol= QVBoxLayout()
        colContainer.addLayout(loadCol)
        unloadCol_R= QVBoxLayout()
        colContainer.addLayout(unloadCol_R)

        #[+]:-- load column is for data entry--------------------------\\
        #-----------------------------------\\
        inputSect_L= QtWidgets.QHBoxLayout()
        itemLabel = QLabel("Item Name:")
        self.weightLabel = QLabel("Weight:")
        self.inputName = QLineEdit()
        self.inputWeight = QLineEdit()
        loadBtn = QtWidgets.QPushButton("Load Item", self)
        self.loadList= QtWidgets.QListWidget(self)
        loadCol.addWidget(QLabel("Load Items"))
        loadBtn.clicked.connect(self.add_thing)
        inputSect_L.addWidget(itemLabel)
        inputSect_L.addWidget(self.inputName)
        inputSect_L.addWidget(self.weightLabel)
        inputSect_L.addWidget(self.inputWeight)
        inputSect_L.addWidget(loadBtn)
        loadCol.addLayout(inputSect_L)
        loadCol.addWidget(self.loadList)


        #[+]:-- unload column reads from the manifest and makes list--------\\
        self.maniBtn = QtWidgets.QPushButton("Open Manifest", self)
        self.manifestList= QtWidgets.QListWidget(self)
        unloadCol_R.addWidget(QLabel("Unoad Items"))
        self.maniBtn.clicked.connect(self.manifest)
        unloadCol_R.addWidget(self.maniBtn)
        unloadCol_R.addWidget(self.manifestList)
        
    
    def manifest(self):
        manifest_Path= fd.askopenfilename()
        print(manifest_Path)
        if len(manifest_Path)>0:
            with open(manifest_Path, "r") as file:
                for row in file:
                    itemEntry= row.strip()
                    self.manifestList.addItem(itemEntry)

    def add_thing(self):
        print("list accessed")
        itemName = self.inputName.text()
        itemWeight= self.inputWeight.text()
        listInput = "+["+itemName+"  :  "+ itemWeight+ "]"
        if len(listInput)+len(itemWeight)>2:
            self.loadList.addItem(listInput)
            self.inputName.clear()
            self.inputWeight.clear()
#-[:+:]========================================Transfer CheckList -========================//


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
        
        self.stacked_widget = QStackedWidget(self)

        main_page = MainPage(self.stacked_widget)
        self.stacked_widget.addWidget(main_page)
        

        login_page = LoginPage(self.stacked_widget)
        self.stacked_widget.addWidget(login_page)

        #[+]--
        transPage= TransferGrid(self.stacked_widget)
        self.stacked_widget.addWidget(transPage)


        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        sizer= 1
        window_size = (16 * 96*sizer*1.1, 9 * 96*sizer + 50)
        self.setFixedSize(*window_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = Canvas()
    canvas.show()
    sys.exit(app.exec_())




# [::] -- Todo --
#     - [+] Add page for the transfer task
#     - [ ] User log comments
#     - [ ] log file
#     - [+] manifest checkist for transfer task
#     - [ ] display instructions for moving containers
#     - [ ] reminder prompt