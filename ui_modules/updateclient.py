import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class UpdateClient(QWidget):
    def __init__(self, clientId):
        super().__init__()
        self.setWindowTitle("Détails données client")
        self.setWindowIcon((QIcon("icons/icon.ico")))
        self.setGeometry(600, 500, 650, 750)
        self.setFixedSize(self.size())
        self.clientId = clientId
        self.set_ui()
        self.show()

    def set_ui(self):
        self.define_widgets()
        self.define_layouts()
        self.client_details()

    def define_widgets(self):
        ############ widgets of top layout ###########
        self.addClientImg = QLabel()
        self.img = QPixmap("icons/addmember.png")
        self.addClientImg.setPixmap(self.img)
        self.titleTxt = QLabel("Modifier un client")
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
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.delete_client)
        self.btn_update = QPushButton("Modifier")
        self.btn_update.clicked.connect(self.update_client)

    def define_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        ############## Add widgets #################
        ########### Widgets of top layout #########
        self.topLayout.addWidget(self.addClientImg)
        self.topLayout.addWidget(self.titleTxt)
        self.topFrame.setLayout(self.topLayout)
        ########### Widgets of bottom layout #########
        self.bottomLayout.addRow(QLabel("Prénom:"), self.txtFirstname)
        self.bottomLayout.addRow(QLabel("Nom:"), self.txtLastname)
        self.bottomLayout.addRow(QLabel("Email:"), self.txtEmail)
        self.bottomLayout.addRow(QLabel("Téléphone:"), self.txtPhone)
        self.bottomLayout.addRow(QLabel("Adresse:"), self.txtAddress)
        self.bottomLayout.addRow("", self.btn_delete)
        self.bottomLayout.addRow("", self.btn_update)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def client_details(self):
        query = "SELECT * FROM clients WHERE id = ?"
        client = cur.execute(query, (self.clientId, )).fetchone()
        self.txtFirstname.setText(client[1])
        self.txtLastname.setText(client[2])
        self.txtEmail.setText(client[3])
        self.txtPhone.setText(client[4])
        self.txtAddress.setText(client[5])

    def delete_client(self):
        clientId = self.clientId

        answer = QMessageBox.question(self, "Attention !!!", "Etes vous sûr de vouloir supprimer le client ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            try:
                cur.execute("DELETE FROM clients WHERE id=?", (clientId,))
                conn.commit()
                QMessageBox.information(self, "Information", "Client supprimé avec succès.")
                self.close()
            except:
                QMessageBox.warning(self, "Avertissement", "Le client n'a pas été supprimé !!!")

    def update_client(self):
        id = self.clientId
        firstname = self.txtFirstname.text()
        lastname = self.txtLastname.text()
        email = self.txtEmail.text()
        phone = self.txtPhone.text()
        address = self.txtAddress.text()

        if lastname and phone and address != "":
            try:
                query = "UPDATE clients SET firstname=?, lastname=?, email=?, phone=?, address=? WHERE id =?"
                cur.execute(query, (firstname, lastname, email, phone, address, id))
                conn.commit()
                QMessageBox.information(self, "Succès !!!", "Détails client modifiés avec succès.")
                self.close()
            except:
                QMessageBox.critical(self, "Attention !!!", "Les détails client n'ont pas été modifiés !")
        else:
            QMessageBox.warning(self, "Avertissement !!!", "Vérifiez les champs obligatoires !")
