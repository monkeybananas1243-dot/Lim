from PyQt5.QtWidgets import ( 
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
    QPushButton, QFileDialog, QMessageBox, QWidget, QHBoxLayout, QSpinBox, QStyle
)

from PyQt5.QtGui import QFont, QIcon 
from PyQt5.QtCore import Qt, QSize 

import sys, os
import urllib.parse

import wikipedia # type: ignore


def api_scrape(query):
    try:
        wikipedia.set_lang("en") 
            
        page = wikipedia.page(query, auto_suggest=False)
        
        summary_text = wikipedia.summary(query, sentences=3, auto_suggest=False)
        
        summary_block = (
            f"\n-{summary_text}"
            f"\n\n"
        )
        source_url_line = f"\n-{page.url}\n"
        
        return summary_block, source_url_line

    except wikipedia.exceptions.PageError:
        return "\n\nCould not find a relevant page on Wikipedia.", None
        
    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:5])
        return f"\n\nQuery '{query}' is ambiguous. Try a more specific term. Options include: {options}", None

    except Exception as e:
        
        return f"\n\nAn unexpected API error occurred: {e}", None

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
        
        self.ask_the_web_button = QPushButton("Ask the Wiki (Selected Text)")
        self.ask_the_web_button.setFont(self.base_font)
        self.ask_the_web_button.setToolTip("Scrape Wikipedia using the currently selected text as the query.")
        self.ask_the_web_button.clicked.connect(self.ask_the_web)
        button_layout.addWidget(self.ask_the_web_button)
        
        button_layout.addStretch(1)

        main_layout.addWidget(button_bar)
        
        self.text_box = QTextEdit(self)
        self.text_box.setFont(self.base_font)
        self.text_box.setPlaceholderText("Start writing here, or select text and click 'Ask the Web' to search Wikipedia.")
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
    
    def ask_the_web(self):

        cursor = self.text_box.textCursor()

        if cursor.hasSelection():
            query = cursor.selectedText()
            clean_query = query.strip()
            
            if not clean_query:
                QMessageBox.warning(self, "No Valid Selection", "Please select some meaningful text to search.")
                return
            
            summary_or_error, source_url_line = api_scrape(clean_query)
            
            if source_url_line is None:
                
                cursor.removeSelectedText()
                cursor.insertText(summary_or_error) 
                
                self.statusBar().showMessage(f"Search failed for '{clean_query}' (See error in text box)", 5000)
                
                QMessageBox.warning(self, "Search Failed", f"Wikipedia lookup failed. Details in text box or status bar.")
            
            else:
                
                summary_block = summary_or_error 

                cursor.removeSelectedText()
                cursor.insertText(summary_block)
                
                if "Sources:" not in self.text_box.toPlainText():
                    self.text_box.append("\n\nSources:\n")
                
                temp_cursor = self.text_box.textCursor() 
                temp_cursor.movePosition(temp_cursor.End)
                temp_cursor.insertText(source_url_line)
                
                self.text_box.setTextCursor(cursor)

                self.statusBar().showMessage(f"Search complete for '{clean_query}'", 5000)

        else:
            QMessageBox.information(self, "No Selection", "Please select the text you wish to search for in the text box first.")
            self.statusBar().showMessage("Action failed: No text selected.", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())