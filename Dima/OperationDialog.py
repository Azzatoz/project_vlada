import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from support_file import SupportClass
from Dima.ChooseDialog import ChooseDialog
from support_file import show_notification


class Ui_OperationDialog(object):
    def __init__(self, operation, Cursor, name):

        self.db_data = {}
        self.name = name
        self.operation_type = operation
        self.original_data = {}
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
        self.find_line.textChanged.connect(lambda text: self.support_instance.search_table(text))
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

        self.c = Cursor
        self.support = SupportClass(self.table_name, self.c, self.table_widget)
        self.operation_action(operation)  # Вызываем метод для установки действий кнопок в зависимости от операции
        self.support.display_table_data()  # Отображаем таблицу
        self.cancel_button.clicked.connect(self.support.cancel)

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

    def display_table_data(self, operation_type):
        if self.connection and self.table_name:
            # Запрос данных из базы данных
            query_data = f"SELECT * FROM {self.table_name}"
            result_data = self.connection.execute(query_data).fetchall()
            initial_result_data = result_data[:]

            # Запрос заголовков таблицы
            query_headers = f"PRAGMA table_info({self.table_name})"
            result_headers = self.connection.execute(query_headers).fetchall()
            headers = [column[1] for column in result_headers]
            count_columns = len(result_headers)

            # Добавление нового заголовка в зависимости от типа операции
            if operation_type == "Продать":
                headers.append("Кому продать")
            elif operation_type == "Переместить":
                headers.append("Переместить в")

            # Установка размеров таблицы и заголовков
            self.table_widget.setRowCount(len(result_data))
            self.table_widget.setColumnCount(
                count_columns + 1)  # Добавляем один столбец для "Переместить в" или "Кому продать"
            self.table_widget.setHorizontalHeaderLabels(headers)

            # Заполнение таблицы данными
            for row_index, row_data in enumerate(result_data):
                for col_index, col_data in enumerate(row_data):
                    if col_data == 'None':
                        col_data = ''
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.table_widget.setItem(row_index, col_index, item)
                    self.original_data[row_index, col_index] = str(col_data)
                    if col_index == 0:
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                    # Добавление данных в новый столбец в зависимости от типа операции
                    if operation_type == "Продать":
                        if col_index == count_columns:
                            item = QtWidgets.QTableWidgetItem("Кому продать")  # Замените на данные о клиенте
                            self.table_widget.setItem(row_index, col_index, item)
                    elif operation_type == "Переместить":
                        if col_index == count_columns:
                            item = QtWidgets.QTableWidgetItem("Переместить в")  # Замените на данные о складе
                            self.table_widget.setItem(row_index, col_index, item)

    # TODO: добавить в support_file
    def open_operation_table_window(self):
        selected_row = self.table_widget.currentRow()
        item = self.table_widget.item(selected_row, 0)
        item_id = item.text()
        for self.row_data in self.db_data:
            if self.row_data[0] == int(item_id):
                operation_table_window = UiOperationTableWindow(self.connection, self.row_data)
                operation_table_window.show()
                UiMainWindow.operation_table_window_instance = operation_table_window

    # TODO: добавить в support_file
    def get_selected_items(self):
        selected_items = []
        for item in self.table_widget.selectedItems():
            selected_items.append(item.text())
        return selected_items

    def operation_action(self, operation_type):
        if operation_type == "Списать":
            self.choose_button.clicked.connect(self.write_off_product)
        elif operation_type in ["Продать", "Переместить"]:
            self.choose_button.clicked.connect(lambda: self.sell_or_move(operation_type))

        # сохраняем внесённые изменения
        self.save_button.clicked.connect(self.support.save)
        self.save_button.clicked.connect(self.write_operation)

    # Метод для списания товара
    def write_off_product(self):
        # Получаем список выделенных строк
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())

        # Если нет выделенных строк, выходим из метода
        if not selected_rows:
            show_notification("Выберите товар на списание")
            return

        # Вызываем метод delete_rows для удаления выделенных строк
        self.support.delete_rows()

    def sell_or_move(self, operation_type):
        selected_items = self.get_selected_items()

        choose_dialog = QtWidgets.QDialog()
        choose_dialog_ui = ChooseDialog(self.c, selected_items, operation_type)

        # Установка интерфейса для диалогового окна
        choose_dialog_ui.verticalLayoutWidget.setParent(choose_dialog)

        # Подключаем сигнал к слоту используя объект диалогового окна
        choose_dialog_ui.data_selected.connect(lambda data: self.handle_sell_move_data(data))

        choose_dialog.show()
        # для сохранения действия в переменной чтобы окно не закрывалось
        Ui_OperationDialog.operation_dialog_instance = choose_dialog

    def handle_sell_move_data(self, data):
        # data содержит информацию о том, кому продавать или куда перемещать товары
        selected_rows = self.table_widget.selectedItems()
        if selected_rows:
            for item in selected_rows:
                row = item.row()
                if isinstance(data, str):
                    item.setText(data)  # Если передана строка (имя клиента или склад), установить ее в ячейку
                else:
                    # Если передан список, каждому элементу списка соответствует строка таблицы
                    for i, val in enumerate(data):
                        if row + i < self.table_widget.rowCount():
                            self.table_widget.setItem(row + i, self.table_widget.columnCount() - 1,
                                                      QtWidgets.QTableWidgetItem(val))

    def write_operation(self):
        # Получаем тип операции
        operation_type = self.operation_type

        # Получаем имя работника
        worker_name = self.name

        # Получаем текущее время
        import time
        current_time = int(time.time())

        # Получаем дополнительные характеристики операции
        additional_characteristics = self.additional_characteristics

        try:
            # Получаем id работника по его имени
            self.c.execute("SELECT id FROM Worker WHERE name=?", (worker_name,))
            worker_row = self.c.fetchone()
            if worker_row:
                worker_id = worker_row[0]
            else:
                # Если работник с таким именем не найден, записываем сообщение в self.info_line и прерываем операцию
                self.info_line.setText(f"Работник с именем '{worker_name}' не найден.")
                return

            # Если операция "Продать", получаем id клиента
            client_id = None
            if operation_type == "Продать":
                # Допустим, у нас есть переменная с именем клиента client_name
                client_name = self.client_name

                # Получаем id клиента по его имени
                self.c.execute("SELECT id FROM Client WHERE name=?", (client_name,))
                client_row = self.c.fetchone()
                if client_row:
                    client_id = client_row[0]
                else:
                    # Если клиент с таким именем не найден, записываем сообщение в self.info_line
                    self.info_line.setText(f"Клиент с именем '{client_name}' не найден.")

            # Вставляем данные операции в таблицу
            self.c.execute("""
                INSERT INTO Operation (type, client_id, worker_id, time, additional_characteristics)
                VALUES (?, ?, ?, ?, ?)
            """, (operation_type, client_id, worker_id, current_time, additional_characteristics))

            # Применяем изменения к базе данных
            self.connection.commit()

            # Удаление выбранного товара из таблицы Current_product для списания и продажи
            if operation_type in ["Списать", "Продать"]:
                selected_row = self.tableWidget.currentRow()
                item = self.tableWidget.item(selected_row, 0)
                item_id = item.text()
                self.c.execute("DELETE FROM Current_product WHERE id=?", (item_id,))
                self.connection.commit()

            # Обработка перемещения или принятия товара в другом складе
            elif operation_type in ["Переместить", "Принять"]:
                # Получаем выбранный склад из comboBox
                selected_warehouse = self.comboBox.currentText()

                # Получаем id выбранного склада
                self.c.execute("SELECT id FROM Warehouse WHERE name=?", (selected_warehouse,))
                warehouse_row = self.c.fetchone()
                if warehouse_row:
                    warehouse_id = warehouse_row[0]
                else:
                    # Если склад с таким именем не найден, выводим сообщение об ошибке
                    self.info_line.setText(f"Склад '{selected_warehouse}' не найден.")
                    return

                # Обновляем информацию о складе у выбранного товара
                selected_rows = self.tableWidget.selectedItems()
                if selected_rows:
                    for item in selected_rows:
                        row = item.row()
                        item_id = self.tableWidget.item(row, 0).text()
                        # Выполняем соответствующий запрос обновления в базе данных
                        if operation_type == "Переместить":
                            self.c.execute("UPDATE Current_product SET warehouse_id=? WHERE id=?",
                                           (warehouse_id, item_id))
                        elif operation_type == "Принять":
                            # Здесь может быть другая логика в зависимости от требований
                            pass

                # Применяем изменения к базе данных
                self.connection.commit()

        except sqlite3.Error as e:
            # В случае ошибки записываем сообщение в self.info_line
            error_message = "Ошибка записи операции в базу данных: " + str(e)
            self.info_line.setText(error_message)


if __name__ == "__main__":
    import sys

    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_OperationDialog("Списать", c, "Иван Иванов")  # тест
    ui.show()
    sys.exit(app.exec_())
