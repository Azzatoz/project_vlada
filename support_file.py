from PyQt5 import QtCore, QtWidgets
from Dima.AutorizationWindow import show_notification


class SupportClass:

    def __init__(self, table_name, connection, table_widget):
        self.changes_made = False
        self.table_name = table_name
        self.connection = connection
        self.table_widget = table_widget
        self.original_data = {}

    def display_table_data(self):
        if self.connection and self.table_name:
            query_data = f"SELECT * FROM {self.table_name}"
            result_data = self.connection.execute(query_data).fetchall()
            query_headers = f"PRAGMA table_info({self.table_name})"
            result_headers = self.connection.execute(query_headers).fetchall()
            headers = [column[1] for column in result_headers]

            self.table_widget.setRowCount(len(result_data))
            self.table_widget.setColumnCount(len(result_headers))
            self.table_widget.setHorizontalHeaderLabels(headers)

            for row_index, row_data in enumerate(result_data):
                for col_index, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.table_widget.setItem(row_index, col_index, item)
                    self.original_data[row_index, col_index] = str(col_data)
                    if col_index == 0:
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def sort_table_by_column(self, logical_index):
        """
        Сортирует данные по нажатию на заголовок столбца
        """
        column_type = self.get_column_type(logical_index)

        # данные из столбца
        column_data = []
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, logical_index)
            if item:
                column_data.append(item.text())
            else:
                column_data.append('')

        # Сортирует данные в зависимости от типа столбца
        if column_type == int:
            column_data = [int(item) for item in column_data]
        elif column_type == float:
            column_data = [float(item) for item in column_data]

        # Определяет порядок сортировки
        sort_order = QtCore.Qt.AscendingOrder if (self.table_widget.horizontalHeader().sortIndicatorOrder() ==
                                                  QtCore.Qt.AscendingOrder) else QtCore.Qt.DescendingOrder

        # Применяет сортировку к таблице
        sorted_data = sorted(enumerate(column_data), key=lambda x: x[1],
                             reverse=(sort_order == QtCore.Qt.DescendingOrder))
        for new_row, (old_row, _) in enumerate(sorted_data):
            self.table_widget.setRowHidden(new_row, False)
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(old_row, col)
                if item:
                    new_item = item.clone()
                    self.table_widget.setItem(new_row, col, new_item)

    def get_column_type(self, logical_index):
        """
        Определяем тип данных в столбце
        """
        column_type = str(self.connection.execute(f"PRAGMA table_info({self.table_name})").fetchall()[logical_index][2])

        if 'INT' in column_type:
            return int
        elif 'REAL' in column_type:
            return float
        else:
            return str

    def cell_changed(self, item):
        """
        Открывает доступ к кнопкам сохранить и отменить при изменении ячеек
        """
        row = item.row()
        col = item.column()
        original_value = self.original_data.get((row, col), '')
        new_value = item.text()

        if original_value != new_value:
            self.table_widget.parent().save_button.setEnabled(True)
            self.table_widget.parent().cancel_button.setEnabled(True)
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

        # Разблокируем кнопку сохранения новой таблицы
        self.table_widget.parent().save_button.setEnabled(True)
        self.table_widget.parent().cancel_button.setEnabled(True)

        self.changes_made = True
        show_notification("Добавлена новая запись")

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
        self.display_table_data()

        # Сбрасываем флаг изменений
        self.changes_made = False
        self.table_widget.parent().save_button.setEnabled(False)
        self.table_widget.parent().cancel_button.setEnabled(False)
        show_notification("Отменены все изменения")

    def delete(self):
        """
        Удаляет выбранные строки / стирает данные в ячейках
        """
        selected_rows = self.table_widget.selectionModel().selectedRows()

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
                    delete_query = f"DELETE FROM {self.table_name} WHERE id = ?;"
                    self.connection.execute(delete_query, (deleted_row_id,))

        else:
            # Если нет выделенных строк, то очищаем данные в выделенной ячейке (за исключением ячейки с id)
            selected_items = self.table_widget.selectedItems()
            for item in selected_items:
                if item.column() != 0:  # Проверяем, что это не ячейка с id
                    # (предполагаем, что id находится в первой колонке)
                    item.setText("")

        # Разблокируем кнопку сохранения новой таблицы
        self.table_widget.parent().save_button.setEnabled(True)
        self.table_widget.parent().cancel_button.setEnabled(True)

        self.changes_made = True
        show_notification("Удалены записи")

    def save(self):
        """
        Сохраняет все внесённые изменения
        """
        if self.changes_made:
            # Получаем старые данные из базы данных
            query_data = f"SELECT * FROM {self.table_name}"
            result_data = self.connection.execute(query_data).fetchall()

            for row in range(self.table_widget.rowCount()):
                new_data = [
                    self.table_widget.item(row, col).text() if self.table_widget.item(row, col) is not None else '' for
                    col in range(self.table_widget.columnCount())]

                if row >= len(result_data):
                    # Новая запись, вставляем её в базу данных
                    self.insert_record(new_data)
                else:
                    old_data = result_data[row]

                    if new_data != old_data:
                        # Обновляем существующую запись в базе данных
                        self.update_record(new_data, old_data)

            # Фиксируем изменения в базе данных
            self.connection.commit()

            # Оповещаем пользователя об успешном сохранении
            QtWidgets.QMessageBox.information(None, "Успешное сохранение", "Изменения успешно сохранены в базе данных.")

            # Сбрасываем флаг изменений и блокируем кнопки
            self.changes_made = False
            self.table_widget.parent().save_button.setEnabled(False)
            self.table_widget.parent().cancel_button.setEnabled(False)
            show_notification("Изменения успешно сохранены в базе данных")

    def insert_record(self, new_data):
        """
        Вставляет новую запись в базу данных
        """
        insert_query = f"INSERT INTO {self.table_name} VALUES ({', '.join(['?' for _ in range(len(new_data))])});"
        with self.connection:
            self.connection.execute(insert_query, new_data)

    def update_record(self, new_data, old_data):
        """
        Обновляет существующую запись в базе данных
        """
        update_query = f"UPDATE {self.table_name} SET "
        update_query += ', '.join([f"{self.table_widget.horizontalHeaderItem(col).text()} = ?" for col in
                                   range(1, len(new_data))])  # Не включаем id в обновление
        update_query += f" WHERE id = ?;"

        with self.connection:
            self.connection.execute(update_query, (*new_data[1:], old_data[0]))

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
