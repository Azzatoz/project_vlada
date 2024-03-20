from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class ChooseDialog(QtCore.QObject):
    # Определение сигнала
    data_selected = QtCore.pyqtSignal(list)

    def __init__(self, cursor, selected_items, operation_type, column_headers):
        super().__init__()
        self.cursor = cursor
        self.selected_items = selected_items
        self.operation_type = operation_type
        self.column_headers = column_headers
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
        self.tableWidget.setRowCount(len(selected_items))
        self.tableWidget.setColumnCount(len(selected_items[0]))
        self.horizontalLayout.addWidget(self.tableWidget)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        self.confirmButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.clicked.connect(self.confirm_selection)
        self.horizontalLayout_4.addWidget(self.confirmButton)

        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_4.addWidget(self.cancelButton)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(self.ChooseDialog)
        QtCore.QMetaObject.connectSlotsByName(self.ChooseDialog)

        # Заполнение comboBox и таблицы
        self.populateComboBox()
        self.populateTable(selected_items, column_headers)

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
            cursor = self.cursor
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

    def populateTable(self, selected_items, column_headers):
        # Проверяем, есть ли выбранные элементы
        if not selected_items:
            return

        # Устанавливаем количество строк и столбцов в таблице
        num_rows = len(selected_items)
        num_cols = len(selected_items[0]) if num_rows > 0 else 0
        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)

        # Устанавливаем заголовки для столбцов
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        # Заполняем таблицу данными
        for row_index, row_data in enumerate(selected_items):
            for col_index, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_index, col_index, item)

    def confirm_selection(self):
        selected_item = self.get_selected_item()
        self.data_selected.emit([selected_item])  # Отправляем список с одним элементом
        self.ChooseDialog.close()

    def get_selected_item(self):
        return self.comboBox.currentText()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    column_headers = ["Заголовок 1", "Заголовок 2"]  # Заголовки столбцов
    ui = ChooseDialog(conn, [["Данные 1", "Данные 2"], ["Данные 3", "Данные 4"]], "Продать", column_headers)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
