from PySide2.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QFont

TESTING_PATH = [[(3,4), (3,3),(3,2), (4,2),(5,2),(6,2),(7,2),(8,2)],
                [(1,5),(1,6),(1,7),(1,8),(1,9),(100,100),(200,100)],
                [(3,4), (3,3),(3,2), (4,2),(5,2),(6,2),(7,2),(8,2)]]

# A new winodws to show the buffer area 
class BufferWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Buffer Window")
        
        self.buffer_col = 4
        self.buffer_row = 24
        
        buffer_layout = QGridLayout()
        buffer_layout.setSpacing(0)
        self.setLayout(buffer_layout)

        for row in range(self.buffer_row):
            for col in range(self.buffer_col):
                label = QLabel()
                label.setFixedSize(96, 96)
                label.setProperty('row', row)
                label.setProperty('col', col)
                block_style = 'border: 1px solid black; '
                label.setStyleSheet(block_style)
                buffer_layout.addWidget(label, col, row)

    def update_buffer_labels(self, block_style, buffer_row, buffer_col):
        for label in self.findChildren(QLabel):
            if label.property('row') == buffer_row and label.property('col') == buffer_col:
                label.setStyleSheet(block_style)

class BlockGrid(QWidget):
    def __init__(self, rows, cols, block_size, parent=None):
        super().__init__(parent)
        
        # Set a custon start and end block for testing
        # x=4, y=1
        self._start_block = (1,2)
        # x=9, y=3
        self._end_block = (9,3)
        
        # 2 coordinates to track the path block
        self._track_block_x = self._start_block[0]
        self._track_block_y = self._start_block[1]
        
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
                
                # Algor to convert cord: x-=1, y=9-y 
                if (row + 1, 9 - col) == self._start_block:
                    block_style += 'background-color: green;'
                elif (row + 1, 9 - col) == self._end_block:
                    block_style += 'background-color: red;'
                    
                label.setStyleSheet(block_style)
                grid_layout.addWidget(label, col, row)
                
        
        # Add button to the layout
        next_button = QPushButton('Next')
        
        # Add button to the test buffer area
        test_button = QPushButton('Test')
        test_button.clicked.connect(self.show_Buffer_window)
        
        # Button holder layout
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(next_button)
        buttons_layout.addWidget(test_button)
        animation_page_layout.addLayout(buttons_layout,3)
        
        
        self.setFixedSize(15 * block_size, 9 * block_size)
                
        # Create a QTimer to update the labels every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(1000)

    # Update the labels
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
        
        # Otherwise, update the path block
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

            if hasattr(self, 'Buffer_window'):
                block_style = 'border: 1px solid black; background-color: red;'  # Customize this style as needed
                self.Buffer_window.update_buffer_labels(block_style, self._track_block_x, self._track_block_y)
            
    # Add this function to create and show the Buffer window
    def show_Buffer_window(self):
        self.Buffer_window = BufferWindow()
        self.Buffer_window.show()
