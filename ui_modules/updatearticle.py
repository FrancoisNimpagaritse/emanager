import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class UpdateArticle(QWidget):
    def __init__(self, articleId):
        super().__init__()
        self.setWindowTitle("Détails données fournisseur")
        self.setWindowIcon((QIcon("icons/icon.ico")))
        self.setGeometry(600, 500, 650, 750)
        self.setFixedSize(self.size())
        self.articleId = articleId
        self.set_ui()
        self.show()

    def set_ui(self):
        self.define_widgets()
        self.define_layouts()
        self.article_details()

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
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.delete_article)
        self.btn_update = QPushButton("Modifier")
        self.btn_update.clicked.connect(self.update_article)

    def define_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
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
        self.bottomLayout.addRow("", self.btn_delete)
        self.bottomLayout.addRow("", self.btn_update)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def article_details(self):
        query = "SELECT * FROM articles WHERE id = ?"
        article = cur.execute(query, (self.articleId, )).fetchone()
        self.txtArticleTitle.setText(article[1])
        self.txtUM.setText(article[2])
        self.txtStockMin.setText(str(article[3]))
        self.txtQtyStock.setText(str(article[4]))
        self.txtPU.setText(str(article[5]))

    def delete_article(self):
        articleId = self.articleId

        answer = QMessageBox.question(self, "Attention !!!", "Etes vous sûr de vouloir supprimer l'article ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            try:
                cur.execute("DELETE FROM articles WHERE id=?", (articleId,))
                conn.commit()
                QMessageBox.information(self, "Information", "Article supprimé avec succès.")
                self.close()
            except:
                QMessageBox.warning(self, "Avertissement", "Le article n'a pas été supprimé !!!")

    def update_article(self):
        id = self.articleId
        article_title = self.txtArticleTitle.text()
        unit_measure = self.txtUM.text()
        stock_min = self.txtStockMin.text()
        qty_stock = self.txtQtyStock.text()
        unit_price = self.txtPU.text()

        if article_title and unit_price != "":
            try:
                query = "UPDATE articles SET title=?, unit_measure=?, minimum_stock=?, stock_quantity=?, unit_price=? WHERE id =?"
                cur.execute(query, (article_title, unit_measure, stock_min, qty_stock, unit_price, id))
                conn.commit()
                QMessageBox.information(self, "Succès !!!", "Détails article modifiés avec succès.")
                self.close()
            except:
                QMessageBox.critical(self, "Attention !!!", "Les détails article n'ont pas été modifiés !")
        else:
            QMessageBox.warning(self, "Avertissement !!!", "Vérifiez les champs obligatoires !")
