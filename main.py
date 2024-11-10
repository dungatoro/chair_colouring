import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QFont

class RGBColorPicker(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Colour Picker")
        self.setGeometry(100, 100, 400, 400)
        self.setFixedSize(400, 240)

        self.sliders = {c: QSlider(Qt.Horizontal) for c in "RGB"}
        for slider in self.sliders.values():
            slider.setMaximum(255)
            slider.valueChanged.connect(self.update_color)

        self.colour_squares = {"normal": QLabel(), "inverse": QLabel()}
        for label in self.colour_squares.values():
            label.setFixedSize(100, 100)

        font = QFont("Cartograph CF", 10)
        font.setPointSize(10)  # Adjust font size for the labels
        
        # Label to display the RGB values
        self.rgb_label = QLabel()
        self.rgb_label.setFont(font)

        self.update_color()  # Initialize with the default color

        # Layout for the color controls (title and sliders in a horizontal layout)
        layout = QVBoxLayout()

        # Add labels and sliders
        for colour, slider in self.sliders.items():
            colour_layout = QHBoxLayout()
            colour_label = QLabel(colour)
            colour_label.setFont(font)  # Apply smaller font
            colour_layout.addWidget(colour_label)
            colour_layout.addWidget(slider)
            layout.addLayout(colour_layout)

        color_preview_layout = QHBoxLayout()
        for label in self.colour_squares.values():
            color_preview_layout.addWidget(label)

        layout.addLayout(color_preview_layout)
        layout.addWidget(self.rgb_label)

        # Set the main layout
        self.setLayout(layout)

    def update_color(self):
        # Get the RGB values from the sliders
        r, g, b = (c.value() for c in self.sliders.values())

        # Update the color preview labels with the selected colors
        for name, colour in [("normal", QColor(r, g, b)), 
                             ("inverse", QColor(255-r, 255-g, 255-b))]:
            pixmap = QPixmap(100, 100)
            pixmap.fill(colour)
            self.colour_squares[name].setPixmap(pixmap)

        # Convert RGB values to binary format (8-bit)
        r_bin, g_bin, b_bin = map( lambda c: format(c, '08b'), (r, g, b))
    
        # Update the RGB values label, display them in binary format
        self.rgb_label.setText(f"{r_bin} {g_bin} {b_bin}")
        
        count_1s = lambda s: s.count('1')
        if sum(map(count_1s, [r_bin, g_bin, b_bin])) == 12:
            self.rgb_label.setStyleSheet("color: black;") 
        else:
            self.rgb_label.setStyleSheet("color: red;") 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    picker = RGBColorPicker()
    picker.show()
    sys.exit(app.exec_())

