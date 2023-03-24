from PySide2.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit

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
                # TODO: Need to fix the buffer area corrdinate
                label.setProperty('row', row)
                label.setProperty('col', col)
                block_style = 'border: 1px solid black; '
                label.setStyleSheet(block_style)
                buffer_layout.addWidget(label, col, row)

    def update_buffer_labels(self, block_style, buffer_row, buffer_col):
        for label in self.findChildren(QLabel):
            if label.property('row') == buffer_row/100 and label.property('col') == buffer_col/100:
                label.setStyleSheet(block_style)
                
    def clear_grid(self):
        for label in self.findChildren(QLabel):
            label.setStyleSheet('border: 1px solid black; ')
            
class BufferStorage:
    def __init__(self,):
        self.storage = [[None for x in range(24)] for y in range(4)]
    
    # Add container to the closest empty slot
    def add_item(self, item):
        for col in range(23 , -1, -1):
            for row in range(3, -1, -1):
                if self.storage[row][col] == None:
                    self.storage[row][col] = item
                    return self.get_path((col, row))
                    # return (row, col)
    
    def print(self):
        for row in range(4):
            for col in range(24):
                print(self.storage[row][col], end=' ')
            print()

    def remove_item(self, item):
        for row in range(4):
            for col in range(24):
                if self.storage[row][col] == item:
                    self.storage[row][col] = None
                    return
    
    def convert_corrdinate(self, x, y):
        new_x = 24 - x
        new_y = y + 1
        return (new_x * 100, new_y * 100)   
    
    # Return the path from the top right (23,0) to end corrdinate
    def get_path(self, end):

        path = []
        # start location
        x, y = 23, 0
        path.append(self.convert_corrdinate(x, y))
        while x > end[0]:
            x -= 1
            path.append(self.convert_corrdinate(x, y))
        
        while y < end[1]:
            y += 1
            path.append(self.convert_corrdinate(x, y))
            
        return path