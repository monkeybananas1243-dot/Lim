from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.base_font = QFont("Helvectica", 12)
        
        self.setWindowTitle("Lim - Untitled")
        self.WIDTH, self.HEIGHT = 400, 400
        self.setGeometry(500, 400, self.WIDTH, self.HEIGHT)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.text_box = QTextEdit(self)
        self.text_box.setGeometry(0, 50, self.WIDTH, self.HEIGHT-50)
        self.text_box.setFont(self.base_font)

        self.save_button = QPushButton("Save", self)
        self.save_button.setFont(QFont("Helvectica", 8))
        self.save_button.setGeometry(0, 0, 70, 40)
        self.save_button.clicked.connect(self.save_file)

        layout.addWidget(self.text_box)
        layout.addWidget(self.save_button)

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
                QMessageBox.information(self, "Try again..", "Error saving file: {e}")
                QMessageBox.setFont(self.base_font)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())