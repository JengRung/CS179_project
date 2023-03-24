import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QPushButton, QRadioButton
# import PySide2.QtWidgets
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PySide2.QtGui import QFont
import os
from tkinter import filedialog as fd
from grid import BlockGrid
import numpy as np
import re
# from a_star import all

FILE_NAME = ""
# USERNAME = ""
# SIZER= 1.15, 2, 1
SIZER= 0.7



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






#-[:+:]===============================Transfer CheckList =====================================================================\\
class TransferGrid(QWidget):
    #---TOdo--:
        #- [+] Process input into numbers for output into A* algo
            # - [+] Load Output: (name, weight)
            # - [+] unload output: ( x, y, weight )
        #- [ ] refactor for better readabilty
        #- [+] Parse manifest weiight and coordinates
        #- [ ] Parse panifest item names
        #- [+] Replace manifest list with Multi-select
#     - [+] Add page for the transfer task
#     - [ ] User log comments
#     - [ ] log file
#     - [+] manifest checkist for transfer task
#     - [ ] display instructions for moving containers
#     - [ ] reminder prompt
#     - [ ] Generat new Manifest
        
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas= canvas

        self.loadout= np.empty((0,2))
        self.unloadItems= np.empty((0,3))

        #[::]-- Holds the two columns in a single box:---\\
        #--[[load][unload]]--------------------------\\
        colContainer = QtWidgets.QHBoxLayout(self)
        
        loadCol= QVBoxLayout()
        colContainer.addLayout(loadCol)

        self.unloadCol_R= QVBoxLayout()
        colContainer.addLayout(self.unloadCol_R)

        subCol_R= QVBoxLayout()
        colContainer.addLayout(subCol_R)

        #[+]:-- load column is for data entry--------------------------\\
        #-----------------------------------\\
        inputSect_L= QtWidgets.QHBoxLayout()
        itemLabel = QLabel("Item Name:")
        self.weightLabel = QLabel("Weight:")
        self.inputName = QLineEdit()
        self.inputWeight = QLineEdit()
        loadBtn = QtWidgets.QPushButton("Load Item", self)
        self.loadList= QtWidgets.QListWidget(self)
        loadCol.addWidget(QLabel("Enter Name and Weight of items to be Loaded: "))
        loadBtn.clicked.connect(self.loadItem)
        inputSect_L.addWidget(itemLabel)
        inputSect_L.addWidget(self.inputName)
        inputSect_L.addWidget(self.weightLabel)
        inputSect_L.addWidget(self.inputWeight)
        inputSect_L.addWidget(loadBtn)
        loadCol.addLayout(inputSect_L)
        loadCol.addWidget(self.loadList)


        #[+]:-- unload column reads from the manifest and makes list-----------\\
        self.maniBtn = QtWidgets.QPushButton("Open Manifest", self)
        self.manifestList= QtWidgets.QListWidget(self)
        self.manifestList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.unloadCol_R.addWidget(QLabel("Select all items to unload: "))
        self.maniBtn.clicked.connect(self.manifest)
        self.unloadCol_R.addWidget(self.maniBtn)
        self.unloadCol_R.addWidget(self.manifestList)
        self.qBtnGroup= QtWidgets.QButtonGroup()
        # self.unloadCol_R.addWidget(self.qBtnGroup)
        # self.scrollBox = QtWidgets.QScrollArea(self)




        #[+]:-- third colum just for submit button------------------------------\\
        self.subBtn = QtWidgets.QPushButton("Generate Instructions", self)
        self.subBtn.clicked.connect(self.getLoadout)
        subCol_R.addWidget(self.subBtn)
        
    
    def manifest(self):
        manifest_Path= fd.askopenfilename()
        print("manifest_Path: "+ str(manifest_Path))
        if len(manifest_Path)>0:
            self.manifestList.clear()
            l_idx=-1
            wRegex = r'\{(-?\d+(?:\.\d+)?)\}'
            # xyRegex = r'\[(-?\d+(?:\,\d+)?)\,'
            xRegex = r'\[(-?\d+(?:\,\d+)?)\,'
            yRegex = r'\,(-?\d+(?:\,\d+)?)\]'
            # nameGex = r'\,(-?\d+(?:\,\d+)?)\]'
            
            with open(manifest_Path, "r") as file:
                for row in file:
                    if "UNUSED" not in row and "NAN" not in row:
                        l_idx+=1 
                        itemEntry= row.strip()
                        itemWeight= int(re.findall(wRegex, itemEntry)[0])
                        itemX= re.findall(xRegex, itemEntry)
                        itemY= re.findall(yRegex, itemEntry)
                        itemXYW= (int(itemX[0]), int(itemY[0]), itemWeight)
                        self.unloadItems= np.append(self.unloadItems, np.reshape(itemXYW, (1, 3)), axis= 0)

                        print("new item.type: "+ str(type(itemXYW[0]))+','+ str( type(itemXYW[1]))+','+ str( type(itemXYW[2])))
                        print("new item(x,y,weight): "+ str(itemXYW)+ "-->unloadItems")
                        print(self.unloadItems)
                            
                        tmp_Name= itemEntry[16+2:19+2]


                        unloadStr= ("["+str(tmp_Name)+"] ==> xy(" + str(itemXYW[0])+","+ str(itemXYW[1])+ ") | {" + str(itemXYW[2]) + "}Kg")
                        self.manifestList.addItem(unloadStr)
                        # self.manifestList.addItem(QtWidgets.QCheckBox(unloadStr))
                        # self.manifestList.setItemWidget(QtWidgets.QListWidgetItem(self.manifestList),QtWidgets.QCheckBox(unloadStr))

                        # radBtn= QRadioButton(unloadStr)
                        # self.manifestList.setItemWidget(QtWidgets.QListWidgetItem(self.manifestList),radBtn)
                        # self.qBtnGroup.addButton(radBtn, l_idx)
                        

                        
    def loadItem(self):
        print("list accessed")
        itemName = self.inputName.text()
        itemWeight= self.inputWeight.text()
        listInput = "+ ["+itemName+"     :     "+ itemWeight+ "] ==>[SHIP]"
        if len(listInput)+len(itemWeight)>=2:
            self.inputName.clear()
            self.inputWeight.clear()
            if "NAN" not in listInput and "Nan" not in listInput and 'nan' not in listInput: 
                if (int(itemWeight)>=0): 
                    # print(type(itemWeight))
                    # print(type(int(itemWeight)))
                    self.loadList.addItem(listInput)
                    newItem= np.reshape((itemName, itemWeight), (1,2))
                    self.loadout= np.append(self.loadout, newItem, axis=0)
                    print(str(newItem)+ " --> " + str(self.loadout))
                    print(str(self.loadout.shape)+ "\n")
                else: print('Invalid Weight entry')
            else: print("Invalid Name")
        else: print("Missing Required Field")

    # This fx should maybe modified to use the A* algo to create the instructions
    def getLoadout(self):
        if len(self.loadout)>0:
            print(self.loadout)
            return self.loadout
        else:
            print("Loadout Empty")
            
        for item in ((self.manifestList.selectedItems())):
            print(item.text())




#-[:+:]========================================Transfer CheckList -===========================================================//






class LoginPage(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        layout = QVBoxLayout()
        text_box = QLineEdit()
        confirm_login = QPushButton('Log In')
        confirm_login.setMaximumSize(150, 50)
        confirm_login.clicked.connect(lambda: self.login(text_box.text()))
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


        rez= app.primaryScreen().size()
        # window_size = (16 * 96*SIZER*1.1, 9 * 96*SIZER + 50)
        window_size = (rez.width()*SIZER, rez.height()*SIZER)
        self.setFixedSize(*window_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = Canvas()
    canvas.show()


    sys.exit(app.exec_())




