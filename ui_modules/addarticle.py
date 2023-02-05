import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class AddArticle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter un nouvel article")
        self.setWindowIcon((QIcon("icons/icon.ico")))
        self.setGeometry(600, 500, 650, 750)
        self.setFixedSize(self.size())
        self.set_ui()
        self.show()

    def set_ui(self):
        self.define_widgets()
        self.define_layouts()

    def define_widgets(self):
        ############ widgets of top layout ###########
        self.addArticleImg = QLabel()
        self.img = QPixmap("icons/addmember.png")
        self.addArticleImg.setPixmap(self.img)
        self.titleTxt = QLabel("Ajout article")
        self.titleTxt.setStyleSheet("font-weight: bold; font-size: 16pt;")
        ############# widgets of bottom layout ########
        self.txtArticleTitle = QLineEdit()
        self.txtArticleTitle.setPlaceholderText("Entrer nom'article")
        self.txtUM = QLineEdit()
        self.txtUM.setPlaceholderText("Entrer l'unité de mesure")
        self.txtStockMin = QLineEdit()
        self.txtStockMin.setPlaceholderText("Entrer le niveau de stock min")
        self.txtQtyStock = QLineEdit()
        self.txtQtyStock.setPlaceholderText("Entrer la quantité disponible")
        self.txtPU = QLineEdit()
        self.txtPU.setPlaceholderText("Entrer le prix unitaire")
        self.btn_submit = QPushButton("Valider")
        self.btn_submit.clicked.connect(self.insert_article)

    def define_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame =QFrame()
        self.bottomFrame =QFrame()
        ############## Add widgets #################
        ########### Widgets of top layout #########
        self.topLayout.addWidget(self.addArticleImg)
        self.topLayout.addWidget(self.titleTxt)
        self.topFrame.setLayout(self.topLayout)
        ########### Widgets of bottom layout #########
        self.bottomLayout.addRow(QLabel("Désignation:"), self.txtArticleTitle)
        self.bottomLayout.addRow(QLabel("Unité mesure:"), self.txtUM)
        self.bottomLayout.addRow(QLabel("Stock Mmnimum:"), self.txtStockMin)
        self.bottomLayout.addRow(QLabel("Quantité en stock:"), self.txtQtyStock)
        self.bottomLayout.addRow(QLabel("Prix unitaire:"), self.txtPU)
        self.bottomLayout.addRow("", self.btn_submit)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def insert_article(self):
            article_title = self.txtArticleTitle.text()
            unit_measure = self.txtUM.text()
            stock_min = self.txtStockMin.text()
            qty_stock = self.txtQtyStock.text()
            pu = self.txtPU.text()

            if article_title and stock_min != "":
                try:
                    query = "INSERT INTO articles(title, unit_measure, minimum_stock, stock_quantity, unit_price) VALUES(?,?,?,?,?)"
                    cur.execute(query, (article_title, unit_measure, stock_min, qty_stock, pu))
                    conn.commit()
                    QMessageBox.information(self, "Succès !!!", "Article ajouté avec succès.")
                    self.close()
                except:
                    QMessageBox.critical(self, "Attention !!!", "L'article n'a pas été ajouté !")
            else:
                QMessageBox.warning(self, "Avertissement !!!", "Vérifiez les champs obligatoires !")
