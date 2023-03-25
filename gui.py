import sys
import copy
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
import container as cont
import a_star as ast
from log import LogDriver


OUTPUT_LOG_FILE = "output_log.txt"
LOGDRIVER = LogDriver(OUTPUT_LOG_FILE)

indexTionary= {
    'main': 0,
    'login': 1,
    'transfer': 2,
    'logout': 3,
}

class MainPage(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.ship_container = [[0 for x in range(12)] for y in range(9)]

        self.canvas = canvas
        
        # Create a vertical layout to hold the widgets
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Add a label to the layout
        label = QLabel('Welcome, please select a task!')
        label.setFont(QFont("Arial", 35, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        balance_button = QPushButton('Balance Task')
        balance_button.setFixedSize(300, 100)
        balance_button.setFont(QFont("Arial", 20, QFont.Bold))
        balance_button.clicked.connect(self.start_balance)
        layout.addWidget(balance_button)

        transfer_button = QPushButton('Transfer Task')
        transfer_button.setFixedSize(300, 100)
        transfer_button.setFont(QFont("Arial", 20, QFont.Bold))
        transfer_button.clicked.connect(self.start_transfer)
        layout.addWidget(transfer_button)
        
        # Add a button to login
        login_button = QPushButton('Login')
        login_button.setFixedSize(300, 100)
        login_button.setFont(QFont("Arial", 20, QFont.Bold))
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        
        # Add a button to logout
        logout_button = QPushButton('Logout')
        logout_button.setFixedSize(300, 100)
        logout_button.setFont(QFont("Arial", 20, QFont.Bold))
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

    #[:+]-- changed 'start_app' to start balance, also added 'start_transfer;  one func
    def start_balance(self):
        # Create the block grid and add it to the stacked widget
        manifest_Path= fd.askopenfilename()
        manifest_name = manifest_Path.split("/")[-1]
        print("manifest_Path: "+ str(manifest_Path))
        # Loading the manifest to self.ship_container (Done by Justin)
        with open(manifest_Path, "r") as file:
            container_pattern = r'(\[.*?\]),\s({.*?}),\s(.*)'
            container_cnt = 0
            for row in file:
                items = re.match(container_pattern, row)

                container_index, container_weight, container_name= items.groups()
                container_indexs = container_index.strip('[]').split(',')
                container_weight = int(container_weight.strip('{}'))
            
                if container_name.upper() == "NAN":
                    self.ship_container[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = -1
                
                elif container_name.upper() == "UNUSED":
                    self.ship_container[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = 0
        
                else:
                    self.ship_container[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = cont.container(container_name, container_weight)
                    container_cnt += 1
        self.ship_container.reverse()
        
        # Write to the log file when loading manifest
        LOGDRIVER.openManifest(manifest_name, container_cnt)
        
        # for row in self.ship_container:
        #     print(row)
        
        ship = cont.ship(self.ship_container)
        new_ship = None

        #Check if balance is possible
        if (ship.can_be_balanced() == False):
            print("Can not be balanced")
            #Add something to skip the rest here
        else:
            new_ship = ship.balance(ast.search,ast.balance(ship))
            #do stuff here

        if new_ship == None:
            print("A* Failure, resort to default")
            #A* Failed for some reason, do the default maritime law algo
        else:
            pass
            #do the balancing GUI stuff here

        #-------- correct order ---------------------
        balance_moves = new_ship.moves
        paths = []
        ship_temp = copy.deepcopy(ship)
        for moves in balance_moves:
            paths.append(ship_temp.shortest_path(moves))
            ship_temp.move(moves) #updates ship for next move
        #--------------------------------------------

        # reverse x, y cords
        for path in paths:
            for move in path:
                move[0], move[1] = move[1], move[0]
                move[0] = move[0] + 1
                move[1] = 9 - move[1] 
                
        # print("New ship: ", new_ship)
        
        grid = BlockGrid(parent_canvas = self.canvas, 
                         logdriver = LOGDRIVER, 
                         input_path = paths, 
                         container_status = self.ship_container, 
                         manifest_name = manifest_name)
        
        self.canvas.addWidget(grid)
        self.canvas.setCurrentWidget(grid)
        
        # Clear ship container
        self.ship_container = [[0 for x in range(12)] for y in range(9)]

    def start_transfer(self):
        self.canvas.setCurrentIndex(indexTionary['transfer']) 
        
    def login(self):
        self.canvas.setCurrentIndex(1) 
        
    def logout(self):
        self.canvas.setCurrentIndex(3)


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
        
        self.ship_container = [[0 for x in range(12)] for y in range(9)]

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
        self.maniBtn = QtWidgets.QPushButton("Select Items From Manifest", self)
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
            xRegex = r'\[(-?\d+(?:\,\d+)?)\,'
            yRegex = r'\,(-?\d+(?:\,\d+)?)\]'
            
            # For reading the manifest file for transfer list ui (Done by Richard)
            #[+]-- ---------------------------------------------------------------------------------------------------------------------------\\
            with open(manifest_Path, "r") as file:
                for row in file:
                    itemEntry= row.strip()
                    tmp_Name= itemEntry[16+2:len(itemEntry)]
                    l_idx+=1 
                    itemWeight= int(re.findall(wRegex, itemEntry)[0])
                    itemX= re.findall(xRegex, itemEntry)
                    itemY= re.findall(yRegex, itemEntry)
                    itemXYW= (int(itemX[0]), int(itemY[0]), itemWeight)
                    if tmp_Name.upper()=="NAN":
                        self.ship_container[int(itemXYW[0]) - 1][int(itemXYW[1]) - 1] = -1
                    elif tmp_Name.upper()=="UNUSED":
                        self.ship_container[int(itemXYW[0]) - 1][int(itemXYW[1]) - 1] = 0
                    
                    else:
                        self.unloadItems= np.append(self.unloadItems, np.reshape(itemXYW, (1, 3)), axis= 0)
                        unloadStr= ("["+str(tmp_Name)+"] ==> xy(" + str(itemXYW[0])+","+ str(itemXYW[1])+ ") | {" + str(itemXYW[2]) + "}Kg")
                        self.manifestList.addItem(unloadStr)
                        #[+]-- Create Ship State based on manifest: 
                        self.ship_container[int(itemXYW[0]) - 1][int(itemXYW[1]) - 1] = cont.container(tmp_Name, itemXYW[2])
                self.ship_container.reverse()
                for row in self.ship_container:
                    print(row)
            #[+]-- ---------------------------------------------------------------------------------------------------------------------------//

            # Loading the manifest to self.ship_container (Done by Justin)
            # with open(manifest_Path, "r") as file:
            #     container_pattern = r'(\[.*?\]),\s({.*?}),\s(.*)'
            #     for row in file:
            #         items = re.match(container_pattern, row)

            #         container_index, container_weight, container_name= items.groups()
            #         container_indexs = container_index.strip('[]').split(',')
            #         container_weight = int(container_weight.strip('{}'))
                
            #         if container_name.upper() == "NAN":
            #             self.ship_container[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = -1
                    
            #         elif container_name.upper() == "UNUSED":
            #             self.ship_container[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = 0
            
            #         else:
            #             self.ship_container[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = cont.container(container_name, container_weight)
            #     self.ship_container.reverse()
            #     for row in self.ship_container:
            #         print(row)





            




                    
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
                    self.loadList.addItem(listInput)
                    newItem= np.reshape((itemName, itemWeight), (1,2))
                    self.loadout= np.append(self.loadout, newItem, axis=0)
                    # print(str(newItem)+ " --> " + str(self.loadout))
                    # print(str(self.loadout.shape)+ "\n")
                else: print('Invalid Weight entry')
            else: print("Invalid Name")
        else: print("Missing Required Field")

    # This fx should maybe modified to use the A* algo to create the instructions
    def getLoadout(self):
        if len(self.loadout)+len(self.manifestList.selectedItems())>0:
            # transfer_list = []
            # for item in self.loadout:
            #     for x in range(len(self.ship_container)-1):
            #         for y in range(len(self.ship_container[x])-1):
            #             if self.ship_container[x][y] != -1 and self.ship_container[x][y] != 0:
            #                 if item[0] == self.ship_container[x][y].name:
            #                     print(self.ship_container[x][y].name, (x, y))                
            #                     transfer_list.append([x, y])


            #[+]-- Populate transfer_list with items that the user has selected to UNload fro the ship------\
            transfer_list= []
            print('\nSelected For Unloading: ')
            for item in self.manifestList.selectedItems():
                print(item.text())
                x= int((re.findall((r'\((-?\d+(?:\,\d+)?)\,'),item.text())[0]))
                y= int((re.findall((r'\,(-?\d+(?:\,\d+)?)\)'),item.text())[0])) 
                # transfer_list.append((x,y))
                transfer_list.append([9-x,y-1])
                # transfer_list= [[7,0],[7,1]]
            print("        [OUTGOING]:=======> "+ str(transfer_list))
            #-----------------------------------------------------------------------------------------------/

            
            ship = cont.ship(self.ship_container)
            balance_moves = ship.transfer_list_off(transfer_list)
            paths = []
            print(balance_moves)
            for move in balance_moves:
                paths.append(ship.shortest_path(move))
            
            # reverse x, y cords
            for path in paths:
                for move in path:
                    move[0], move[1] = move[1], move[0]
                    move[0] = move[0] + 1
                    move[1] = 9 - move[1] 
            
            print(paths)
            grid = BlockGrid(self.canvas, LOGDRIVER, paths)
            self.canvas.addWidget(grid)
            self.canvas.setCurrentWidget(grid)
            
            return self.loadout
        else:
            print("Fields are empty!")
            
            # ship = cont.ship(self.ship_container)
            # transfer_list = [[0, 3], [0, 7]]
            # moves = ship.transfer_list_off(transfer_list)
            # print(moves)


class LoginPage(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        layout = QVBoxLayout()
        text_box = QLineEdit()
        text_box.setFixedSize(1300, 200)
        text_box.setFont(QFont('Arial', 50))
        confirm_login = QPushButton('Log In')
        confirm_login.setMaximumSize(150, 50)
        confirm_login.setFont(QFont('Arial', 20))
        confirm_login.clicked.connect(lambda: self.login(text_box.text()))
        layout.addWidget(text_box)
        layout.addWidget(confirm_login)
        self.setLayout(layout)
    def login(self, username):
        if username != '':
            print(username)
            LOGDRIVER.login(username)
            self.canvas.setCurrentIndex(0)
                    
                    
class LogoutPage(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        layout = QVBoxLayout()
        confirm_logout = QLabel('Log Out Successful')
        confirm_logout.setFixedSize(1500, 500)
        confirm_logout.setFont(QFont('Arial', 50))
        
        home_button = QPushButton('Go back to home')
        home_button.setFont(QFont('Arial', 20))
        home_button.clicked.connect(self.backhome)
        
        layout.addWidget(confirm_logout)
        layout.addWidget(home_button)
        self.setLayout(layout)
        
    def backhome(self):
        LOGDRIVER.logout()
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
        
        logout_page = LogoutPage(self.stacked_widget)
        self.stacked_widget.addWidget(logout_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


        window_size = (2000, 1000)
        self.setFixedSize(*window_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = Canvas()
    canvas.show()


    sys.exit(app.exec_())