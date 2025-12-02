from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
    QPushButton, QFileDialog, QMessageBox, QWidget, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

import sys, os, urllib.parse
import requests
from bs4 import BeautifulSoup

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
    
    if not clean_summary:
        return f"\n\nCould not find a relevant summary on Wikipedia. ({search_url})"
        
    return (
        f"\n-{clean_summary}"
        f"\n--------------------------------------------\n"
        f"Source: Wikipedia ({search_url})"
    )

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

            self.statusBar().showMessage(f"Searching Wikipedia for: '{clean_query}'...", 0)
            
            try:
                result_text = scrape(clean_query)
                
                self.text_box.append(result_text)
                self.statusBar().showMessage(f"Search complete for '{clean_query}'", 5000)
                
            except requests.exceptions.HTTPError as http_err:
                if http_err.response.status_code == 404:
                     msg = f"Wikipedia page not found for '{clean_query}'. Please try a different query."
                else:
                    msg = f"HTTP Error occurred: {http_err}"
                QMessageBox.warning(self, "Scraping Error", msg)
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())