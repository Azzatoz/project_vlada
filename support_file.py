from PyQt5 import QtCore, QtWidgets


class Ui_DialogTable(object):
    table_name = ''
    connection = None
    changes_made = False

    # def setupUi(self, Dialog):
    #     self.original_data = {}
    #     Dialog.setObjectName("Dialog")
    #     Dialog.resize(774, 559)
    #     self.tableWidget = QtWidgets.QTableWidget(Dialog)
    #     self.tableWidget.setGeometry(QtCore.QRect(30, 70, 711, 361))
    #     self.tableWidget.setObjectName("tableWidget")
    #     self.tableWidget.setSortingEnabled(True)
    #     self.tableWidget.itemChanged.connect(self.cell_changed)
    #
    #     self.btnAdd = QtWidgets.QPushButton(Dialog)
    #     self.btnAdd.setGeometry(QtCore.QRect(602, 20, 131, 28))
    #     self.btnAdd.setObjectName("btnAdd")
    #
    #     self.btnDelete = QtWidgets.QPushButton(Dialog)
    #     self.btnDelete.setGeometry(QtCore.QRect(450, 20, 131, 28))
    #     self.btnDelete.setObjectName("btnDelete")
    #
    #     self.btnSave = QtWidgets.QPushButton(Dialog)
    #     self.btnSave.setEnabled(False)
    #     self.btnSave.setGeometry(QtCore.QRect(600, 470, 131, 28))
    #     self.btnSave.setObjectName("btnSave")
    #
    #     self.btnCancel = QtWidgets.QPushButton(Dialog)
    #     self.btnCancel.setEnabled(False)
    #     self.btnCancel.setGeometry(QtCore.QRect(450, 470, 131, 28))
    #     self.btnCancel.setObjectName("btnCancel")
    #
    #     self.notification = QtWidgets.QTextEdit(Dialog)
    #     self.notification.setGeometry(QtCore.QRect(30, 440, 401, 81))
    #     self.notification.setObjectName("textEdit")
    #
    #     self.lineEdit = QtWidgets.QLineEdit(Dialog)
    #     self.lineEdit.setGeometry(QtCore.QRect(30, 40, 350, 22))
    #     self.lineEdit.setObjectName("lineEdit")
    #     self.lineEdit.textChanged.connect(self.search_table)
    #
    #     self.btnAdd.clicked.connect(self.add)
    #     self.btnDelete.clicked.connect(self.delete)
    #     self.btnSave.clicked.connect(self.save)
    #     self.btnCancel.clicked.connect(self.cancel)
    #
    #     self.retranslateUi(Dialog)
    #     QtCore.QMetaObject.connectSlotsByName(Dialog)
    #
    #     self.display_table_data()
    #     self.btnSave.setEnabled(False)
    #     self.btnCancel.setEnabled(False)
    #     for col in range(self.tableWidget.columnCount()):
    #         self.tableWidget.horizontalHeaderItem(col).setTextAlignment(QtCore.Qt.AlignCenter)
    #         self.tableWidget.horizontalHeaderItem(col).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #         self.tableWidget.horizontalHeader().setSectionsClickable(True)
    #         self.tableWidget.horizontalHeader().sectionClicked.connect(self.sort_table_by_column)
    #
    # def retranslateUi(self, Dialog):
    #     _translate = QtCore.QCoreApplication.translate
    #     Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
    #     self.btnAdd.setText(_translate("Dialog", "Добавить"))
    #     self.btnDelete.setText(_translate("Dialog", "Удалить"))
    #     self.btnSave.setText(_translate("Dialog", "Сохранить"))
    #     self.btnCancel.setText(_translate("Dialog", "Отменить"))

    def display_table_data(self):
        if self.connection and self.table_name:
            query_data = f"SELECT * FROM {self.table_name}"
            result_data = self.connection.execute(query_data).fetchall()
            query_headers = f"PRAGMA table_info({self.table_name})"
            result_headers = self.connection.execute(query_headers).fetchall()
            headers = [column[1] for column in result_headers]

            self.tableWidget.setRowCount(len(result_data))
            self.tableWidget.setColumnCount(len(result_headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)

            for row_index, row_data in enumerate(result_data):
                for col_index, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.tableWidget.setItem(row_index, col_index, item)
                    self.original_data[row_index, col_index] = str(col_data)
                    # Заблокировать редактирование ячейки с id
                    if col_index == 0:
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def sort_table_by_column(self, logical_index):
        """
        Сортирует данные по нажатию на заголовок столбца
        """
        column_type = self.get_column_type(logical_index)

        # данные из столбца
        column_data = []
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, logical_index)
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
        sort_order = QtCore.Qt.AscendingOrder if self.tableWidget.horizontalHeader().sortIndicatorOrder() == QtCore.Qt.AscendingOrder else QtCore.Qt.DescendingOrder

        # Применяет сортировку к таблице
        sorted_data = sorted(enumerate(column_data), key=lambda x: x[1],
                             reverse=(sort_order == QtCore.Qt.DescendingOrder))
        for new_row, (old_row, _) in enumerate(sorted_data):
            self.tableWidget.setRowHidden(new_row, False)
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(old_row, col)
                if item:
                    new_item = item.clone()
                    self.tableWidget.setItem(new_row, col, new_item)

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
            self.btnSave.setEnabled(True)
            self.btnCancel.setEnabled(True)
            self.changes_made = True

    def search_table(self, text):
        """
        Выполняет поиск по таблице и скрывает строки, не соответствующие критериям поиска.
        """
        for row in range(self.tableWidget.rowCount()):
            row_hidden = True
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item and text.lower() in item.text().lower():
                    row_hidden = False
                    break

            self.tableWidget.setRowHidden(row, row_hidden)

    def add(self):
        """
        Добавляет новую строку в таблицу
        """
        # Получаем текущее количество строк в таблице
        current_row_count = self.tableWidget.rowCount()

        # Определяем следующий доступный id для новой строки
        new_id = 1
        existing_ids = set(int(self.tableWidget.item(row, 0).text()) for row in range(current_row_count))

        while new_id in existing_ids:
            new_id += 1

        # Добавляем новую строку в интерфейсе и устанавливаем новый id
        self.tableWidget.insertRow(current_row_count)
        item_id = QtWidgets.QTableWidgetItem(str(new_id))
        item_id.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Заблокировать редактирование
        self.tableWidget.setItem(current_row_count, 0, item_id)

        # Разблокируем кнопку сохранения новой таблицы
        self.btnSave.setEnabled(True)
        self.btnCancel.setEnabled(True)

        self.changes_made = True
        self.notification.append("Добавлена новая запись")

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
        self.btnSave.setEnabled(False)
        self.btnCancel.setEnabled(False)
        self.notification.append("Отменены все изменения")

    def delete(self):
        """
        Удаляет выбранные строки / стирает данные в ячейках
        """
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        if selected_rows:
            # Если выделены строки, то удаляем их
            for row in reversed(selected_rows):
                # Получаем id удаляемой строки и удаляем её из базы данных
                deleted_row_id = self.tableWidget.item(row.row(), 0).text() if self.tableWidget.item(row.row(),
                                                                                                     0) is not None else None

                # Удаляем строку из интерфейса
                self.tableWidget.removeRow(row.row())

                # Удаляем строку из базы данных, если id существует
                if deleted_row_id is not None:
                    delete_query = f"DELETE FROM {self.table_name} WHERE id = ?;"
                    self.connection.execute(delete_query, (deleted_row_id,))

        else:
            # Если нет выделенных строк, то очищаем данные в выделенной ячейке (за исключением ячейки с id)
            selected_items = self.tableWidget.selectedItems()
            for item in selected_items:
                if item.column() != 0:  # Проверяем, что это не ячейка с id (предполагаем, что id находится в первой колонке)
                    item.setText("")

        # Разблокируем кнопку сохранения новой таблицы
        self.btnSave.setEnabled(True)
        self.btnCancel.setEnabled(True)

        self.changes_made = True
        self.notification.append("Удалены записи")

    def save(self):
        """
        Сохраняет все внесённые изменения
        """
        if self.changes_made:
            # Получаем старые данные из базы данных
            query_data = f"SELECT * FROM {self.table_name}"
            result_data = self.connection.execute(query_data).fetchall()

            for row in range(self.tableWidget.rowCount()):
                new_data = [
                    self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) is not None else '' for
                    col in range(self.tableWidget.columnCount())]

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
            self.btnSave.setEnabled(False)
            self.btnCancel.setEnabled(False)
            self.notification.append("Изменения успешно сохранены в базе данных")

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
        update_query += ', '.join([f"{self.tableWidget.horizontalHeaderItem(col).text()} = ?" for col in
                                   range(1, len(new_data))])  # Не включаем id в обновление
        update_query += f" WHERE id = ?;"

        with self.connection:
            self.connection.execute(update_query, (*new_data[1:], old_data[0]))

    def set_info(self, table_name, operation_type):
        if operation_type == "списать":
            self.choose_button.setText("Списать")
        elif operation_type == "продать":
            self.choose_button.setText("продать...")
            # выбор клиента, если клиента нет - добавить
        elif operation_type == "переместить":
            # выбор склада куда переместить товар
            self.choose_button.setText("Выбрать товар для перемещения")

    def write_off(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            item_id = self.tableWidget.item(selected_row, 0).text()  # Получаем id товара из выбранной строки
            # Здесь можно написать код для списания товара по его id
            show_notification(f"Товар с id {item_id} успешно списан.")
        else:
            show_notification("Выберите товар для списания.")

    def sell(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            item_id = self.tableWidget.item(selected_row, 0).text()  # Получаем id товара из выбранной строки
            # Здесь можно написать код для продажи товара по его id
            show_notification(f"Товар с id {item_id} успешно продан.")
        else:
            show_notification("Выберите товар для продажи.")

    def move(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            item_id = self.tableWidget.item(selected_row, 0).text()  # Получаем id товара из выбранной строки
            # Здесь можно написать код для перемещения товара по его id
            show_notification(f"Товар с id {item_id} успешно перемещен.")
        else:
            show_notification("Выберите товар для перемещения.")

# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = Ui_DialogTable()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())
