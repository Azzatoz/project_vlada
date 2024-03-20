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

        self.cursor = Cursor
        self.support = SupportClass(self.table_name, self.cursor, self.table_widget)
        self.operation_action(operation)  # Вызываем метод для установки действий кнопок в зависимости от операции
        self.display_current_product_data(self.cursor, self.operation_type)  # Отображаем таблицу
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

    def display_current_product_data(self, cursor, operation_type, selected_row=None, selected_items=None):
        if cursor and self.table_name == 'Current_product':
            try:
                # 1. Получаем данные из таблицы Current_product
                query_data = f"SELECT id, quantity, delivery_id, warehouse_id, delivery_date FROM {self.table_name}"
                cursor.execute(query_data)
                result_data = cursor.fetchall()

                # 2. Получаем имена операторов и складов
                operator_names = [
                    cursor.execute(
                        f"SELECT name FROM Client WHERE id = {row[2]}"
                    ).fetchone()[0] for row in result_data
                ]
                warehouse_names = [
                    cursor.execute(
                        f"SELECT name FROM Warehouse WHERE id = {row[3]}"
                    ).fetchone()[0] for row in result_data
                ]

                # 3. Создаем новый столбец с заголовком в зависимости от типа операции
                destination_column_name = "Кому продать" if operation_type == "Продать" else "Переместить в"

                # 4. Обновляем заголовки таблицы, добавляя новый столбец
                headers = ['ID', 'Количество', 'Оператор', 'Склад', 'Дата поставки', destination_column_name]
                num_cols = len(headers)

                # Устанавливаем количество строк и столбцов
                num_rows = len(result_data)

                # Устанавливаем количество строк и столбцов в table_widget
                self.table_widget.setRowCount(num_rows)
                self.table_widget.setColumnCount(num_cols)
                self.table_widget.setHorizontalHeaderLabels(headers)

                # 5. Заполняем таблицу данными
                for row_index, row_data in enumerate(result_data):
                    # Получаем данные строки
                    product_id, quantity, delivery_id, warehouse_id, delivery_date = row_data

                    # Создаем элементы QTableWidgetItem для каждого столбца
                    item_id = QtWidgets.QTableWidgetItem(str(product_id))
                    item_quantity = QtWidgets.QTableWidgetItem(str(quantity))
                    item_operator = QtWidgets.QTableWidgetItem(operator_names[row_index])
                    item_warehouse = QtWidgets.QTableWidgetItem(warehouse_names[row_index])
                    item_delivery_date = QtWidgets.QTableWidgetItem(str(delivery_date))
                    item_destination = QtWidgets.QTableWidgetItem("")  # Создаем пустой элемент

                    # Устанавливаем элементы в соответствующие ячейки
                    self.table_widget.setItem(row_index, 0, item_id)
                    self.table_widget.setItem(row_index, 1, item_quantity)
                    self.table_widget.setItem(row_index, 2, item_operator)
                    self.table_widget.setItem(row_index, 3, item_warehouse)
                    self.table_widget.setItem(row_index, 4, item_delivery_date)

                    # Если передана выбранная строка и данные для вставки
                    if selected_row is not None and selected_items is not None:
                        # Заполняем выбранную строку данными из selected_items
                        for col_index, col_data in enumerate(selected_items):
                            item = QtWidgets.QTableWidgetItem(str(col_data))
                            self.table_widget.setItem(selected_row, col_index, item)

            except Exception as e:
                print("Ошибка при отображении данных:", e)

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

    # TODO: добавить в support_file
    def get_selected_items(self):
        selected_items = []
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())

        # Проверяем, есть ли выделенные строки
        if not selected_rows:
            return selected_items

        # Получаем все данные из выделенных строк
        for row in selected_rows:
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            selected_items.append(row_data)
        return selected_items

    def sell_or_move(self, operation_type):
        selected_items = self.get_selected_items()  # Получаем выбранные элементы из таблицы

        # Получаем заголовки текущей таблицы
        column_headers = []
        for col in range(self.table_widget.columnCount()):
            header = self.table_widget.horizontalHeaderItem(col).text()
            column_headers.append(header)

        # Создаем экземпляр диалогового окна и передаем выбранные строки и заголовки
        choose_dialog = ChooseDialog(self.cursor, selected_items, operation_type, column_headers)

        # Сохраняем экземпляр диалогового окна в переменной, чтобы окно не закрывалось
        Ui_OperationDialog.operation_dialog_instance = choose_dialog

        # Отображаем диалоговое окно
        choose_dialog.ChooseDialog.show()

        # Подключаем сигнал к слоту для передачи данных после подтверждения
        choose_dialog.data_selected.connect(lambda data: self.handle_sell_move_data(data))

    def handle_sell_move_data(self, selected_destination):
        # Получаем список индексов выбранных строк
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())

        # Проверяем, есть ли выделенные строки
        if not selected_rows:
            return

        # Преобразуем selected_destination в строку, если это список
        selected_destination = selected_destination[0] if isinstance(selected_destination,
                                                                     list) else selected_destination

        # Устанавливаем выбранный элемент в каждую выбранную строку
        for row_index in selected_rows:
            item = QtWidgets.QTableWidgetItem(str(selected_destination))
            self.table_widget.setItem(row_index, 5, item)

    def write_operation(self, additional_characteristics=None):
        # Получаем тип операции
        operation_type = self.operation_type

        # Получаем имя работника
        worker_name = self.name

        # Получаем текущее время
        import time
        current_time = int(time.time())

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
                selected_row = self.table_widget.currentRow()
                item = self.table_widget.item(selected_row, 0)
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
                selected_rows = self.table_widget.selectedItems()
                if selected_rows:
                    for item in selected_rows:
                        row = item.row()
                        item_id = self.table_widget.item(row, 0).text()
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
    ui = Ui_OperationDialog("Продать", c, "Иван Иванов")  # тест
    ui.show()
    sys.exit(app.exec_())
