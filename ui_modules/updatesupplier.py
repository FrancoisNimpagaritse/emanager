import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3


conn = sqlite3.connect("data/emanager.db")
cur = conn.cursor()


class UpdateSupplier(QWidget):
    def __init__(self, supplierId):
        super().__init__()
        self.setWindowTitle("Détails données fournisseur")
        self.setWindowIcon((QIcon("icons/icon.ico")))
        self.setGeometry(600, 500, 650, 750)
        self.setFixedSize(self.size())
        self.supplierId = supplierId
        self.set_ui()
        self.show()

    def set_ui(self):
        self.define_widgets()
        self.define_layouts()
        self.supplier_details()

    def define_widgets(self):
        ############ widgets of top layout ###########
        self.addSupplierImg = QLabel()
        self.img = QPixmap("icons/addmember.png")
        self.addSupplierImg.setPixmap(self.img)
        self.titleTxt = QLabel("Modifier fournisseur")
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
        self.btn_delete.clicked.connect(self.delete_supplier)
        self.btn_update = QPushButton("Modifier")
        self.btn_update.clicked.connect(self.update_supplier)

    def define_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
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
        self.bottomLayout.addRow("", self.btn_delete)
        self.bottomLayout.addRow("", self.btn_update)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def supplier_details(self):
        query = "SELECT * FROM suppliers WHERE id = ?"
        supplier = cur.execute(query, (self.supplierId, )).fetchone()
        self.txtFirstname.setText(supplier[1])
        self.txtLastname.setText(supplier[2])
        self.txtEmail.setText(supplier[3])
        self.txtPhone.setText(supplier[4])
        self.txtAddress.setText(supplier[5])

    def delete_supplier(self):
        supplierId = self.supplierId

        answer = QMessageBox.question(self, "Attention !!!", "Etes vous sûr de vouloir supprimer le fournisseur ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            try:
                cur.execute("DELETE FROM clients WHERE id=?", (supplierId,))
                conn.commit()
                QMessageBox.information(self, "Information", "Fournisseur supprimé avec succès.")
                self.close()
            except:
                QMessageBox.warning(self, "Avertissement", "Le fournisseur n'a pas été supprimé !!!")

    def update_supplier(self):
        id = self.supplierId
        firstname = self.txtFirstname.text()
        lastname = self.txtLastname.text()
        email = self.txtEmail.text()
        phone = self.txtPhone.text()
        address = self.txtAddress.text()

        if lastname and phone and address != "":
            try:
                query = "UPDATE suppliers SET firstname=?, lastname=?, email=?, phone=?, address=? WHERE id =?"
                cur.execute(query, (firstname, lastname, email, phone, address, id))
                conn.commit()
                QMessageBox.information(self, "Succès !!!", "Détails fournisseur modifiés avec succès.")
                self.close()
            except:
                QMessageBox.critical(self, "Attention !!!", "Les détails fournisseur n'ont pas été modifiés !")
        else:
            QMessageBox.warning(self, "Avertissement !!!", "Vérifiez les champs obligatoires !")
