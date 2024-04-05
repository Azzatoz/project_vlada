from PyQt5 import QtCore, QtWidgets
import re


def show_notification(message):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setText(message)
    msg_box.exec_()


class SupportClass:

    def __init__(self, table_name, connection, table_widget):
        self.changes_made = False
        self.table_name = table_name
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.table_widget = table_widget
        self.original_data = {}
        self.table_widget.sort_order = None
        self.row_id = None
        self.result_data = []
        self.initial_result_data = []
        self.count_columns = None
        self.headers = None
        self.current_column_names = None
        self.deleted_rows_op_pr = []
        self.deleted_rows_prod_pr = []
        self.deleted_rows_cur_pr = []
        self.column_names = {
            'Operation': ["Идентификатор", "Тип операции", "Имя клиента", "Имя сотрудника", "Время",
                          "Другие характеристики"],
            'Operation_product': ["Идентификатор", "Товар", "Склад", "Количество", "Состояние"],
            'Worker': ["Идентификатор", "Имя сотрудника", "День рождения", "Номер телефона",
                       "Должность", "Логин", "Пароль"],
            'Client': ["Идентификатор", "Имя клиента", "Номер телефона", "Другие данные"],
            'Positions': ["Идентификатор", "Название должности", "Зарплата", "Уровень доступа"],
            'Warehouse': ["Идентификатор", "Номер склада", "Адрес", "Координаты", "Геолокация", "Имеющиеся товары"]
        }

    def display_table_data(self, row_id=None, existing_data=None):
        if existing_data:
            self.result_data = existing_data

        else:
            if self.connection and self.table_name:
                query_headers = (f"SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = "
                                 f"'{self.table_name}' ORDER BY ordinal_position")
                self.cursor.execute(query_headers)
                result_headers = self.cursor.fetchall()
                self.headers = [column[0] for column in result_headers if column[0] != 'operation_id']
                self.count_columns = len(self.headers)
                columns = ', '.join(self.headers)
                query_data = f"SELECT {columns} FROM {self.table_name}"
                if self.table_name == 'Operation_product':
                    query_data += f" WHERE operation_id = {row_id}"
                self.cursor.execute(query_data)
                self.result_data = self.cursor.fetchall()
                self.initial_result_data = self.result_data[:]
                self.row_id = row_id

                self.current_column_names = self.column_names.get(self.table_name, [])

                self.table_widget.setColumnCount(self.count_columns)
                self.table_widget.setHorizontalHeaderLabels(self.current_column_names)

                if self.table_name == 'Operation':
                    client_names = []
                    for row in self.result_data:
                        if row[2] is not None:
                            self.cursor.execute(
                                f"SELECT name FROM Client WHERE id = {row[2]}"
                            )
                            result = self.cursor.fetchone()
                            client_name = result[0] if result is not None else ''
                            client_names.append(client_name)
                        else:
                            client_names.append('')

                    worker_names = []
                    for row in self.result_data:
                        self.cursor.execute(
                            f"SELECT name FROM Worker WHERE id = {row[3]}"
                        )
                        result = self.cursor.fetchone()
                        worker_name = result[0] if result is not None else ''
                        worker_names.append(worker_name)

                    for row_index, row_data in enumerate(self.result_data):
                        client_name = client_names[row_index] if row_index < len(client_names) else ""
                        worker_name = worker_names[row_index] if row_index < len(worker_names) else ""
                        new_row_data = row_data[:2] + (client_name, worker_name) + row_data[4:]
                        self.result_data[row_index] = new_row_data

                elif self.table_name == 'Operation_product':
                    product_property_names = []
                    for row in self.result_data:
                        self.cursor.execute(
                            f"SELECT DISTINCT current_product_name FROM Product_property "
                            f"WHERE id = {row[1]}"
                        )
                        result = self.cursor.fetchone()
                        product_property_name = result[0] if result is not None else ''
                        product_property_names.append(product_property_name)

                    warehouse_names = []
                    for row in self.result_data:
                        self.cursor.execute(
                            f"SELECT name FROM Warehouse WHERE id = {row[2]}"
                        )
                        result = self.cursor.fetchone()
                        warehouse_name = result[0] if result is not None else ''
                        warehouse_names.append(warehouse_name)

                    for row_index, row_data in enumerate(self.result_data):
                        product_property_name = product_property_names[row_index] \
                            if row_index < len(product_property_names) else ""
                        warehouse_name = warehouse_names[row_index] if row_index < len(warehouse_names) else ""
                        new_row_data = row_data[:1] + (product_property_name, warehouse_name) + row_data[3:]
                        self.result_data[row_index] = new_row_data

                elif self.table_name == 'Worker':
                    position_names = []
                    for row in self.result_data:
                        self.cursor.execute(
                            f"SELECT name_position FROM Positions "
                            f"WHERE id = {row[4]}"
                        )
                        result = self.cursor.fetchone()
                        position_name = result[0] if result is not None else ''
                        position_names.append(position_name)

                    for row_index, row_data in enumerate(self.result_data):
                        name_position = position_names[row_index] if row_index < len(position_names) else ""
                        new_row_data = row_data[:4] + (name_position, ) + row_data[5:]
                        self.result_data[row_index] = new_row_data

        self.table_widget.setRowCount(len(self.result_data))

        for row_index, row_data in enumerate(self.result_data):
            for col_index, col_data in enumerate(row_data):
                if col_data is None:
                    col_data = ''
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.table_widget.setItem(row_index, col_index, item)
                self.original_data[row_index, col_index] = str(col_data)
                if col_index == 0:
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        return self.initial_result_data, self.result_data, self.count_columns, self.headers

    def get_visible_data(self):
        """
        Извлекает данные из видимых строк таблицы
        :return:
        """
        visible_data = []
        for row in range(self.table_widget.rowCount()):
            if not self.table_widget.isRowHidden(row):
                visible_row_data = []
                for column in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, column)
                    if item is not None:
                        visible_row_data.append(item.text())
                    else:
                        visible_row_data.append('')
                visible_data.append(visible_row_data)
        return visible_data

    def sort_data_by_column(self, column_index):
        """
        Сортирует данные
        :param column_index:
        :return:
        """
        current_order = self.table_widget.sort_order
        if current_order is None:
            current_order = True
        else:
            current_order = not current_order

        visible_data = self.get_visible_data()
        sorted_data = sorted(visible_data, key=lambda x: x[column_index], reverse=current_order)

        row_index = 0
        for row_data in sorted_data:
            for column_index, cell_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(cell_data))
                self.table_widget.setItem(row_index, column_index, item)
            row_index += 1

        self.table_widget.sort_order = current_order

    def cell_changed(self, item):
        """
        Открывает доступ к кнопкам сохранить и отменить при изменении ячеек
        """
        row = item.row()
        col = item.column()
        original_value = self.original_data.get((row, col), '')
        new_value = item.text()

        if original_value != new_value:
            # self.table_widget.parent().save_button.setEnabled(True)
            # self.table_widget.parent().cancel_button.setEnabled(True)
            self.changes_made = True

    def search_table(self, text):
        """
        Выполняет поиск по таблице и скрывает строки, не соответствующие критериям поиска.
        """
        for row in range(self.table_widget.rowCount()):
            row_hidden = True
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item and text.lower() in item.text().lower():
                    row_hidden = False
                    break

            self.table_widget.setRowHidden(row, row_hidden)

    def add(self):
        """
        Добавляет новую строку в таблицу
        """
        # Получаем текущее количество строк в таблице
        current_row_count = self.table_widget.rowCount()

        # Определяем следующий доступный id для новой строки
        new_id = 1
        existing_ids = set(int(self.table_widget.item(row, 0).text()) for row in range(current_row_count))

        while new_id in existing_ids:
            new_id += 1

        # Добавляем новую строку в интерфейсе и устанавливаем новый id
        self.table_widget.insertRow(current_row_count)
        item_id = QtWidgets.QTableWidgetItem(str(new_id))
        item_id.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Заблокировать редактирование
        self.table_widget.setItem(current_row_count, 0, item_id)

        # Заполнение новой строки пустыми значениями
        for column in range(1, self.table_widget.columnCount()):
            item = QtWidgets.QTableWidgetItem('')
            self.table_widget.setItem(current_row_count, column, item)

    def cancel(self):
        """
        Отменяет все изменения
        """
        if self.changes_made:
            # Если были внесены изменения, спрашиваем пользователя о подтверждении отмены
            confirmation = QtWidgets.QMessageBox.question(
                None,
                "Подтверждение отмены",
                "Вы уверены, что хотите отменить все изменения?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )

            if confirmation == QtWidgets.QMessageBox.No:
                return

        # Восстанавливаем исходные данные
        self.display_table_data(self.row_id, self.result_data)

        # Сбрасываем флаг изменений
        self.changes_made = False
        # self.table_widget.parent().save_button.setEnabled(False)
        # self.table_widget.parent().cancel_button.setEnabled(False)
        show_notification("Отменены все изменения")

    def delete_rows(self):
        """
        Удаляет выбранные строки / стирает данные в ячейках
        """
        selected_rows = self.table_widget.selectionModel().selectedRows()
        deleted_row_ids = []
        deleted_rows_dict = {}

        if selected_rows:
            # Если выделены строки, то удаляем их
            for row in reversed(selected_rows):
                # Получаем id удаляемой строки и удаляем её из базы данных
                deleted_row_id = self.table_widget.item(row.row(), 0).text() if (
                        self.table_widget.item(row.row(), 0) is not None) else None

                # Удаляем строку из интерфейса
                self.table_widget.removeRow(row.row())

                # Удаляем строку из базы данных, если id существует
                if deleted_row_id is not None:
                    if self.table_name == 'Operation':
                        select_query = "SELECT * FROM Operation_product WHERE operation_id = %s"
                        self.cursor.execute(select_query, (deleted_row_id,))
                        self.deleted_rows_op_pr.append(self.cursor.fetchall())

                        select_query = "SELECT product_id FROM Operation_product WHERE operation_id = %s"
                        self.cursor.execute(select_query, (deleted_row_id,))
                        prod_id = self.cursor.fetchall()

                        prod_id_values = [row[0] for row in prod_id]
                        placeholders_string = ', '.join(['%s'] * len(prod_id_values))

                        select_query = f"SELECT * FROM Product_property WHERE id IN ({placeholders_string})"
                        self.cursor.execute(select_query, prod_id_values)
                        self.deleted_rows_prod_pr.append(self.cursor.fetchall())

                        select_query = f"SELECT * FROM Current_product WHERE id IN ({placeholders_string})"
                        self.cursor.execute(select_query, prod_id_values)
                        self.deleted_rows_cur_pr.append(self.cursor.fetchall())

                        deleted_rows_dict["Current_product"] = self.deleted_rows_cur_pr
                        deleted_rows_dict["Product_property"] = self.deleted_rows_prod_pr
                        deleted_rows_dict["Operation_product"] = self.deleted_rows_op_pr

                    delete_query = f"DELETE FROM {self.table_name} WHERE id = %s;"
                    self.cursor.execute(delete_query, (deleted_row_id,))
                    deleted_row_ids.append(deleted_row_id)

        else:
            # Если нет выделенных строк, то очищаем данные в выделенной ячейке (за исключением ячейки с id)
            selected_items = self.table_widget.selectedItems()
            if not selected_rows and not selected_items:
                # Если ни одна запись не выбрана и нет выделенных ячеек, выводим сообщение
                show_notification("Вы не выбрали ни одной записи")
            for item in selected_items:
                if item.column() != 0:  # Проверяем, что это не ячейка с id
                    # (предполагаем, что id находится в первой колонке)
                    item.setText("")
            if selected_rows or selected_items:
                show_notification("Удалены записи")
        return deleted_row_ids, deleted_rows_dict

    @staticmethod
    def validate_item(item_text, name_col, initial_name_col):
        if initial_name_col == 'birthday':
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', item_text):
                show_notification(f"Неправильный формат даты(YYYY-MM-DD) в столбце {name_col}.")
                return False
        elif initial_name_col == 'phone_number':
            if not re.match(r'^\d{1,15}$', item_text):
                show_notification(f"Неправильный формат номера телефона (максимум 15 чисел) в столбце {name_col}.")
                return False
        elif initial_name_col == 'username':
            if not re.match(r'^[a-zA-Z0-9_]{5,}$', item_text):
                show_notification(f"Неправильный формат логина в столбце {name_col}.")
                return False
        elif initial_name_col == 'password':
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', item_text):
                show_notification(f"Неправильный формат пароля в столбце {name_col}.")
                return False
        return True

    def save(self, new_position=None):
        """
        Сохраняет все внесённые изменения
        """
        # Получаем старые данные из базы данных
        query_data = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query_data)
        result_data = self.cursor.fetchall()

        result_data.clear()

        for row in range(self.table_widget.rowCount()):
            new_data = [
                self.table_widget.item(row, col).text() if self.table_widget.item(row, col) is not None else '' for
                col in range(self.table_widget.columnCount())]

            # Проверяем каждый элемент данных перед сохранением
            for col, item_text in enumerate(new_data[1:], start=1):
                name_col = self.current_column_names[col]
                initial_name_col = self.headers[col]
                if not self.validate_item(item_text, name_col, initial_name_col):
                    return

            result_data.append(new_data)

            if row >= len(self.result_data):
                # Новая запись, вставляем её в базу данных
                if self.table_name == 'Worker':
                    new_data[4] = new_position[1]
                self.insert_record(new_data)
            else:
                old_data = self.result_data[row]
                initial_old_data = self.initial_result_data[row]

                if self.table_name not in ['Operation', 'Operation_product', 'Worker']:

                    if new_data != old_data:
                        # Обновляем существующую запись в базе данных
                        self.update_record(new_data, old_data)

                elif self.table_name == 'Worker':
                    if new_data[4] != old_data[4]:
                        new_data[4] = new_position[1]
                    else:
                        new_data[4] = initial_old_data[4]

                    self.update_record(new_data, old_data)

            # Фиксируем изменения в базе данных
        self.connection.commit()

        show_notification("Изменения успешно сохранены в базе данных")

    def insert_record(self, new_data):
        """
        Вставляет новую запись в базу данных
        """
        insert_query = (f"INSERT IGNORE INTO {self.table_name} VALUES "
                        f"({', '.join(['%s' for _ in range(len(new_data))])});")
        self.cursor.execute(insert_query, new_data)
        self.connection.commit()

    def update_record(self, new_data, old_data):
        """
        Обновляет существующую запись в базе данных
        """
        update_query = f"UPDATE {self.table_name} SET "
        update_query += ', '.join(
            [f"{self.headers[col]} = %s" for col in range(1, len(new_data))])
        update_query += " WHERE id = %s;"

        data_to_update = new_data[1:] + [old_data[0]]

        self.cursor.execute(update_query, data_to_update)
        self.connection.commit()

    def write_off(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            item_id = self.table_widget.item(selected_row, 0).text()  # Получаем id товара из выбранной строки
            # Здесь можно написать код для списания товара по его id
            show_notification(f"Товар с id {item_id} успешно списан.")
        else:
            show_notification("Выберите товар для списания.")

    def sell(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            item_id = self.table_widget.item(selected_row, 0).text()  # Получаем id товара из выбранной строки
            # Здесь можно написать код для продажи товара по его id
            show_notification(f"Товар с id {item_id} успешно продан.")
        else:
            show_notification("Выберите товар для продажи.")

    def move(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            item_id = self.table_widget.item(selected_row, 0).text()  # Получаем id товара из выбранной строки
            # Здесь можно написать код для перемещения товара по его id
            show_notification(f"Товар с id {item_id} успешно перемещен.")
        else:
            show_notification("Выберите товар для перемещения.")
