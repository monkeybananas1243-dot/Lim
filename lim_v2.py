from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
import sys, os

from datasets import load_dataset

streaming_dataset = load_dataset("HuggingFaceFW/fineweb", streaming=True)
full_train_stream = streaming_dataset['train']

train_data_subset = full_train_stream.skip(10000).take(100)
train_data = list(train_data_subset)

validation_data_subset = full_train_stream.take(10)
validation_data = list(validation_data_subset)

print(f"Loaded {len(train_data)} training items and {len(validation_data)} validation items.")

print(train_data[1]["text"])

"""train_ds = tf.keras.utils.text_dataset_from_directory(
    'path/to/train_directory',
    batch_size=32,
    validation_split=0.2,
    subset='training',
    seed=123
)"""

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

        self.ask_ai_button = QPushButton("Ask AI", self)
        self.ask_ai_button.setFont(QFont("Helvectica", 8))
        self.ask_ai_button.setStyleSheet("QPushButton { border-radius: 10px; border: 1px solid gray; background-color: white; }")
        self.ask_ai_button.setGeometry(self.WIDTH//2, 0, 70, 40)
        self.ask_ai_button.clicked.connect(self.ask_ai)

        layout.addWidget(self.text_box)
        layout.addWidget(self.save_normal_file_button)
        
        layout.addWidget(self.ai_text_box)

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
    
    def ask_ai(self):
        text_box_contents = self.text_box.toPlainText()

        opening_prompt = -1
        closing_prompt = -1
        for i in range(len(text_box_contents) - 1):
            if text_box_contents[i:i+2] == "-/":
                opening_prompt = i + 2
            elif text_box_contents[i:i+2] == "/-":
                closing_prompt = i - 1
        
        if opening_prompt == -1 and closing_prompt == -1:
            return

        prompt = text_box_contents[opening_prompt:closing_prompt].strip()
        print(prompt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())