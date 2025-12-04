from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
    QPushButton, QFileDialog, QMessageBox, QWidget, QHBoxLayout, QSpinBox, QStyle
)

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

import sys, os
import urllib.parse

import regex as re

import requests
from bs4 import BeautifulSoup

#* Scrapes Wikipedia
def scrape(query):
    search_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query.strip())}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(search_url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    content_div = soup.find('div', id='mw-content-text')

    paragraphs = content_div.find_all('p', limit=5)

    summary_parts = []
    
    for p in paragraphs:
        if p.get_text().strip() and not p.find_parent('table', class_='infobox'):
            summary_parts.append(p.get_text())

    clean_summary = ' '.join(summary_parts).strip()
    clean_summary = re.sub(r'\[.*?\]', '', clean_summary)
    
    if not clean_summary:
        return f"\n\nCould not find a relevant summary on Wikipedia. ({search_url})"
    
    summary_block = (
        f"\n-{clean_summary}"
        f"\n\n"
    )

    source_url_line = f"\n-{search_url}\n"

    return summary_block, source_url_line

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
        
        self.ask_the_web_button = QPushButton("Ask the Web (Selected Text)")
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
    
    #* Uses the scraper and outputs the results
    def ask_the_web(self):

        cursor = self.text_box.textCursor()

        if cursor.hasSelection():
            query = cursor.selectedText()
            
            clean_query = query.strip()
            
            if not clean_query:
                QMessageBox.warning(self, "No Valid Selection", "Please select some meaningful text to search.")
                return
            
            try:
                scrape_res = scrape(clean_query)

                summary_block, source_url_line = scrape(clean_query)

                cursor.removeSelectedText()

                cursor.insertText(summary_block)
                
                if "Sources:" not in self.text_box.toPlainText():
                    self.text_box.append("\n\nSources:\n")

                temp_cursor = self.text_box.textCursor() 

                temp_cursor.movePosition(temp_cursor.End)

                temp_cursor.insertText(source_url_line)

                self.text_box.setTextCursor(cursor)

                self.statusBar().showMessage(f"Search complete for '{clean_query}'", 5000)
                
            except requests.exceptions.HTTPError as http_err:
                if http_err.response.status_code == 404:
                     msg = f"Wikipedia page not found for '{clean_query}'. Please try a different query."
                else:
                    msg = f"HTTP Error occurred: {http_err}"
                QMessageBox.warning(self, "Search Error", msg)
                self.statusBar().showMessage(f"Error: {http_err}", 5000)

            except requests.exceptions.RequestException as req_err:
                QMessageBox.critical(self, "Network Error", 
                                     f"Network request failed (e.g., no internet connection, timeout): {req_err}")
                self.statusBar().showMessage("Network error occurred.", 5000)

            except Exception as e:
                QMessageBox.critical(self, "Application Error", 
                                     f"An unexpected error occurred during scraping: {e}")
                self.statusBar().showMessage("An unexpected error occurred.", 5000)

        else:
            QMessageBox.information(self, "No Selection", "Please select the text you wish to search for in the text box first.")
            self.statusBar().showMessage("Action failed: No text selected.", 5000)

#* Main loop
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())