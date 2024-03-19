import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from support_file import SupportClass


class Ui_OperationWindow(object):
    def __init__(self, operation, cursor, name):

        self.name = name
        self.operation_type = operation
        self.original_data = {}
        self.table_name = "Current_product"

        self.operationWindow = QtWidgets.QDialog()
        self.operationWindow.setObjectName("OperationWindow")
        self.operationWindow.resize(1620, 960)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.operationWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(100, 60, 1400, 860))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.choose_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.choose_button.setEnabled(True)
        self.choose_button.setObjectName("choose_button")
        self.horizontalLayout_2.addWidget(self.choose_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.save_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.save_button.setEnabled(True)
        self.save_button.setMouseTracking(False)
        self.save_button.setCheckable(False)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.cancel_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(self.operationWindow)
        QtCore.QMetaObject.connectSlotsByName(self.operationWindow)

        self.cursor = cursor
        self.support = SupportClass(self.table_name, cursor, self.tableWidget)
        self.operation_action(operation)  # Вызываем метод для установки действий кнопок в зависимости от операции
        self.support.display_table_data()  # Отображаем таблицу

    def retranslateUi(self, OperationWindow):
        _translate = QtCore.QCoreApplication.translate
        OperationWindow.setWindowTitle(_translate("OperationWindow", "Окно операции"))
        self.choose_button.setText(_translate("OperationWindow", self.operation_type))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.save_button.setText(_translate("OperationWindow", "Выполнить"))
        self.cancel_button.setText(_translate("OperationWindow", "Отмена"))

    def show(self):
        self.operationWindow.show()

    def operation_action(self, operation_type):
        if operation_type == "Списать":
            self.choose_button.clicked.connect(self.write_off_product_and_record_operation)
        elif operation_type == "Продать":
            self.choose_button.clicked.connect(self.support.sell)
            # выбор клиента, если клиента нет - добавить
        elif operation_type == "Переместить":
            # выбор склада куда переместить товар
            self.choose_button.clicked.connect(self.support.move)

        # сохраняем внесённые изменения
        self.save_button.clicked.connect(self.support.save)

    def write_off_product_and_record_operation(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self.operationWindow, "Предупреждение", "Выберите товары для списания!")
            return

        # Получите данные о выбранных товарах и выполните операцию списания,
        # напишите логику для записи операции в базу данных
        # Пример:
        operation_type = "Списание"
        worker_id = self.get_current_worker_id()  # Получить ID текущего работника
        time = self.get_current_time()  # Получить текущее время
        additional_characteristics = "Дополнительные характеристики"  # Например, комментарий к списанию

        # Запись операции в базу данных
        self.cursor.execute("INSERT INTO Operation (type, worker_id, time, additional_characteristics) "
                            "VALUES (?, ?, ?, ?)", (operation_type, worker_id, time, additional_characteristics))
        operation_id = self.cursor.lastrowid  # Получить ID только что добавленной операции

        # Запись товаров, которые списываются, в таблицу Operation_product
        for row in range(0, len(selected_items), self.tableWidget.columnCount()):
            product_id = int(selected_items[row].text())  # Получить ID товара из выделенной строки
            quantity = int(selected_items[row + 1].text())  # Получить количество товара
            condition = "Списано"  # Условие можно уточнить или оставить по умолчанию
            self.cursor.execute("INSERT INTO Operation_product (operation_id, product_id, quantity, condition) "
                                "VALUES (?, ?, ?, ?)", (operation_id, product_id, quantity, condition))

        # Подтверждение изменений в базе данных
        self.conn.commit()
        QtWidgets.QMessageBox.information(self.operationWindow, "Информация", "Товары успешно списаны!")

    def get_current_worker_id(self):
        # Здесь нужно реализовать метод, который возвращает ID текущего работника Например, если вы вводите имя
        # работника при входе в систему, можете использовать его для поиска ID в базе данных В этом примере
        # предположим, что у вас есть переменная self.name, содержащая имя текущего работника
        self.cursor.execute("SELECT id FROM Worker WHERE name=?", (self.name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_current_time(self):
        # Здесь нужно реализовать метод, который возвращает текущее время
        # Примерно так можно получить текущее время, но вам может потребоваться другой способ в вашем приложении
        return QtCore.QDateTime.currentDateTime().toPyDateTime()


    # def write_off_product_and_record_operation(self):
    #     # Списываем товар
    #     self.support.write_off()
    #
    #     # Записываем операцию в таблицу Operation
    #     operation_type = self.operation_type
    #     self.insert_operation_record(operation_type)
    #
    #     # Записываем операцию в другую таблицу
    #     self.record_operation(operation_type)
    #
    # def insert_operation_record(self, operation_type, item_id=None):
    #     """
    #     Вставляет запись о действии в таблицу Operation
    #     """
    #     if self.connection is None:
    #         show_notification("Отсутствует соединение с базой данных.")
    #         return
    #
    #     insert_query = """
    #         INSERT INTO Operation (type, client_id, worker_id, time, additional_characteristics)
    #         VALUES (?, NULL, NULL, ?, NULL);
    #     """
    #     current_time = int(QtCore.QDateTime.currentDateTime().toSecsSinceEpoch())
    #
    #     with self.connection:
    #         self.connection.execute(insert_query, (operation_type, current_time))
    #
    # # Новый метод для записи операции в другую таблицу
    # def record_operation(self, operation_type, additional_data=None):
    #     # Пример: если операция типа "Списать" и требуется дополнительные данные,
    #     # мы можем передать их в этот метод и использовать при записи
    #     if operation_type == "Списать" and additional_data:
    #         # Пример: запись дополнительных данных в другую таблицу
    #         pass
    #     # TODO: Добавить условия для других типов операций


if __name__ == "__main__":
    import sys

    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_OperationWindow("Списать", c, "Иван Иванов")  # тест
    ui.show()
    sys.exit(app.exec_())
