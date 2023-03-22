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