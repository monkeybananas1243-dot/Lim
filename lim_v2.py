from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
import sys, os

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
        self.text_box.setGeometry(0, 50, self.WIDTH//2, self.HEIGHT-50)
        self.text_box.setStyleSheet("QTextEdit { border-radius: 10px; border: 1px solid gray; background-color: white; }")
        self.text_box.setFont(self.base_font)

        self.save_normal_file_button = QPushButton("Save", self)
        self.save_normal_file_button.setFont(QFont("Helvectica", 8))
        self.save_normal_file_button.setStyleSheet("QPushButton { border-radius: 10px; border: 1px solid gray; background-color: white; }")
        self.save_normal_file_button.setGeometry(0, 0, 70, 40)
        self.save_normal_file_button.clicked.connect(self.save_file)

        self.ai_text_box = QTextEdit(self)
        self.ai_text_box.setGeometry(self.WIDTH//2, 50, self.WIDTH//2, self.HEIGHT-50)
        self.ai_text_box.setStyleSheet("QTextEdit { border-radius: 10px; border: 1px solid gray; background-color: white; }")
        self.ai_text_box.setFont(self.base_font)

        self.ask_the_web_button = QPushButton("Ask the Web", self)
        self.ask_the_web_button.setFont(QFont("Helvectica", 8))
        self.ask_the_web_button.setStyleSheet("QPushButton { border-radius: 10px; border: 1px solid gray; background-color: white; }")
        self.ask_the_web_button.setGeometry(self.WIDTH//2, 0, 70, 40)

        layout.addWidget(self.text_box)
        layout.addWidget(self.save_normal_file_button)
        
        layout.addWidget(self.ask_the_web_button)

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
    
    def ask_the_web(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())