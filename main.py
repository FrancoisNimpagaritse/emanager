import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from ui_modules import addclient, addsupplier, addarticle, updateclient, updatesupplier, updatearticle, searchArticleApprovs


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eManager ~ Gestion Commerciale")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.showMaximized()

        self.set_ui()
        self.show()

    def set_ui(self):
        self.toolbar()
        self.define_main_widgets()
        self.layouts_and_widgets()
        self.display_clients()
        self.display_suppliers()
        self.display_articles()
        #self.display_approvs()


    def toolbar(self):
        self.tlBar = self.addToolBar("Tool Bar")
        self.tlBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # Toolbar buttons
        self.manageCustomers = QAction(QIcon("icons/members.png"), "Gestion Clients", self)
        self.manageCustomers.triggered.connect(self.clients_stack)
        self.tlBar.addAction(self.manageCustomers)
        self.tlBar.addSeparator()
        self.manageSuppliers = QAction(QIcon("icons/suppliers.png"), "Gestion Fournisseurs")
        self.manageSuppliers.triggered.connect(self.suppliers_stack)
        self.tlBar.addAction(self.manageSuppliers)
        self.tlBar.addSeparator()
        self.manageArticles = QAction(QIcon("icons/articles.png"), "Gestion Articles", self)
        self.manageArticles.triggered.connect(self.articles_stack)
        self.tlBar.addAction(self.manageArticles)
        self.tlBar.addSeparator()
        self.manageApprovs = QAction(QIcon("icons/stock.png"), "Gestion Achats")
        self.manageApprovs.triggered.connect(self.approvs_stack)
        self.tlBar.addAction(self.manageApprovs)
        self.tlBar.addSeparator()
        self.manageStock = QAction(QIcon("icons/inventory.png"), "Gestion Stock")
        self.manageStock.triggered.connect(self.stock_stack)
        self.tlBar.addAction(self.manageStock)
        self.tlBar.addSeparator()
        self.manageRestoPub = QAction(QIcon("icons/restaurant.png"), "Bar Restaurant")
        self.manageRestoPub.triggered.connect(self.resto_pub_stack)
        self.tlBar.addAction(self.manageRestoPub)
        self.tlBar.addSeparator()

    def define_main_widgets(self):
        # Main Layout #
        self.mainWgt = QStackedWidget()

        self.clientsStack = QWidget()
        self.suppliersStack = QWidget()
        self.articlesStack = QWidget()
        self.approvsStack = QWidget()
        self.stockStack = QWidget()
        self.restoPubStack = QWidget()

        self.mainWgt.addWidget(self.clientsStack)
        self.mainWgt.addWidget(self.suppliersStack)
        self.mainWgt.addWidget(self.articlesStack)
        self.mainWgt.addWidget(self.approvsStack)
        self.mainWgt.addWidget(self.stockStack)
        self.mainWgt.addWidget(self.restoPubStack)

        self.setCentralWidget(self.mainWgt)

    def layouts_and_widgets(self):
        # Client Stack layout and widgets #
        self.clientMainLayout = QHBoxLayout()
        self.clientLeftMainLayout = QHBoxLayout()
        self.clientRightMainLayout = QVBoxLayout()
        self.clientRightUpperLayout = QHBoxLayout()
        self.clientRightTopLayout = QHBoxLayout()
        self.clientRightMiddleLayout = QHBoxLayout()
        self.clientUpperGrpBx = QGroupBox("Mise à jour clients")
        self.clientTopGrpBx = QGroupBox("Recherche client")
        self.clientMiddleGrpBx = QGroupBox("Filtre clients")
        self.clientMiddleGrpBx.setContentsMargins(10, 50, 10, 800)

        # Main left layout widgets#
        self.tblClients = QTableWidget()
        self.tblClients.setColumnCount(6)
        self.tblClients.setColumnHidden(0, True)
        self.tblClients.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tblClients.setHorizontalHeaderItem(1, QTableWidgetItem("Nom"))
        self.tblClients.setHorizontalHeaderItem(2, QTableWidgetItem("Prénom"))
        self.tblClients.setHorizontalHeaderItem(3, QTableWidgetItem("Email"))
        self.tblClients.setHorizontalHeaderItem(4, QTableWidgetItem("Téléphone"))
        self.tblClients.setHorizontalHeaderItem(5, QTableWidgetItem("Adresse"))
        self.tblClients.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblClients.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.tblClients.doubleClicked.connect(self.selected_client)

        # client Main right layout widgets#
        self.btn_AddClient = QPushButton("Ajouter")
        self.btn_AddClient.clicked.connect(self.add_new_client)
        self.btn_UpdateClient = QPushButton("Modifier")
        self.btn_DeleteClient = QPushButton("Supprimer")

        self.searchClientTxt = QLineEdit()
        self.searchClientTxt.setPlaceholderText("Chercher un client")
        self.btn_searchClient = QPushButton("Chercher")
        self.btn_searchClient.clicked.connect(self.search_clients)

        self.clientRightUpperLayout.addWidget(self.btn_AddClient)
        self.clientRightUpperLayout.addWidget(self.btn_UpdateClient)
        self.clientRightUpperLayout.addWidget(self.btn_DeleteClient)
        self.clientUpperGrpBx.setLayout(self.clientRightUpperLayout)

        self.clientRightMainLayout.addWidget(self.clientUpperGrpBx)

        self.clientRightTopLayout.addWidget(self.searchClientTxt)
        self.clientRightTopLayout.addWidget(self.btn_searchClient)
        self.clientTopGrpBx.setLayout(self.clientRightTopLayout)

        self.clientRightMainLayout.addWidget(self.clientTopGrpBx)

        self.allClients = QRadioButton("Tous")
        self.activeClients = QRadioButton("Actifs")
        self.inactiveClients = QRadioButton("Inactifs")
        self.btn_liste = QPushButton("Lister")

        self.clientRightMiddleLayout.addWidget(self.allClients)
        self.clientRightMiddleLayout.addWidget(self.activeClients)
        self.clientRightMiddleLayout.addWidget(self.inactiveClients)
        self.clientRightMiddleLayout.addWidget(self.btn_liste)
        self.clientMiddleGrpBx.setLayout(self.clientRightMiddleLayout)

        self.clientRightMainLayout.addWidget(self.clientMiddleGrpBx)
        self.clientLeftMainLayout.addWidget(self.tblClients)

        self.clientMainLayout.addLayout(self.clientLeftMainLayout, 70)
        self.clientMainLayout.addLayout(self.clientRightMainLayout, 30)

        self.clientsStack.setLayout(self.clientMainLayout)

        ################## Supplier Stack layout and widgets #####################
        self.supplierMainLayout = QHBoxLayout()
        self.supplierLeftMainLayout = QHBoxLayout()
        self.supplierRightMainLayout = QVBoxLayout()
        self.supplierRightUpperLayout = QHBoxLayout()
        self.supplierRightTopLayout = QHBoxLayout()
        self.supplierRightMiddleLayout = QHBoxLayout()
        self.supplierUpperGrpBx = QGroupBox("Mise à jour fournisseurs")
        self.supplierTopGrpBx = QGroupBox("Recherche fournisseur")
        self.supplierMiddleGrpBx = QGroupBox("Filtre fournisseurs")
        self.supplierMiddleGrpBx.setContentsMargins(10, 50, 10, 800)

        self.tblSuppliers = QTableWidget()
        self.tblSuppliers.setColumnCount(6)
        self.tblSuppliers.setColumnHidden(0, True)
        self.tblSuppliers.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tblSuppliers.setHorizontalHeaderItem(1, QTableWidgetItem("Nom Fournisseur"))
        self.tblSuppliers.setHorizontalHeaderItem(2, QTableWidgetItem("Prénom"))
        self.tblSuppliers.setHorizontalHeaderItem(3, QTableWidgetItem("Email"))
        self.tblSuppliers.setHorizontalHeaderItem(4, QTableWidgetItem("Téléphone"))
        self.tblSuppliers.setHorizontalHeaderItem(5, QTableWidgetItem("Adresse"))
        self.tblSuppliers.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblSuppliers.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tblSuppliers.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.tblSuppliers.doubleClicked.connect(self.selected_supplier)

        # supplier Main right layout widgets#
        self.btn_AddSupplier = QPushButton("Ajouter")
        self.btn_AddSupplier.clicked.connect(self.add_new_supplier)
        self.btn_UpdateSupplier = QPushButton("Modifier")
        self.btn_DeleteSupplier = QPushButton("Supprimer")

        self.searchSupplierTxt = QLineEdit()
        self.searchSupplierTxt.setPlaceholderText("Chercher un fournisseur")
        self.btn_searchSupplier = QPushButton("Chercher")
        self.btn_searchSupplier.clicked.connect(self.search_suppliers)

        self.supplierRightUpperLayout.addWidget(self.btn_AddSupplier)
        self.supplierRightUpperLayout.addWidget(self.btn_UpdateSupplier)
        self.supplierRightUpperLayout.addWidget(self.btn_DeleteSupplier)
        self.supplierUpperGrpBx.setLayout(self.supplierRightUpperLayout)

        self.supplierRightMainLayout.addWidget(self.supplierUpperGrpBx)

        self.supplierRightTopLayout.addWidget(self.searchSupplierTxt)
        self.supplierRightTopLayout.addWidget(self.btn_searchSupplier)
        self.supplierTopGrpBx.setLayout(self.supplierRightTopLayout)

        self.supplierRightMainLayout.addWidget(self.supplierTopGrpBx)

        self.allSupplier = QRadioButton("Tous")
        self.activeSupplier = QRadioButton("Actifs")
        self.inactiveSupplier = QRadioButton("Inactifs")
        self.btn_liste = QPushButton("Lister")

        self.supplierRightMiddleLayout.addWidget(self.allSupplier)
        self.supplierRightMiddleLayout.addWidget(self.activeSupplier)
        self.supplierRightMiddleLayout.addWidget(self.inactiveSupplier)
        self.supplierRightMiddleLayout.addWidget(self.btn_liste)
        self.supplierMiddleGrpBx.setLayout(self.clientRightMiddleLayout)

        self.supplierRightMainLayout.addWidget(self.supplierMiddleGrpBx)
        self.supplierLeftMainLayout.addWidget(self.tblSuppliers)

        self.supplierMainLayout.addLayout(self.supplierLeftMainLayout, 70)
        self.supplierMainLayout.addLayout(self.supplierRightMainLayout, 30)

        self.suppliersStack.setLayout(self.supplierMainLayout)

        ########## Article Stack layout and widgets ##############
        self.articleMainLayout = QHBoxLayout()
        self.articleLeftMainLayout = QHBoxLayout()
        self.articleRightMainLayout = QVBoxLayout()
        self.articleRightUpperLayout = QHBoxLayout()
        self.articleRightTopLayout = QHBoxLayout()
        self.articleRightMiddleLayout = QHBoxLayout()
        self.articleUpperGrpBx = QGroupBox("Mise à jour article")
        self.articleTopGrpBx = QGroupBox("Recherche un article")
        self.articleMiddleGrpBx = QGroupBox("Filtre articles")
        self.articleMiddleGrpBx.setContentsMargins(10, 50, 10, 800)

        # articles Main left layout widgets#
        self.tblArticles = QTableWidget()
        self.tblArticles.setColumnCount(6)
        self.tblArticles.setColumnHidden(0, True)
        self.tblArticles.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tblArticles.setHorizontalHeaderItem(1, QTableWidgetItem("Désignation"))
        self.tblArticles.setHorizontalHeaderItem(2, QTableWidgetItem("Unité Mesure"))
        self.tblArticles.setHorizontalHeaderItem(3, QTableWidgetItem("Seuil Stock"))
        self.tblArticles.setHorizontalHeaderItem(4, QTableWidgetItem("Qté en stock"))
        self.tblArticles.setHorizontalHeaderItem(5, QTableWidgetItem("Prix Unitaire"))

        self.tblArticles.doubleClicked.connect(self.selected_article)

        # articles Main right layout widgets#
        self.btn_AddArticle = QPushButton("Ajouter")
        self.btn_AddArticle.clicked.connect(self.add_new_article)
        self.btn_UpdateArticle = QPushButton("Modifier")
        self.btn_DeleteArticle = QPushButton("Supprimer")

        self.searchArticleTxt = QLineEdit()
        self.searchArticleTxt.setPlaceholderText("Chercher un article")
        self.btn_searchArticle = QPushButton("Chercher")
        self.btn_searchArticle.clicked.connect(self.search_articles)

        self.articleRightUpperLayout.addWidget(self.btn_AddArticle)
        self.articleRightUpperLayout.addWidget(self.btn_UpdateArticle)
        self.articleRightUpperLayout.addWidget(self.btn_DeleteArticle)
        self.articleUpperGrpBx.setLayout(self.articleRightUpperLayout)

        self.articleRightMainLayout.addWidget(self.articleUpperGrpBx)

        self.articleRightTopLayout.addWidget(self.searchArticleTxt)
        self.articleRightTopLayout.addWidget(self.btn_searchArticle)
        self.articleTopGrpBx.setLayout(self.articleRightTopLayout)
        self.articleRightMainLayout.addWidget(self.articleTopGrpBx)

        self.allArticle = QRadioButton("Tous")
        self.activeArticle = QRadioButton("Actifs")
        self.inactiveArticle = QRadioButton("Inactifs")
        self.btn_liste = QPushButton("Lister")

        self.articleRightMiddleLayout.addWidget(self.allArticle)
        self.articleRightMiddleLayout.addWidget(self.activeArticle)
        self.articleRightMiddleLayout.addWidget(self.inactiveArticle)
        self.articleRightMiddleLayout.addWidget(self.btn_liste)
        self.articleMiddleGrpBx.setLayout(self.clientRightMiddleLayout)

        self.articleRightMainLayout.addWidget(self.articleMiddleGrpBx)
        self.articleLeftMainLayout.addWidget(self.tblArticles)

        self.articleMainLayout.addLayout(self.articleLeftMainLayout, 70)
        self.articleMainLayout.addLayout(self.articleRightMainLayout, 30)

        self.articlesStack.setLayout(self.articleMainLayout)

        ########## Approvs Stack layout and widgets ##############
        self.approvsMainLayout = QVBoxLayout()

        self.approvsTopMainLayout = QHBoxLayout()
        self.approvsMiddleUpMainLayout = QHBoxLayout()
        self.approvsMiddleMidMainLayout = QHBoxLayout()
        self.approvsMiddleDownMainLayout = QHBoxLayout()
        self.approvsBottomMainLayout = QHBoxLayout()

        self.approvsInfosAchatGrpBx = QGroupBox("Informations facture")
        self.frmApprovsInfosAchat = QFormLayout()
        self.approvsInfosClientGrpBx = QGroupBox("Informations client")
        self.frmApprovsInfosClient = QFormLayout()
        self.approvsInfoPaymentGrpBx = QGroupBox()
        self.frmApprovsInfosPayment = QFormLayout()
        self.approvsOtherInfosClientGrpBx = QGroupBox()
        self.frmApprovsOtherInfosClient = QFormLayout()

        # placer bien les groupbox dans les Qformlayouts
        # approvs Top Main layout widgets#
        self.frmApprovsInfosAchat.addRow("Numéro :", QLineEdit())
        self.frmApprovsInfosAchat.addRow("Date: ", QDateEdit())
        self.frmApprovsInfosClient.addRow("Client :", QLineEdit())
        # approvs MiddleUp Main layout widgets#
        self.frmApprovsInfosPayment.addRow("Mode paiement :", QLineEdit())
        self.frmApprovsInfosPayment.addRow("Date échéance :", QDateEdit())
        self.frmApprovsOtherInfosClient.addRow("Référence :", QLineEdit())
        # approvs MiddleMid Main layout widgets#
        self.btn_AddApprovsArticle = QPushButton("Ajouter")
        self.btn_AddApprovsArticle.clicked.connect(self.search_article_new_approvs)
        self.btn_RemoveApprovsArticle = QPushButton("Retirer")
        self.btn_Test1ApprovsArticle = QPushButton("Tester 1")
        self.btn_Test2ApprovsArticle = QPushButton("Tester 2")
        # approvs MiddleDown Main layout widgets#
        self.tblApprovsDetails = QTableWidget()
        # approvs Bottom Main layout widgets#
        self.approvsLeftTotauxLayout = QFormLayout()
        self.approvsRightTotauxLayout = QFormLayout()
        self.approvsRightTotauxLayout.addRow("Total HTVA:", QLineEdit())
        self.approvsRightTotauxLayout.addRow("Total TVA :", QLineEdit())
        self.approvsRightTotauxLayout.addRow("Total TVAC :", QLineEdit())
        # add widgets to groupbox  #

        self.approvsInfosAchatGrpBx.setLayout(self.frmApprovsInfosAchat)
        self.approvsTopMainLayout.addWidget(self.approvsInfosAchatGrpBx)

        self.approvsInfosClientGrpBx.setLayout(self.frmApprovsInfosClient)
        self.approvsTopMainLayout.addWidget(self.approvsInfosClientGrpBx)

        self.approvsInfoPaymentGrpBx.setLayout(self.frmApprovsInfosPayment)
        self.approvsMiddleUpMainLayout.addWidget(self.approvsInfoPaymentGrpBx)

        self.approvsOtherInfosClientGrpBx.setLayout(self.frmApprovsOtherInfosClient)
        self.approvsMiddleUpMainLayout.addWidget(self.approvsOtherInfosClientGrpBx)

        self.approvsMiddleMidMainLayout.addWidget(self.btn_AddApprovsArticle)
        self.approvsMiddleMidMainLayout.addWidget(self.btn_RemoveApprovsArticle)
        self.approvsMiddleMidMainLayout.addWidget(self.btn_Test1ApprovsArticle)
        self.approvsMiddleMidMainLayout.addWidget(self.btn_Test2ApprovsArticle)

        self.approvsMiddleDownMainLayout.addWidget(self.tblApprovsDetails)

        self.approvsBottomMainLayout.addLayout(self.approvsLeftTotauxLayout, 75)
        self.approvsBottomMainLayout.addLayout(self.approvsRightTotauxLayout, 25)

        self.approvsMainLayout.addLayout(self.approvsTopMainLayout)
        self.approvsMainLayout.addLayout(self.approvsMiddleUpMainLayout)
        self.approvsMainLayout.addLayout(self.approvsMiddleMidMainLayout)
        self.approvsMainLayout.addLayout(self.approvsMiddleDownMainLayout)
        self.approvsMainLayout.addLayout(self.approvsBottomMainLayout)

        self.approvsStack.setLayout(self.approvsMainLayout)

        ########## Functions ##############
    def clients_stack(self):
        self.mainWgt.setCurrentIndex(0)

    def suppliers_stack(self):
        self.mainWgt.setCurrentIndex(1)

    def articles_stack(self):
        self.mainWgt.setCurrentIndex(2)

    def approvs_stack(self):
        self.mainWgt.setCurrentIndex(3)

    def stock_stack(self):
        self.mainWgt.setCurrentIndex(4)

    def resto_pub_stack(self):
        self.mainWgt.setCurrentIndex(5)

    def add_new_client(self):
        self.newClient = addclient.AddClient()

    def add_new_supplier(self):
        self.newSupplier = addsupplier.AddSupplier()

    def add_new_article(self):
        self.newArticle = addarticle.AddArticle()

    def search_article_new_approvs(self):
        self.searchArticleApprov = searchArticleApprovs.SearchArticleApprovs()

    def display_clients(self):
        self.tblClients.setFont(QFont("Comic sans serif", 10))
        for i in reversed(range(self.tblClients.rowCount())):
            self.tblClients.removeRow(i)

        query = cur.execute("SELECT id, lastname, firstname, email, phone, address FROM clients")
        for row_data in query:
            row_number = self.tblClients.rowCount()
            self.tblClients.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tblClients.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.tblClients.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selected_client(self):
        global clientId
        listClientFieldsValues = []
        for i in range(0, 6):
            listClientFieldsValues.append(self.tblClients.item(self.tblClients.currentRow(), i).text())
        clientId = listClientFieldsValues[0]
        #Start and pass client id to the update form
        self.updateClient = updateclient.UpdateClient(clientId)
        #self.updateClient.txtEmail.setText(clientId)
        #self.updateClient.show()

    def display_suppliers(self):
        self.tblSuppliers.setFont(QFont("Comic sans serif", 10))
        for i in reversed(range(self.tblSuppliers.rowCount())):
            self.tblSuppliers.removeRow(i)

        query = cur.execute("SELECT id, lastname, firstname, email, phone, address FROM suppliers")
        for row_data in query:
            row_number = self.tblSuppliers.rowCount()
            self.tblSuppliers.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tblSuppliers.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.tblSuppliers.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selected_supplier(self):
        global supplierId
        listSuppliersFieldsValues = []
        for i in range(0, 6):
            listSuppliersFieldsValues.append(self.tblSuppliers.item(self.tblSuppliers.currentRow(), i).text())
        supplierId = listSuppliersFieldsValues[0]
        #Start and pass client id to the update form
        self.updateSupplier = updatesupplier.UpdateSupplier(supplierId)

    def display_articles(self):
        self.tblArticles.setFont(QFont("Comic sans serif", 10))
        for i in reversed(range(self.tblArticles.rowCount())):
            self.tblArticles.removeRow(i)

        query = cur.execute("SELECT id, title, unit_measure, minimum_stock, stock_quantity, unit_price FROM articles")
        for row_data in query:
            row_number = self.tblArticles.rowCount()
            self.tblArticles.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tblArticles.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.tblArticles.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selected_article(self):
        global articleId
        listArticlesFieldsValues = []
        for i in range(0, 6):
            listArticlesFieldsValues.append(self.tblArticles.item(self.tblArticles.currentRow(), i).text())
        articleId = listArticlesFieldsValues[0]
        #Start and pass client id to the update form
        self.updateArticle = updatearticle.UpdateArticle(articleId)

    def search_clients(self):
        value = self.searchClientTxt.text()
        if value == "":
            QMessageBox.information(self, "Avertissement", "Veuillez renseigner une valeur de recherche !")
        else:
            self.searchClientTxt.setText("")
            query = "SELECT id, firstname, lastname, email, phone FROM clients WHERE firstname LIKE ? OR lastname LIKE ? OR email LIKE ? OR phone LIKE ?"
            results = cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()

            if results == []:
                    QMessageBox.information(self, "Avertissement !!", "Le client recherché n'existe pas !!!")
            else:
                for i in reversed(range(self.tblClients.rowCount())):
                    self.tblClients.removeRow(i)
                for row_data in results:
                    row_number = self.tblClients.rowCount()
                    self.tblClients.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tblClients.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search_suppliers(self):
        value = self.searchSupplierTxt.text()
        if value == "":
            QMessageBox.information(self, "Avertissement", "Veuillez renseigner une valeur de recherche !")
        else:
            self.searchSupplierTxt.setText("")
            query = "SELECT id, firstname, lastname, email, phone FROM suppliers WHERE firstname LIKE ? OR lastname LIKE ? OR email LIKE ? OR phone LIKE ?"
            results = cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()

            if results == []:
                QMessageBox.information(self, "Avertissement !!", "Le fournisseur recherché n'existe pas !!!")
            else:
                for i in reversed(range(self.tblSuppliers.rowCount())):
                    self.tblSuppliers.removeRow(i)
                for row_data in results:
                    row_number = self.tblSuppliers.rowCount()
                    self.tblSuppliers.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tblSuppliers.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search_articles(self):
        value = self.searchArticleTxt.text()
        if value == "":
            QMessageBox.information(self, "Avertissement", "Veuillez renseigner une valeur de recherche !")
        else:
            self.searchArticleTxt.setText("")
            query = "SELECT id, title, unit_measure, minimum_stock, stock_quantity, unit_price FROM articles WHERE id LIKE ? OR title LIKE ?"
            results = cur.execute(query, ('%' + value + '%', '%' + value + '%')).fetchall()

            if results == []:
                QMessageBox.information(self, "Avertissement !!", "L'article recherché n'existe pas !!!")
            else:
                for i in reversed(range(self.tblArticles.rowCount())):
                    self.tblArticles.removeRow(i)
                for row_data in results:
                    row_number = self.tblArticles.rowCount()
                    self.tblArticles.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tblArticles.setItem(row_number, column_number, QTableWidgetItem(str(data)))


def main():
    app = QApplication(sys.argv)
    win = MainWindow()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
