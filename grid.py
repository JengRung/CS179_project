from PySide2.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide2.QtCore import QTimer
from PySide2.QtGui import QFont

from buffer import BufferWindow

TESTING_PATH = [[(3,4), (3,3),(3,2), (4,2),(5,2),(6,2),(7,2),(8,2)],
                [(1,5),(1,6),(1,7),(1,8),(1,9),(100,100),(200,100),(300,100),(400,100)],
                [(2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6), (9,6), (9,7)],
                [(11,3), (10,3), (9,3), (8,3), (7,3), (6,3), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9)],
                [(1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5)]]

class BlockGrid(QWidget):
    def __init__(self, rows, cols, block_size, parent=None):
        super().__init__(parent)
        
        # Count how many path have already complete, use to track the current path when update
        self.finish_path = 0
        
        # Index to track the current block in the path
        self.path_index = 0
        
        # 2 coordinates to track the path block
        self._track_block_x = TESTING_PATH[self.finish_path][0][0]
        self._track_block_y = TESTING_PATH[self.finish_path][0][1]
        
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
        
        # Set buffer and truck block property to -1, -2 to avoid conflict with the grid
        buffer_block.setProperty('row', -1)
        buffer_block.setProperty('col', -1)
        
        truck_block.setProperty('row', -2)
        truck_block.setProperty('col', -2)
        
        buffer_truck_layout.addWidget(buffer_block, 0, 1)
        buffer_truck_layout.addWidget(truck_block, 0, 0)
        

        # Create a grid layout to hold the blocks
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        animation_page_layout.addLayout(grid_layout)
        
        # Add the blocks to the grid layout
        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                label.setFixedSize(block_size, block_size)
                label.setProperty('row', row)
                label.setProperty('col', col)
                block_style = 'border: 1px solid black; '

                if (row + 1, 9 - col) == (TESTING_PATH[self.finish_path][0][0], TESTING_PATH[self.finish_path][0][1]):
                    block_style += 'background-color: green;'
                elif (row + 1, 9 - col) == (TESTING_PATH[self.finish_path][-1][0], TESTING_PATH[self.finish_path][-1][1]):
                    block_style += 'background-color: yellow;'
                    
                label.setStyleSheet(block_style)
                grid_layout.addWidget(label, col, row)
                
        
        # Add button to the layout
        next_button = QPushButton('Next')
        next_button.clicked.connect(self.next_path)
        
        # Add button to the test buffer area
        test_button = QPushButton('Test')
        test_button.clicked.connect(self.show_Buffer_window)
        
        # Button holder layout
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(next_button)
        buttons_layout.addWidget(test_button)
        animation_page_layout.addLayout(buttons_layout,3)
        
        
        self.setFixedSize(15 * block_size, 9 * block_size)
        
        # Call the buffer window if needed, this only run for the first path
        if self.buffer_require():
            self.show_Buffer_window()
                
        # Create a QTimer to update the labels every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(500)

    # Update the labels
    def update_labels(self):
        
        # print(self._track_block_x, self._track_block_y)
        
        # Finish one cycle of path, clear the color and tracking block
        if self.path_index == len(TESTING_PATH[self.finish_path]):
            print("Finish one cycle")
            self.path_index = 0
            
            # Reset the tracking block to initial position
            self._track_block_x = TESTING_PATH[self.finish_path][self.path_index][0]
            self._track_block_y = TESTING_PATH[self.finish_path][self.path_index][1]
            
            # Update the initial block and reset the path color
            for label in self.findChildren(QLabel):
                row = label.property('row')
                col = label.property('col')
                
                block_style = 'border: 1px solid black; '
                if (row + 1, 9 - col) == (TESTING_PATH[self.finish_path][0][0], TESTING_PATH[self.finish_path][0][1]):
                    block_style += 'background-color: green;'
                elif (row + 1, 9 - col) == (TESTING_PATH[self.finish_path][-1][0], TESTING_PATH[self.finish_path][-1][1]):
                    block_style += 'background-color: yellow;'
                label.setStyleSheet(block_style)
                
            # Reset the buffer window
            if self.buffer_require():
                self.Buffer_window.clear_grid()
        
        # Otherwise, update the path block
        else:            
            self._track_block_x = TESTING_PATH[self.finish_path][self.path_index][0]
            self._track_block_y = TESTING_PATH[self.finish_path][self.path_index][1]
            
            # Skip the first and last block
            if self.path_index != 0 and self.path_index != len(TESTING_PATH[self.finish_path]) - 1:
                if self._track_block_x < 100:
                    for label in self.findChildren(QLabel):
                        row = label.property('row')
                        col = label.property('col')
                        if (row + 1, 9 - col) == (self._track_block_x, self._track_block_y):
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
                
        if hasattr(self, 'Buffer_window'):
            self.Buffer_window.close()
                
        # Check if the current path require buffer
        if self.buffer_require():
            self.show_Buffer_window()
        
        # Clear blocks color
        for label in self.findChildren(QLabel):
            row = label.property('row')
            col = label.property('col')
            
            block_style = 'border: 1px solid black; '
            if (row + 1, 9 - col) == (TESTING_PATH[self.finish_path][0][0], TESTING_PATH[self.finish_path][0][1]):
                block_style += 'background-color: green;'
            elif (row + 1, 9 - col) == (TESTING_PATH[self.finish_path][-1][0], TESTING_PATH[self.finish_path][-1][1]):
                block_style += 'background-color: yellow;'
            label.setStyleSheet(block_style)

    # A helper function to check if the current path require buffer
    def buffer_require(self):
        for corr in TESTING_PATH[self.finish_path]:
            if corr[0] > 100:
                return True
        return False
    
    # Add this function to create and show the Buffer window
    def show_Buffer_window(self):
        self.Buffer_window = BufferWindow()
        self.Buffer_window.show()
