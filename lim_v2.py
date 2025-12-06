from PyQt5.QtWidgets import ( 
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
    QPushButton, QFileDialog, QMessageBox, QWidget, QHBoxLayout, QSpinBox, QStyle
)

from PyQt5.QtGui import QFont, QIcon 
from PyQt5.QtCore import Qt, QSize 

import sys, os
import urllib.parse

class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        self.setWindowTitle("Lim - Untitled")
        self.base_font = QFont("Arial", 10)
        
        self.resize(800, 600)
        self.setMinimumSize(QSize(400, 300))
        
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        button_bar = QWidget()
        button_layout = QHBoxLayout(button_bar)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        self.save_normal_file_button = QPushButton("Save (Ctrl+S)")
        self.save_normal_file_button.setFont(self.base_font)
        self.save_normal_file_button.setToolTip("Save the current document")
        self.save_normal_file_button.clicked.connect(self.save_file)
        button_layout.addWidget(self.save_normal_file_button)

        self.set_font_size_box = QSpinBox()
        self.set_font_size_box.setToolTip("Change font of the main text-box.")
        self.set_font_size_box.setMinimum(8)
        self.set_font_size_box.setMaximum(72)
        self.set_font_size_box.setValue(10)
        self.set_font_size_box.setSingleStep(1)
        self.set_font_size_box.valueChanged.connect(lambda value: self.text_box.setFont(QFont("Arial", value)))
        button_layout.addWidget(self.set_font_size_box)
        
        button_layout.addStretch(1)

        main_layout.addWidget(button_bar)
        
        self.text_box = QTextEdit(self)
        self.text_box.setFont(self.base_font)
        self.text_box.setPlaceholderText("Start writing here.")
        main_layout.addWidget(self.text_box)
        
        self.text_box.setAcceptRichText(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:

            modifiers = event.modifiers()
            target_modifiers = Qt.ControlModifier

            if modifiers & target_modifiers:
                self.save_file()

                event.accept()
                return
        
        super().keyPressEvent(event)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self,
            "Save File",
            "",
            "Text Files (*.txt);;All Files (*)"
            )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(self.text_box.toPlainText())
            except Exception as e:
                QMessageBox.information(self, "Try again..", f"Error saving file: {e}")
                QMessageBox.setFont(self.base_font)
            
            file_name_ = os.path.basename(filename)

            self.setWindowTitle(f"Lim - {file_name_}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())