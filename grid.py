from PySide2.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide2.QtCore import QTimer
from PySide2.QtGui import QFont

from buffer import BufferWindow

TESTING_PATH = [[(3,4), (3,3),(3,2), (4,2),(5,2),(6,2),(7,2),(8,2),(-2,-2)],
                [(3,7),(3,8),(3,9),(3,10),(4,10),(5,10),(6,10),(6,9),(6,8)],
                [(1,5),(1,6),(1,7),(1,8),(1,9),(100,100),(200,100),(300,100),(400,100)],
                [(2,6), (3,6), (4,6), (5,6), (-2,-2), (6,6), (7,6), (8,6), (9,6), (9,7)],
                [(11,3), (10,3), (9,3), (8,3), (7,3), (6,3), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9)],
                [(1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5)]]

class BlockGrid(QWidget):
    def __init__(self, parent_canvas, driver, parent=None):
        super().__init__(parent)
        
        self.path = TESTING_PATH
        self.driver = driver
        
        rows = 12
        
        # 9 cols + 1 for above the ship area
        cols = 10
        
        # Set the default block_size to 96
        block_size = 96
        
        self.parent_canvas = parent_canvas
        
        # Count how many path have already complete, use to track the current path when update
        self.finish_path = 0
        
        # Index to track the current block in the path
        self.path_index = 0
        
        # 2 coordinates to track the path block
        self._track_block_x = self.path[self.finish_path][0][0]
        self._track_block_y = self.path[self.finish_path][0][1]
        
        # Create a canvas layout to hold the blocks and button 
        animation_page_layout = QHBoxLayout()
        self.setLayout(animation_page_layout)
        
        # Create the buffer and truck blocks and add them to the layout
        buffer_truck_layout = QGridLayout()
        buffer_truck_layout.setSpacing(0)
        animation_page_layout.addLayout(buffer_truck_layout)
        
        buffer_block = QLabel()
        truck_block = QLabel()
        
        # Specify the font size and boldness
        buffer_block.setText('Buffer')
        truck_block.setText('Truck')
        
        font = QFont()
        font.setPointSize(12)  # Set the desired font size here
        font.setBold(True)  # Set the font to bold (optional)

        buffer_block.setFont(font)
        truck_block.setFont(font)
        
        buffer_block.setFixedSize(block_size, block_size)
        truck_block.setFixedSize(block_size, block_size)
        
        block_style = 'border: 1px solid black; '
        buffer_block.setStyleSheet(block_style)
        truck_block.setStyleSheet(block_style)
        
        # Set buffer and truck block property to -3, -2 to avoid conflict with the grid
        buffer_block.setProperty('row', -3)
        buffer_block.setProperty('col', -3)
        
        truck_block.setProperty('row', -2)
        truck_block.setProperty('col', -2)
        
        buffer_truck_layout.addWidget(buffer_block, 0, 0)
        buffer_truck_layout.addWidget(truck_block, 0, 1)
        

        # Create a grid layout to hold the blocks
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        animation_page_layout.addLayout(grid_layout)
        
        # Add the blocks to the grid layout
        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                label.setFixedSize(block_size, block_size)
                transfered_row = row + 1
                transfered_col = 10 - col
                label.setProperty('row', transfered_row)
                label.setProperty('col', transfered_col)
                
                if col == 0:
                    block_style = 'border: none; background-color: transparent;'
                else:
                    block_style = 'border: 1px solid black; '

                label.setStyleSheet(block_style)
                grid_layout.addWidget(label, col, row)
                
        
        # Update the initial block and reset the path color
        self.update_blocks_color()
        
        # Add button to the layout
        next_button = QPushButton('Next')
        next_button.setFixedSize(300, 150)
        next_button.setFont(QFont("Arial", 20, QFont.Bold))
        next_button.clicked.connect(self.next_path)
        
        # Button holder layout
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(next_button)
        animation_page_layout.addLayout(buttons_layout,3)
        
        
        self.setFixedSize(25 * block_size, 10 * block_size)
        
        # Call the buffer window if needed, this only run for the first path
        if self.buffer_require():
            self.show_Buffer_window()
                
        # Create a QTimer to update the labels every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(500)

    def update_blocks_color(self):
        for label in self.findChildren(QLabel):
            row = label.property('row')
            col = label.property('col')
            
            block_style = 'border: 1px solid black; '
            if col == 10:
                block_style = 'border: none; background-color: transparent;'
            elif (row, col) == (self.path[self.finish_path][0][0], self.path[self.finish_path][0][1]):
                block_style += 'background-color: green;'
            elif (row,col) == (self.path[self.finish_path][-1][0], self.path[self.finish_path][-1][1]):
                block_style += 'background-color: yellow;'
            label.setStyleSheet(block_style)
    
    # Update the labels
    def update_labels(self):
        
        # print(self._track_block_x, self._track_block_y)
        
        # Finish one cycle of path, clear the color and tracking block
        if self.path_index == len(self.path[self.finish_path]):
            print("Finish one cycle")
            self.path_index = 0
            
            # Reset the tracking block to initial position
            self._track_block_x = self.path[self.finish_path][self.path_index][0]
            self._track_block_y = self.path[self.finish_path][self.path_index][1]
            
            # Update the initial block and reset the path color
            self.update_blocks_color()
                
            # Reset the buffer window
            if self.buffer_require():
                self.Buffer_window.clear_grid()
        
        # Otherwise, update the path block
        else:            
            self._track_block_x = self.path[self.finish_path][self.path_index][0]
            self._track_block_y = self.path[self.finish_path][self.path_index][1]
            
            # Skip the first and last block
            if self.path_index != 0 and self.path_index != len(self.path[self.finish_path]) - 1:
                if self._track_block_x < 100:
                    for label in self.findChildren(QLabel):
                        row = label.property('row')
                        col = label.property('col')
                        
                        if (row , col) == (self._track_block_x, self._track_block_y):
                            label.setStyleSheet('border: 1px solid black; background-color: red;')
                        elif row == self._track_block_x and col == self._track_block_y:
                            label.setStyleSheet('border: 1px solid black; background-color: red;')
                            
                else:
                    if hasattr(self, 'Buffer_window'):
                        block_style = 'border: 1px solid black; background-color: red;'  # Customize this style as needed
                        self.Buffer_window.update_buffer_labels(block_style, self._track_block_x, self._track_block_y)
            # Inceament the path index
            self.path_index += 1


    def next_path(self):
        self.finish_path += 1
        self.path_index = 0
        
        if self.finish_path == len(self.path) -1:
            finish_page = FinishPage(self.parent_canvas)
            # Set the finish page as index 5
            self.parent_canvas.insertWidget(5, finish_page)
            self.parent_canvas.setCurrentIndex(5)
            self.deleteLater()

            return
                
        if hasattr(self, 'Buffer_window'):
            self.Buffer_window.close()
                
        # Check if the current path require buffer
        if self.buffer_require():
            self.show_Buffer_window()
        
        # Clear blocks color
        self.update_blocks_color()

    # A helper function to check if the current path require buffer
    def buffer_require(self):
        for corr in self.path[self.finish_path]:
            if corr[0] > 100:
                return True
        return False
    
    # Add this function to create and show the Buffer window
    def show_Buffer_window(self):
        self.Buffer_window = BufferWindow()
        self.Buffer_window.show()

