import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class AddSupplier(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter un nouveau fournisseur")
        self.setWindowIcon((QIcon("icons/icon.ico")))
        self.setGeometry(600, 500, 650, 750)
        self.setFixedSize(self.size())
        self.set_ui()
        self.show()

    def set_ui(self):
        self.define_widgets()
        print("here")
        self.define_layouts()

    def define_widgets(self):
        ############ widgets of top layout ###########
        self.addSupplierImg = QLabel()
        self.img = QPixmap("icons/addmember.png")
        self.addSupplierImg.setPixmap(self.img)
        self.titleTxt = QLabel("Ajout fournisseur")
        self.titleTxt.setStyleSheet("font-weight: bold; font-size: 16pt;")
        ############# widgets of bottom layout ########
        self.txtFirstname = QLineEdit()
        self.txtFirstname.setPlaceholderText("Entrer le prénom")
        self.txtLastname = QLineEdit()
        self.txtFirstname.setPlaceholderText("Entrer le nom")
        self.txtEmail = QLineEdit()
        self.txtFirstname.setPlaceholderText("Entrer l'email")
        self.txtPhone = QLineEdit()
        self.txtFirstname.setPlaceholderText("Entrer le téléphone")
        self.txtAddress = QLineEdit()
        self.txtFirstname.setPlaceholderText("Entrer l'adresse")
        self.btn_submit = QPushButton("Valider")
        self.btn_submit.clicked.connect(self.insert_supplier)

    def define_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame =QFrame()
        self.bottomFrame =QFrame()
        ############## Add widgets #################
        ########### Widgets of top layout #########
        self.topLayout.addWidget(self.addSupplierImg)
        self.topLayout.addWidget(self.titleTxt)
        self.topFrame.setLayout(self.topLayout)
        ########### Widgets of bottom layout #########
        self.bottomLayout.addRow(QLabel("Prénom:"), self.txtFirstname)
        self.bottomLayout.addRow(QLabel("Nom:"), self.txtLastname)
        self.bottomLayout.addRow(QLabel("Email:"), self.txtEmail)
        self.bottomLayout.addRow(QLabel("Téléphone:"), self.txtPhone)
        self.bottomLayout.addRow(QLabel("Adresse:"), self.txtAddress)
        self.bottomLayout.addRow("", self.btn_submit)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def insert_supplier(self):
            firstname = self.txtFirstname.text()
            lastname = self.txtLastname.text()
            email = self.txtEmail.text()
            phone = self.txtPhone.text()
            address = self.txtAddress.text()

            if lastname and phone and address != "":
                try:
                    query = "INSERT INTO suppliers(firstname, lastname, email, phone, address) VALUES(?,?,?,?,?)"
                    cur.execute(query, (firstname, lastname, email, phone, address))
                    conn.commit()
                    QMessageBox.information(self, "Succès !!!", "Fournisseur ajouté avec succès.")
                    self.close()
                except:
                    QMessageBox.critical(self, "Attention !!!", "Le fournisseur n'a pas été ajouté !")
            else:
                QMessageBox.warning(self, "Avertissement !!!", "Vérifiez les champs obligatoires !")
