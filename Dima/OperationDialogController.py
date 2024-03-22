import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from support_file import SupportClass
from Dima.ChooseDialog import ChooseDialog
from support_file import show_notification


class OperationDialogController:
    def __init__(self, operation_dialog_instance, support_instance, table_widget, info_line, operation, connection, worker_name):

        self.support_instance = support_instance
        self.operation_dialog_instance = operation_dialog_instance

        self.operation_type = operation
        self.connection = connection
        self.cursor = connection.cursor()
        self.worker_name = worker_name
        self.table_name = "Current_product"
        self.table_widget = table_widget
        self.info_line = info_line

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
        self.support_instance.delete_rows()

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
            self.table_widget.setItem(row_index, 6, item)

    def get_worker_id(self, worker_name):
        try:
            self.cursor.execute("SELECT id FROM Worker WHERE name=?", (worker_name,))
            worker_row = self.cursor.fetchone()
            if worker_row:
                return worker_row[0]
            else:
                self.info_line.setText(f"Работник с именем '{worker_name}' не найден.")
                return None
        except sqlite3.Error as e:
            self.info_line.setText("Ошибка при получении идентификатора работника: " + str(e))
            return None

    def get_client_or_warehouse_id(self, operation_type):
        try:
            if operation_type in ["Продать", "Переместить"]:
                column_headers = [self.table_widget.horizontalHeaderItem(col).text() for col in
                                  range(self.table_widget.columnCount())]
                destination_column_name = "Кому продать" if operation_type == "Продать" else "Переместить в"
                if destination_column_name in column_headers:
                    destination_column_index = column_headers.index(destination_column_name)
                    destination_name = self.table_widget.item(self.table_widget.currentRow(),
                                                              destination_column_index).text()
                    if operation_type == "Продать":
                        self.cursor.execute("SELECT id FROM Client WHERE name=?", (destination_name,))
                    else:
                        self.cursor.execute("SELECT id FROM Warehouse WHERE name=?", (destination_name,))
                    client_or_warehouse_row = self.cursor.fetchone()
                    if client_or_warehouse_row:
                        return client_or_warehouse_row[0]
                    else:
                        self.info_line.setText(
                            f"{'' if operation_type == 'Продать' else 'Склад '}с именем '{destination_name}' не найден.")
                        return None
        except sqlite3.Error as e:
            self.info_line.setText(
                f"Ошибка при получении идентификатора {'клиента' if operation_type == 'Продать' else 'склада'}: " + str(
                    e))
            return None

    def save_operation_data(self):
        # Получаем тип операции и прочие данные
        print("Функция save_operation_data запускается.")
        import datetime
        operation_type = self.operation_type
        current_time = datetime.datetime.now().strftime("%d-%m-%Y")
        worker_id = self.get_worker_id(self.worker_name)
        client_or_warehouse_id = self.get_client_or_warehouse_id(operation_type)
        print(operation_type, current_time, worker_id, client_or_warehouse_id)
        # Получаем информацию о выбранных строках для операции
        selected_rows_data = []
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 6)  # Проверяем ячейку в шестом столбце
            if item is not None and item.text():
                row_data = []
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                print(row_data)
                selected_rows_data.append(row_data)
                print(selected_rows_data)

        # Если нет выбранных строк, показываем уведомление и выходим из функции
        if not selected_rows_data:
            show_notification("Выберите товары для операции")
            return

        # Вставляем данные операции в таблицу для каждой выбранной строки
        print("До цикла в save_operation_data.")
        for selected_row_data in selected_rows_data:
            self.insert_operation_data(operation_type, client_or_warehouse_id, worker_id, current_time,
                                       additional_characteristics=None, selected_row_data=selected_row_data)
        print("После цикла в save_operation_data.")
        # Удаляем выбранные товары из таблицы Current_product для операций "Списать" и "Продать"
        self.delete_selected_product(operation_type)
        print("после удаления в save_operation_data.")
        # Обновляем информацию о складе у выбранных товаров для операции "Переместить"
        if operation_type == "Переместить":
            selected_warehouse = self.comboBox.currentText()
            self.update_warehouse_info(selected_warehouse)

        # После сохранения операции вызываем метод для отображения данных
        self.operation_dialog_instance.display_current_product_data(self.cursor, operation_type)

    def insert_operation_data(self, operation_type, client_or_warehouse_id, worker_id, current_time,
                              additional_characteristics, selected_row_data):
        try:
            print("Функция insert_operation_data запускается.")
            # Вставка данных в таблицу Operation
            self.cursor.execute(
                "INSERT INTO Operation (type, client_id, worker_id, time, additional_characteristics) "
                "VALUES (?, ?, ?, ?, ?)",
                (operation_type, client_or_warehouse_id, worker_id, current_time, additional_characteristics))

            # Получение id только что вставленной операции
            operation_id = self.cursor.lastrowid

            # Вставка данных в таблицу Operation_product
            product_id = selected_row_data[0]  # ID товара на складе
            warehouse_id = selected_row_data[3]  # ID склада
            quantity = selected_row_data[2]  # Количество товара

            self.cursor.execute(
                "INSERT INTO Operation_product (operation_id, product_id, warehouse_id, quantity, condition) "
                "VALUES (?, ?, ?, ?, ?)",
                (operation_id, product_id, warehouse_id, quantity, operation_type))  # Здесь передаем operation_type

            self.connection.commit()
        except sqlite3.Error as e:
            self.info_line.setText("Ошибка при записи данных операции в базу данных: " + str(e))

    def delete_selected_product(self, operation_type):
        try:
            print("Функция delete_selected_product работает.")
            if operation_type in ["Списать", "Продать"]:
                selected_row = self.table_widget.currentRow()
                item = self.table_widget.item(selected_row, 0)
                if item is not None:  # Проверка на None
                    item_id = item.text()
                    self.cursor.execute("DELETE FROM Current_product WHERE id=?", (item_id,))

                    self.connection.commit()
                else:
                    self.info_line.setText("Ошибка: Не удалось получить элемент из таблицы.")
        except sqlite3.Error as e:
            self.info_line.setText("Ошибка при удалении товара из таблицы Current_product: " + str(e))

    def update_warehouse_info(self, selected_warehouse):
        try:
            print("Функция update_warehouse_info работает.")
            self.cursor.execute("SELECT id FROM Warehouse WHERE name=?", (selected_warehouse,))
            warehouse_row = self.cursor.fetchone()
            if warehouse_row:
                warehouse_id = warehouse_row[0]
                selected_rows = self.table_widget.selectedItems()
                if selected_rows:
                    for item in selected_rows:
                        row = item.row()
                        item_id = self.table_widget.item(row, 0).text()
                        self.cursor.execute("UPDATE Current_product SET warehouse_id=? WHERE id=?",
                                            (warehouse_id, item_id))
                    self.connection.commit()
        except sqlite3.Error as e:
            self.info_line.setText("Ошибка при обновлении информации о складе: " + str(e))
