from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class ChooseDialog(QtCore.QObject):
    # Определение сигнала
    data_selected = QtCore.pyqtSignal(list)

    def __init__(self, cursor, selected_items, operation_type):
        super().__init__()
        self.cursor = cursor
        self.selected_items = selected_items
        self.operation_type = operation_type

        self.ChooseDialog = QtWidgets.QDialog()
        self.ChooseDialog.setObjectName("Dialog")
        self.ChooseDialog.resize(962, 594)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.ChooseDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 901, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(selected_items[0]))
        self.tableWidget.setRowCount(len(selected_items))
        self.horizontalLayout.addWidget(self.tableWidget)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        self.confirmButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.confirmButton.setObjectName("confirmButton")
        self.horizontalLayout_4.addWidget(self.confirmButton)

        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_4.addWidget(self.cancelButton)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(self.ChooseDialog)
        QtCore.QMetaObject.connectSlotsByName(self.ChooseDialog)

        # Заполнение comboBox и таблицы
        self.populateComboBox()
        self.populateTable(selected_items)

    def retranslateUi(self, choose_dialog):
        _translate = QtCore.QCoreApplication.translate
        choose_dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox.setCurrentText(_translate("Dialog",
                                                "Выберите склад..." if self.operation_type == "Переместить"
                                                else "Выберите клиента..."))
        self.confirmButton.setText(_translate("Dialog", "Подтвердить"))
        self.cancelButton.setText(_translate("Dialog", "Отмена"))

    def populateComboBox(self):
        if self.operation_type == "Продать":
            # Создание объекта курсора
            cursor = self.cursor.cursor()
            # Запрос данных о клиентах из базы данных и заполнение comboBox
            query = "SELECT name FROM Client"
            cursor.execute(query)
            clients = cursor.fetchall()
            for client in clients:
                self.comboBox.addItem(client[0])
        elif self.operation_type == "Переместить":
            # Создание объекта курсора
            cursor = self.cursor.cursor()
            # Запрос названий складов из базы данных и заполнение comboBox
            query = "SELECT name FROM Warehouse"
            cursor.execute(query)
            warehouses = cursor.fetchall()
            for warehouse in warehouses:
                self.comboBox.addItem(warehouse[0])

    def populateTable(self, data):
        # Очистите таблицу перед обновлением данных
        self.tableWidget.clearContents()

        # Установка числа строк и столбцов в таблице
        num_rows = len(data)
        num_cols = len(data[0])
        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)

        # Установка данных ячеек таблицы
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_ChooseDialog(None, [["Данные 1", "Данные 2"], ["Данные 3", "Данные 4"]], "Продать")  # Пример данных
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
