from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_AddDialog(QtWidgets.QDialog):
    # Определение сигнала
    data_added = QtCore.pyqtSignal()

    def __init__(self, operation_type):
        super().__init__()

        self.operation_type = operation_type

        self.setWindowTitle("")
        self.resize(400, 200)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_name = QtWidgets.QLabel("")
        self.verticalLayout.addWidget(self.label_name)

        self.lineEdit_name = QtWidgets.QLineEdit(self)
        self.verticalLayout.addWidget(self.lineEdit_name)

        self.label_surname = QtWidgets.QLabel("")
        self.verticalLayout.addWidget(self.label_surname)

        self.lineEdit_surname = QtWidgets.QLineEdit(self)
        self.verticalLayout.addWidget(self.lineEdit_surname)

        self.label_patronymic = QtWidgets.QLabel("")
        self.verticalLayout.addWidget(self.label_patronymic)

        self.lineEdit_patronymic = QtWidgets.QLineEdit(self)
        self.verticalLayout.addWidget(self.lineEdit_patronymic)

        self.label_phone = QtWidgets.QLabel("")
        self.verticalLayout.addWidget(self.label_phone)

        self.lineEdit_phone = QtWidgets.QLineEdit(self)
        self.verticalLayout.addWidget(self.lineEdit_phone)

        self.label_note = QtWidgets.QLabel("")
        self.verticalLayout.addWidget(self.label_note)

        self.lineEdit_note = QtWidgets.QLineEdit(self)
        self.verticalLayout.addWidget(self.lineEdit_note)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()

        # Блокировка кнопки "Ок" при создании диалога
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        # Подключение слотов для проверки заполнения важных данных
        self.lineEdit_name.textChanged.connect(self.check_data)
        self.lineEdit_surname.textChanged.connect(self.check_data)
        self.lineEdit_phone.textChanged.connect(self.check_data)

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        if self.operation_type == "Продать":
            self.setWindowTitle(_translate("operationDialog", "Добавить клиента"))
            self.label_name.setText(_translate("operationDialog", "Имя:"))
            self.label_surname.setText(_translate("operationDialog", "Фамилия:"))
            self.label_patronymic.setText(_translate("operationDialog", "Отчество:"))
            self.label_phone.setText(_translate("operationDialog", "Номер телефона:"))
            self.label_note.setText(_translate("operationDialog", "Примечание:"))
        elif self.operation_type == "Переместить":
            self.setWindowTitle(_translate("operationDialog", "Добавить склад"))
            self.label_name.setText(_translate("operationDialog", "Название склада:"))
            self.label_surname.setText(_translate("operationDialog", "Адрес:"))
            self.label_patronymic.setText(_translate("operationDialog", "Координаты:"))
            self.label_phone.setText(_translate("operationDialog", "Геолокация:"))
            self.label_note.setText(_translate("operationDialog", "Примечание:"))

    def check_data(self):
        # Проверка заполнения важных данных в зависимости от типа операции
        if self.operation_type == "Продать":
            name_valid = self.lineEdit_name.text().isalpha()
            surname_valid = self.lineEdit_surname.text().isalpha()
            patronymic_valid = self.lineEdit_patronymic.text().isalpha()
            phone_valid = self.lineEdit_phone.text().isdigit()

            if name_valid and surname_valid and patronymic_valid and phone_valid:
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        elif self.operation_type == "Переместить":
            name_valid = self.lineEdit_name.text() != ""
            address_valid = self.lineEdit_surname.text() != ""
            coordinates_valid = self.lineEdit_patronymic.text().isdigit()
            geolocation_valid = self.lineEdit_phone.text().isdigit()
            if name_valid and address_valid and coordinates_valid and geolocation_valid:
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def save_data(self):
        # Получаем данные в зависимости от типа операции
        if self.operation_type == "Продать":
            # Получаем данные о клиенте из полей ввода
            name = self.lineEdit_name.text()
            surname = self.lineEdit_surname.text()
            patronymic = self.lineEdit_patronymic.text()
            phone = self.lineEdit_phone.text()
            json_note = self.lineEdit_note.text()

            # Объединяем имя, фамилию и отчество в одну строку
            full_name = " ".join(filter(None, [surname, name, patronymic]))

            # Создаем подключение к базе данных
            conn = sqlite3.connect('warehouse.db')
            c = conn.cursor()

            # Вставляем данные о клиенте в таблицу Client
            c.execute("INSERT INTO Client (name, phone_number, json_note) VALUES (?, ?, ?)",
                      (full_name, phone, json_note))

            # Сохраняем изменения в базе данных
            conn.commit()
            conn.close()

            # Отправляем сигнал о добавлении данных
            self.data_added.emit()

            # Закрываем диалоговое окно
            self.accept()
        elif self.operation_type == "Переместить":
            # Получаем данные о складе из полей ввода
            name = self.lineEdit_name.text() != ""
            address = self.lineEdit_surname.text() != ""
            coordinates = self.lineEdit_patronymic.text().isdigit()
            geolocation = self.lineEdit_phone.text().isdigit()

            # Создаем подключение к базе данных
            conn = sqlite3.connect('warehouse.db')
            c = conn.cursor()

            # Вставляем данные о складе в таблицу Warehouse
            c.execute(
                "INSERT INTO Warehouse (name, address, coordinates, geolocation) VALUES (?, ?, ?, ?)",
                (name, address, coordinates, geolocation))

            conn.commit()
            conn.close()
            # Отправляем сигнал о добавлении данных
            self.data_added.emit()
            # Закрываем диалоговое окно
            self.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = AddDialog()
    dialog.exec_()
    sys.exit(app.exec_())
