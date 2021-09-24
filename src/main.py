from io import SEEK_CUR
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import requests
from bs4 import BeautifulSoup
import re

# Wikpedia Kelime Verisi Çekici

class Window(QWidget):
    def __init__(self, title, shape, icon):
        super().__init__()
        self.title = title
        self.x, self.y, self.w, self.h = shape
        self.icon = QIcon(icon)
        self.vbox = QVBoxLayout()
        self.initUI()
        self.setLayout(self.vbox)

    def GetWords(self):
        url = self.urlTextBox.text()
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html.parser')

        paragraphs = soup.find_all("p")
        allText = ""

        for paragraph in paragraphs:
            allText += paragraph.text

        allText = allText.strip()
        words = allText.split(" ")
        return words

    def ClearWords(self, words):
        clearWords = []
        for word in words:
            letters = re.findall("\W+|\d+", word)
            for letter in letters:
                word = word.replace(letter, "")
            if len(word) > 0:
                clearWords.append(word)
        return clearWords

    def SortWords(self, words):
        sortedWords = {}
        words.sort()

        for word in words:
            if word in sortedWords:
                sortedWords[word] += 1
            else:
                sortedWords[word] = 1
        
        return sortedWords

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.w, self.h)
        self.setWindowIcon(self.icon)
        
        self.label = QLabel(text="Enter Wikipedia Url: ")
        self.vbox.addWidget(self.label)

        self.urlTextBox = QLineEdit()
        self.vbox.addWidget(self.urlTextBox)

        self.getBtn = QPushButton(text="Get Data", clicked=lambda : self.GetData())
        self.vbox.addWidget(self.getBtn)

        self.list = QListWidget()
        self.vbox.addWidget(self.list)

    def GetData(self):
        words = self.GetWords()
        words = self.ClearWords(words)
        words = self.SortWords(words)

        for word, number in words.items():
            item = "{}[{}]".format(word, number)
            self.list.addItem(QListWidgetItem(item))


app = QApplication(sys.argv)
dialog = Window("Wikipedia Data Taker", (100, 100, 500, 500), "../img/icon.jpg")
dialog.show()
app.exec_()