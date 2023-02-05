import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class SearchArticleApprovs(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recherche d'un article pour l'achat")
        self.setWindowIcon((QIcon("icons/icon.ico")))
        self.setGeometry(750, 350, 950, 750)
        self.setFixedSize(self.size())
        self.set_ui()
        #self.show()
        ## set the dialog as a modal popup
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def set_ui(self):
        self.define_widgets()
        self.define_layouts()
        self.display_articles_dispo()

    def define_widgets(self):
        self.searchArticleTxt = QLineEdit()
        self.searchArticleTxt.setPlaceholderText("saisir la désignation.....")
        self.btn_Add = QPushButton("Ajouter sur facture")
        self.tblSearchArticleApprovs = QTableWidget()
        self.tblSearchArticleApprovs.setColumnCount(5)
        self.tblSearchArticleApprovs.setColumnHidden(0, True)
        self.tblSearchArticleApprovs.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tblSearchArticleApprovs.setHorizontalHeaderItem(1, QTableWidgetItem("Désignation"))
        self.tblSearchArticleApprovs.setHorizontalHeaderItem(2, QTableWidgetItem("Unité Mesure"))
        self.tblSearchArticleApprovs.setHorizontalHeaderItem(3, QTableWidgetItem("Qté stock"))
        self.tblSearchArticleApprovs.setHorizontalHeaderItem(4, QTableWidgetItem("PU"))
        self.tblSearchArticleApprovs.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.testFont = QLabel("Test de police vrai")
        self.testFont.setFont(QFont("Arial", 11))

        #self.tblSearchArticleApprovs.doubleClicked.connect(self.selected_article)

    def define_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        ############## add widgets to layouts #############
        self.topLayout.addWidget(self.searchArticleTxt)
        self.topLayout.addWidget(self.btn_Add)
        self.bottomLayout.addWidget(self.tblSearchArticleApprovs)
        self.bottomLayout.addWidget(self.testFont)
        ############## Add layouts to main layput #########
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)


    def display_articles_dispo(self):
        self.tblSearchArticleApprovs.setFont(QFont("Comic sans serif", 10))
        for i in reversed(range(self.tblSearchArticleApprovs.rowCount())):
            self.tblSearchArticleApprovs.removeRow(i)

        query = cur.execute("SELECT id, title, unit_measure, stock_quantity, unit_price FROM articles WHERE stock_quantity > 0 ORDER BY title")
        for row_data in query:
            row_number = self.tblSearchArticleApprovs.rowCount()
            self.tblSearchArticleApprovs.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tblSearchArticleApprovs.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.tblSearchArticleApprovs.setEditTriggers(QAbstractItemView.NoEditTriggers)