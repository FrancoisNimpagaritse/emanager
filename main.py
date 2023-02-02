import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from ui_modules import addclient, addsupplier, updateclient, updatesupplier


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eManager ~ Gestion Commerciale")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(250, 100, 2000, 1400)
        self.setFixedSize(self.size())

        self.set_ui()
        self.show()

    def set_ui(self):
        self.toolbar()
        self.define_main_widgets()
        self.layouts_and_widgets()
        self.display_clients()
        self.display_suppliers()


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
        self.tblClients.doubleClicked.connect(self.selected_product)

        # client Main right layout widgets#
        self.btn_AddClient = QPushButton("Ajouter")
        self.btn_AddClient.clicked.connect(self.add_new_client)
        self.btn_UpdateClient = QPushButton("Modifier")
        self.btn_DeleteClient = QPushButton("Supprimer")

        self.searchTxt = QLineEdit()
        self.searchTxt.setPlaceholderText("Chercher un client")
        self.btn_search = QPushButton("Chercher")

        self.clientRightUpperLayout.addWidget(self.btn_AddClient)
        self.clientRightUpperLayout.addWidget(self.btn_UpdateClient)
        self.clientRightUpperLayout.addWidget(self.btn_DeleteClient)
        self.clientUpperGrpBx.setLayout(self.clientRightUpperLayout)

        self.clientRightMainLayout.addWidget(self.clientUpperGrpBx)

        self.clientRightTopLayout.addWidget(self.searchTxt)
        self.clientRightTopLayout.addWidget(self.btn_search)
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

        # Supplier Stack layout and widgets #
        self.supplierMainLayout = QHBoxLayout()
        self.supplierLeftMainLayout = QHBoxLayout()
        self.supplierRightMainLayout = QVBoxLayout()
        self.supplierRightUpperLayout = QHBoxLayout()
        self.supplierRightTopLayout = QHBoxLayout()
        self.supplierRightMiddleLayout = QHBoxLayout()
        self.supplierUpperGrpBx = QGroupBox("Mise à jour fournisseurs")
        self.supplierTopGrpBx = QGroupBox("Recherche fournisseur")
        self.supplierMiddleGrpBx = QGroupBox("Filtre client")
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

        # supplier Main right layout widgets#
        self.btn_AddSupplier = QPushButton("Ajouter")
        self.btn_AddSupplier.clicked.connect(self.add_new_supplier)
        self.btn_UpdateSupplier = QPushButton("Modifier")
        self.btn_DeleteSupplier = QPushButton("Supprimer")

        self.searchTxt = QLineEdit()
        self.searchTxt.setPlaceholderText("Chercher un client")
        self.btn_search = QPushButton("Chercher")

        self.supplierRightUpperLayout.addWidget(self.btn_AddSupplier)
        self.supplierRightUpperLayout.addWidget(self.btn_UpdateSupplier)
        self.supplierRightUpperLayout.addWidget(self.btn_DeleteSupplier)
        self.supplierUpperGrpBx.setLayout(self.supplierRightUpperLayout)

        self.supplierRightMainLayout.addWidget(self.supplierUpperGrpBx)

        self.supplierRightTopLayout.addWidget(self.searchTxt)
        self.supplierRightTopLayout.addWidget(self.btn_search)
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

        # Article Stack layout and widgets #
        self.articleMainLayout = QHBoxLayout()
        self.articleLeftMainLayout = QHBoxLayout()
        self.articleRightMainLayout = QVBoxLayout()
        self.articleRightTopLayout = QHBoxLayout()
        self.articleRightMiddleLayout = QHBoxLayout()
        self.articleTopGrpBx = QGroupBox()
        self.articleMiddleGrpBx = QGroupBox()

        self.tblArticles = QTableWidget()
        self.tblArticles.setColumnCount(6)
        self.tblArticles.setColumnHidden(0, True)
        self.tblArticles.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tblArticles.setHorizontalHeaderItem(1, QTableWidgetItem("Désignation"))
        self.tblArticles.setHorizontalHeaderItem(2, QTableWidgetItem("Unité Mesure"))
        self.tblArticles.setHorizontalHeaderItem(3, QTableWidgetItem("Seuil Stock"))
        self.tblArticles.setHorizontalHeaderItem(4, QTableWidgetItem("Qté en stock"))
        self.tblArticles.setHorizontalHeaderItem(5, QTableWidgetItem("Prix Unitaire"))

        self.articleLeftMainLayout.addWidget(self.tblArticles)
        self.articleMainLayout.addLayout(self.articleLeftMainLayout)
        self.articlesStack.setLayout(self.articleMainLayout)

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

    def selected_product(self):
        global clientId
        listClientFieldsValues = []
        for i in range(0, 6):
            listClientFieldsValues.append(self.tblClients.item(self.tblClients.currentRow(), i).text())
        clientId = listClientFieldsValues[0]
        #Start and pass client id to the update form
        self.updateClient = updateclient.UpdateProduct(clientId)
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


def main():
    app = QApplication(sys.argv)
    win = MainWindow()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
