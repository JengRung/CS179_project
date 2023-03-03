import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PySide2.QtCore import Qt, QTimer

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
        button = QPushButton('Start')
        button.setMaximumSize(150, 50)
        button.clicked.connect(self.start_app)
        layout.addWidget(button)

    def start_app(self):
        # Create the block grid and add it to the stacked widget
        block_size = 96
        grid = BlockGrid(12, 9, block_size)
        self.canvas.addWidget(grid)

        # Switch to the game widget
        self.canvas.setCurrentWidget(grid)

class BlockGrid(QWidget):
    def __init__(self, rows, cols, block_size, parent=None):
        super().__init__(parent)
        
        # Set a custon start and end block for testing
        # x=4, y=1
        self._start_block = (4,5)
        # x=9, y=3
        self._end_block = (9,3)
        
        # 2 coordinates to track the path block
        self._track_block_x = self._start_block[0]
        self._track_block_y = self._start_block[1]
        
        # Create a canvas layout to hold the blocks and button 
        animation_page_layout = QHBoxLayout()
        self.setLayout(animation_page_layout)

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
        button = QPushButton('Next')
        animation_page_layout.addWidget(button, 2)
        
        self.setFixedSize(12 * block_size + 200, 9 * block_size)
                
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
                    
class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the stacked widget to hold the pages
        self.stacked_widget = QStackedWidget(self)
        
        # Create the first page widget and add it to the stacked widget
        main_page = MainPage(self.stacked_widget)
        self.stacked_widget.addWidget(main_page)

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
