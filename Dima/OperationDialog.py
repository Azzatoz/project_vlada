import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from Dima.OperationDialogController import OperationDialogController
from Dima.ChooseDialog import ChooseDialog
from support_file import SupportClass


class Ui_OperationDialog(object):
    def __init__(self, operation, connection, name):

        self.db_data = {}
        self.original_data = {}
        self.name = name
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.operation_type = operation
        self.table_name = "Current_product"

        self.operationDialog = QtWidgets.QDialog()
        self.operationDialog.setObjectName("operationDialog")
        self.operationDialog.resize(1200, 800)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.operationDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 1141, 751))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.find_line = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.find_line.setInputMask("")
        self.find_line.setText("")
        self.find_line.setObjectName("find_line")
        self.find_line.textChanged.connect(lambda text: self.controller.support_instance.search_table(text))
        self.horizontalLayout.addWidget(self.find_line)

        self.choose_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.choose_button.setObjectName("choose_button")
        self.horizontalLayout.addWidget(self.choose_button)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout.addLayout(self.horizontalLayout_3)

        self.cancel_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.table_widget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.verticalLayout.addWidget(self.table_widget)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.check_excel = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.check_excel.setObjectName("check_excel")
        self.verticalLayout_2.addWidget(self.check_excel)

        self.check_word = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.check_word.setObjectName("check_word")
        self.verticalLayout_2.addWidget(self.check_word)

        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)

        self.save_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy)
        self.save_button.setMinimumSize(QtCore.QSize(100, 20))
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_4.addWidget(self.save_button)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.info_line = QtWidgets.QLineEdit(self.verticalLayoutWidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_line.sizePolicy().hasHeightForWidth())

        self.info_line.setSizePolicy(sizePolicy)
        self.info_line.setMinimumSize(QtCore.QSize(0, 60))
        self.info_line.setInputMask("")
        self.info_line.setText("")
        self.info_line.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.info_line.setObjectName("info_line")

        self.verticalLayout.addWidget(self.info_line)

        self.retranslateUi(self.operationDialog)
        QtCore.QMetaObject.connectSlotsByName(self.operationDialog)

        self.support_instance = SupportClass(self.table_name, self.connection, self.table_widget)
        self.controller = OperationDialogController(self, self.support_instance, self.table_widget, self.info_line,
                                                    operation, connection, self.name)
        self.show()
        # отображаем таблицу с данными
        self.display_current_product_data(self.cursor, self.operation_type)
        # определяем функции к кнопкам
        self.connect_buttons_events(self.operation_type)

    def retranslateUi(self, operationDialog):
        _translate = QtCore.QCoreApplication.translate
        operationDialog.setWindowTitle(_translate("operationDialog", "operationDialog"))
        self.find_line.setPlaceholderText(_translate("operationDialog", "Найти..."))
        self.choose_button.setText(_translate("operationDialog", self.operation_type))
        self.cancel_button.setText(_translate("operationDialog", "Отмена"))
        self.check_excel.setText(_translate("operationDialog", "Создать файл Excel"))
        self.check_word.setText(_translate("operationDialog", "Создать файл Word"))
        self.save_button.setText(_translate("operationDialog", "Сохранить"))
        self.info_line.setPlaceholderText(_translate("operationDialog", "Ваши действия..."))

    def show(self):
        self.operationDialog.show()

    def display_current_product_data(self, cursor, operation_type, selected_row=None, selected_items=None):

        # данные из таблицы Current_product и Product_property
        query_data = f"SELECT cp.id, cp.quantity, cp.delivery_id, cp.warehouse_id, cp.delivery_date, pp.current_product_name " \
                     f"FROM {self.table_name} AS cp " \
                     f"JOIN Product_property AS pp ON cp.id = pp.current_product_id"
        cursor.execute(query_data)
        result_data = cursor.fetchall()

        # имена операций и складов
        operator_names = [
            cursor.execute(
                f"SELECT type FROM Operation WHERE id = {row[2]}"
            ).fetchone()[0] for row in result_data
        ]
        warehouse_names = [
            cursor.execute(
                f"SELECT name FROM Warehouse WHERE id = {row[3]}"
            ).fetchone()[0] for row in result_data
        ]

        # новый столбец с заголовком в зависимости от типа операции
        destination_column_name = "Кому продать" if operation_type == "Продать" else "Переместить в"

        # Устанавливаем заголовки таблицы, добавляя новый столбец
        headers = ['ID', 'Наименование', 'Количество', 'Поставки', 'Склад', 'Дата поставки',
                   destination_column_name]
        num_cols = len(headers)

        # Устанавливаем количество строк и столбцов
        num_rows = len(result_data)

        # Устанавливаем количество строк и столбцов в table_widget
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_cols)
        self.table_widget.setHorizontalHeaderLabels(headers)

        # Заполняем таблицу данными
        for row_index, row_data in enumerate(result_data):
            # Получаем данные строки
            product_id, quantity, delivery_id, warehouse_id, delivery_date, product_name = row_data

            # Создаем элементы QTableWidgetItem для каждого столбца
            item_id = QtWidgets.QTableWidgetItem(str(product_id))
            item_name = QtWidgets.QTableWidgetItem(str(product_name))
            item_quantity = QtWidgets.QTableWidgetItem(str(quantity))
            item_operator = QtWidgets.QTableWidgetItem(operator_names[row_index])
            item_warehouse = QtWidgets.QTableWidgetItem(warehouse_names[row_index])
            item_delivery_date = QtWidgets.QTableWidgetItem(str(delivery_date))

            # Устанавливаем элементы в соответствующие ячейки
            self.table_widget.setItem(row_index, 0, item_id)
            self.table_widget.setItem(row_index, 1, item_name)
            self.table_widget.setItem(row_index, 2, item_quantity)
            self.table_widget.setItem(row_index, 3, item_operator)
            self.table_widget.setItem(row_index, 4, item_warehouse)
            self.table_widget.setItem(row_index, 5, item_delivery_date)

            # Если передана выбранная строка и данные для вставки
            if selected_row is not None and selected_items is not None:
                # Заполняем выбранную строку данными из selected_items
                for col_index, col_data in enumerate(selected_items):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.table_widget.setItem(selected_row, col_index, item)

    def connect_buttons_events(self, operation_type):
        from Vlada.MainWindow import UiMainWindow
        mainWindow_instance = UiMainWindow(self.name)
        # Подключение событий к обработчикам
        self.save_button.clicked.connect(self.controller.save_operation_data)
        self.cancel_button.clicked.connect(mainWindow_instance.cancel_deletion_row)
        if operation_type == "Списать":
            self.choose_button.clicked.connect(self.controller.write_off_product)
        elif operation_type in ["Продать", "Переместить"]:
            self.choose_button.clicked.connect(self.choose_button_clicked)

    def choose_button_clicked(self):
        """
        Передает данные в ChooseDialog для заполнения колонки клиента или склада
        :return:
        """
        selected_items = self.controller.get_selected_items()  # Получаем выбранные элементы из таблицы
        column_headers = []
        for col in range(self.table_widget.columnCount()):
            header = self.table_widget.horizontalHeaderItem(col).text()
            column_headers.append(header)
        choose_dialog = ChooseDialog(self.cursor, selected_items, self.operation_type, column_headers)
        Ui_OperationDialog.operation_dialog_instance = choose_dialog
        choose_dialog.ChooseDialog.show()
        choose_dialog.data_selected.connect(lambda data: self.controller.handle_sell_move_data(data))


if __name__ == "__main__":
    import sys

    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_OperationDialog("Продать", c, "Иван Иванов")  # тест
    sys.exit(app.exec_())
