import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from Dima.OperationDialogController import OperationDialogController
from Dima.AddDialog import Ui_AddDialog
from support_file import SupportClass
from support_file import show_notification


# TODO: изменить получение клиента или склада на просто comboBox в OperationDialog (chooseDialog не нужен), Done;
#  добавить добавление нового клиента, Done;
#  чтобы сохранение обрабатывало сразу все данные, Done;
#  добавить обновление в MainWindow (попробовать с помощью commit'a)


class Ui_OperationDialog(object):
    def __init__(self, operation, connection, worker_name):

        self.db_data = {}
        self.original_data = {}
        self.worker_name = worker_name
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

        self.choose_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.choose_comboBox.setObjectName("choose_button")
        self.horizontalLayout.addWidget(self.choose_comboBox)

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
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
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
                                                    operation, connection, self.worker_name)
        self.show()
        # отображаем таблицу с данными
        self.display_current_product_data(self.cursor)
        self.table_widget.cellChanged.connect(self.handle_cell_changed)

        # определяем функции к кнопкам
        self.connect_buttons_events(self.operation_type)

    def retranslateUi(self, operationDialog):
        _translate = QtCore.QCoreApplication.translate
        operationDialog.setWindowTitle(_translate("operationDialog", "operationDialog"))
        self.find_line.setPlaceholderText(_translate("operationDialog", "Найти..."))
        self.cancel_button.setText(_translate("operationDialog", "Отмена"))
        self.check_excel.setText(_translate("operationDialog", "Создать файл Excel"))
        self.check_word.setText(_translate("operationDialog", "Создать файл Word"))
        self.save_button.setText(_translate("operationDialog", "Сохранить"))
        self.info_line.setPlaceholderText(_translate("operationDialog", "Ваши действия..."))

    def show(self):
        self.operationDialog.show()

    def display_current_product_data(self, cursor):
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
        operation_column_title = "Количество на " + self.operation_type.lower()

        # Устанавливаем заголовки таблицы, добавляя новый столбец
        headers = ['ID', 'Наименование', 'Количество на складе', operation_column_title, 'Поставки', 'Склад',
                   'Дата поставки']
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
            self.table_widget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(""))  # Пустая ячейка для нового столбца
            self.table_widget.setItem(row_index, 4, item_operator)
            self.table_widget.setItem(row_index, 5, item_warehouse)
            self.table_widget.setItem(row_index, 6, item_delivery_date)

            # Устанавливаем флаги для ячеек редактирования
            for row_index, row_data in enumerate(result_data):
                for column_index in range(num_cols):
                    item = self.table_widget.item(row_index, column_index)
                    if item and column_index == 3:  # Проверяем, что это столбец с количеством на складе
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    else:
                        if item:
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Убираем флаг редактирования

    def save_operation_data(self):
        """
        Сохраняет данные операции в базу данных и обновляет информацию о товарах.
        """
        # Получаем тип операции и текущее время
        import datetime
        operation_type = self.operation_type
        current_time = datetime.datetime.now().strftime("%d-%m-%Y")

        # Получаем идентификатор работника
        worker_id = self.controller.get_worker_id(self.worker_name)

        # Получаем выбранный элемент из comboBox
        selected_destination = self.choose_comboBox.currentText()

        # Получаем идентификатор клиента или склада
        client_or_warehouse_id = self.controller.get_client_or_warehouse_id(selected_destination)
        print(client_or_warehouse_id)

        # Получаем выбранные товары для операции
        selected_items = self.controller.get_selected_items()
        if not selected_items:
            show_notification("Выберите товары для операции")
            return

        # Вставляем данные об операции
        self.controller.insert_operation_data(operation_type, client_or_warehouse_id, worker_id, current_time,
                                              additional_characteristics=None, selected_items=selected_items)

        # Обновляем информацию о товарах и складе
        self.controller.update_product_information(selected_items, client_or_warehouse_id)

        # После сохранения операции вызываем метод для отображения данных
        self.display_current_product_data(self.cursor)

    def populateComboBox(self):
        cursor = self.cursor
        self.choose_comboBox.clear()  # Очищаем combobox

        if self.operation_type == "Продать":
            # Запрос данных о клиентах из базы данных и заполнение comboBox
            query = "SELECT name FROM Client"
            cursor.execute(query)
            clients = cursor.fetchall()
            for client in clients:
                self.choose_comboBox.addItem(client[0])
        elif self.operation_type == "Переместить":
            # Запрос названий складов из базы данных и заполнение comboBox
            query = "SELECT name FROM Warehouse"
            cursor.execute(query)
            warehouses = cursor.fetchall()
            for warehouse in warehouses:
                self.choose_comboBox.addItem(warehouse[0])

        # Добавляем опцию "Добавить" после основных элементов
        self.choose_comboBox.addItem("Добавить...")
        self.choose_comboBox.activated.connect(self.handleAddItem)
        self.choose_comboBox.activated[str].connect(self.controller.get_client_or_warehouse_id)

    def connect_buttons_events(self, operation_type):
        from Vlada.MainWindow import UiMainWindow
        mainWindow_instance = UiMainWindow(self.worker_name)
        # Подключение событий к обработчикам
        self.save_button.clicked.connect(self.save_operation_data)
        self.cancel_button.clicked.connect(mainWindow_instance.cancel_deletion_row)
        if operation_type == "Списать":
            self.choose_comboBox.clicked.connect(self.controller.write_off_product)
        elif operation_type in ["Продать", "Переместить"]:
            self.populateComboBox()

    def handle_cell_changed(self, row, column):
        """
        Проверяет, есть ли данные в столбце с количеством
        :param row:
        :param column:
        :return:
        """
        if column == 3:  # Проверяем, что изменения произошли в столбце с количеством на операцию
            item = self.table_widget.item(row, column)
            if item:
                new_quantity = item.text()
                # Проверяем, что введены только цифры
                if not new_quantity.isdigit():
                    # # Выводим сообщение об ошибке
                    # QtWidgets.QMessageBox.warning(self.operationDialog, "Ошибка", "Введены некорректные данные. "
                    #                                                               "Пожалуйста, введите число.")
                    # Возвращаем старое значение
                    original_quantity = self.original_data.get((row, column), "")
                    item.setText(original_quantity)
                else:
                    # Проверяем, не превышает ли новое количество на складе
                    max_quantity = int(self.table_widget.item(row, 2).text())  # Количество на складе
                    if int(new_quantity) > max_quantity:
                        # Выводим сообщение об ошибке
                        QtWidgets.QMessageBox.warning(self.operationDialog, "Ошибка", "Введено количество больше, "
                                                                                      "чем имеется на складе.")
                        # Возвращаем старое значение
                        original_quantity = self.original_data.get((row, column), "")
                        item.setText(original_quantity)
                    else:
                        # Сохраняем новое значение
                        self.db_data[(row, column)] = new_quantity

    def handleAddItem(self, index):
        # Проверяем, была ли выбрана опция "Добавить"
        if index == self.choose_comboBox.count() - 1:
            add_dialog = Ui_AddDialog(self.operation_type)
            add_dialog.exec()
            Ui_OperationDialog.add_dialog_instance = add_dialog
            self.populateComboBox()


if __name__ == "__main__":
    import sys

    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_OperationDialog("Продать", c, "Иван Иванов")  # тест
    sys.exit(app.exec_())