class FinishPage(QWidget):
    def __init__(self, parent_canvas, parent=None):
        super().__init__(parent)
        
        self.parent_canvas = parent_canvas
        
        # Create a QVBoxLayout to hold the finish message and a button to go back
        finish_page_layout = QVBoxLayout()
        self.setLayout(finish_page_layout)

        # Add a QLabel to display the finish message
        finish_message = QLabel("Transfer task is done! Remember to send the manifest to the ship company.")
        finish_message.setFont(QFont("Arial", 25, QFont.Bold))
        finish_page_layout.addWidget(finish_message)

        # Add a QPushButton to go back to the main page
        back_button = QPushButton("Back to home page")
        back_button.setFixedSize(800, 100)
        back_button.setFont(QFont("Arial", 20, QFont.Bold))
        back_button.clicked.connect(self.go_back)
        finish_page_layout.addWidget(back_button)

    def go_back(self):
        self.parent_canvas.setCurrentIndex(0)

'''
Algor:
    1. Sort all the block base on the ship, buffer area and truck
    2. If there is only ship, cost = # of ship_block - 1
    3. If there is ship and truck, cost = # of ship_block - 1 + 2 (for ship to truck)
    4: If there is ship and buffer, cost = # of ship_block - 1 + 4 (for ship to buffer) + # of buffer_block - 1
'''
def cost_calculator(paths):
    
    arr_costs = []
    for path in paths:
        
        blocks = {"truck": 0, "buffer": 0, "ship": 0}
        for move in path:
            if move[0] == -2:
                blocks["truck"] += 1
            elif move[0] >= 100:
                blocks["buffer"] += 1
            else:
                blocks["ship"] += 1

        total_cost = blocks["ship"] - 1
        if blocks["truck"] == 1:
            total_cost += 2
        elif blocks["buffer"] > 0:
            total_cost += blocks["buffer"] - 1
            total_cost += 4
        
        arr_costs.append(total_cost)

    return arr_costs