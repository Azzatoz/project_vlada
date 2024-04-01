import mysql.connector
from support_file import show_notification


class OperationDialogController:
    def __init__(self, operation_dialog_instance, support_instance, table_widget, info_line, operation, connection,
                 worker_name):

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
        # Проходим по всем строкам таблицы
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 4)

            # Проверяем, заполнен ли четвертый столбец (количество на...)
            if item is not None and item.text():
                row_data = []

                # Получаем все данные из строки
                for col in range(self.table_widget.columnCount()):
                    cell_item = self.table_widget.item(row, col)
                    if cell_item is not None:
                        row_data.append(cell_item.text())
                    else:
                        row_data.append("")

                selected_items.append(row_data)
        return selected_items

    def get_worker_id(self, worker_name):
        try:
            self.cursor.execute("SELECT id FROM Worker WHERE name=%s", (worker_name,))
            worker_row = self.cursor.fetchone()
            if worker_row:
                return worker_row[0]
            else:
                self.info_line.setText(f"Работник с именем '{worker_name}' не найден.")
                return None
        except sqlite3.Error as e:
            self.info_line.setText("Ошибка при получении идентификатора работника: " + str(e))
            return None

    def get_client_or_warehouse_id(self, selected_destination):
        try:
            if self.operation_type == "Продать":
                self.cursor.execute("SELECT id FROM Client WHERE name=%s", (selected_destination,))
            else:
                self.cursor.execute("SELECT id FROM Warehouse WHERE name=%s", (selected_destination,))
            client_or_warehouse_row = self.cursor.fetchone()
            if client_or_warehouse_row:
                return client_or_warehouse_row[0]
            else:
                self.info_line.setText(
                    f"{'' if self.operation_type == 'Продать' else 'Склад '}с именем '{selected_destination}' не найден.")
                return None
        except sqlite3.Error as e:
            self.info_line.setText(
                f"Ошибка при получении идентификатора {'клиента' if self.operation_type == 'Продать' else 'склада'}: " + str(
                    e))
            return None

    def get_warehouse_id(self, warehouse_name):
        warehouse = warehouse_name
        self.cursor.execute("SELECT id FROM Warehouse WHERE name=%s", (warehouse,))
        warehouse_row = self.cursor.fetchone()

        return warehouse_row[0]

    def insert_operation_data(self, operation_type, client_or_warehouse_id, worker_id, current_time,
                              additional_characteristics, selected_items):
        try:
            # Вставляем данные операции в таблицу
            self.cursor.execute(
                "INSERT INTO Operation (type, client_id, worker_id, time, additional_characteristics) "
                "VALUES (%s, %s, %s, %s, %s)",
                (operation_type, client_or_warehouse_id, worker_id, current_time, additional_characteristics))

            # Получаем id только что вставленной операции
            operation_id = self.cursor.lastrowid
            for selected_row_data in selected_items:
                product_id = selected_row_data[0]  # ID товара на складе
                quantity = int(selected_row_data[3])
                quantity_to_operate = int(selected_row_data[4])  # Количество для операции
                warehouse_id = self.get_warehouse_id(selected_row_data[6])
                # Проверяем, что количество для операции меньше или равно общему количеству товара на складе
                if quantity_to_operate <= quantity:  # Общее количество товара
                    self.cursor.execute(
                        "INSERT INTO Operation_product (operation_id, product_id, warehouse_id, quantity, condition_type)"
                        "VALUES (%s, %s, %s, %s, %s)",
                        (operation_id, product_id, warehouse_id, quantity_to_operate, operation_type))
                else:
                    self.info_line.setText(
                        "Ошибка: Количество для операции превышает общее количество товара на складе.")
                    return

            self.connection.commit()
        except mysql.connector.Error as e:
            self.info_line.setText("Ошибка при записи данных операции в базу данных: " + str(e))

    def update_product_information(self, selected_items, selected_warehouse_id=None):
        try:
            if selected_items:
                for selected_row_data in selected_items:
                    item_id = selected_row_data[0]  # ID товара на складе
                    quantity_in_warehouse = int(selected_row_data[3])
                    print(selected_items)
                    quantity_to_operate = int(selected_row_data[4])
                    new_quantity_for_warehouse = quantity_in_warehouse - quantity_to_operate

                    # Обновляем информацию о складе, если указан конкретный склад
                    if selected_warehouse_id:
                        self.cursor.execute("UPDATE Current_product SET warehouse_id=%s WHERE id=%s",
                                            (selected_warehouse_id, item_id))

                        # меняем изначальное количество товара
                        self.cursor.execute("UPDATE Current_product SET quantity=%s WHERE id=%s",
                                            (new_quantity_for_warehouse, item_id))

                self.connection.commit()
        except mysql.connector.Error as e:
            self.info_line.setText("Ошибка при обновлении информации о товаре: " + str(e))
