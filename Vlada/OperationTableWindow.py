from PyQt5 import QtCore, QtWidgets
from support_file import SupportClass


class UiOperationTableWindow(QtWidgets.QDialog):
    def __init__(self, cursor, row_data):
        super(UiOperationTableWindow, self).__init__()

        self.cursor = cursor
        self.row_data = row_data
        self.table_name = 'Operation_product'
        self.initial_result_data = []

        self.setObjectName("Dialog")
        self.resize(1200, 800)
        self.data_edit = QtWidgets.QTextEdit(self)
        self.data_edit.setReadOnly(True)
        self.data_edit.setGeometry(QtCore.QRect(90, 60, 651, 231))
        self.data_edit.setObjectName("data_edit")
        self.open_word_btn = QtWidgets.QPushButton(self)
        self.open_word_btn.setGeometry(QtCore.QRect(920, 60, 191, 81))
        self.open_word_btn.setObjectName("open_word_btn")
        self.open_excel_btn = QtWidgets.QPushButton(self)
        self.open_excel_btn.setGeometry(QtCore.QRect(920, 150, 191, 81))
        self.open_excel_btn.setObjectName("open_excel_btn")
        self.search_edit = QtWidgets.QLineEdit(self)
        self.search_edit.setGeometry(QtCore.QRect(90, 330, 651, 22))
        self.search_edit.setObjectName("search_edit")
        self.search_edit.setPlaceholderText("Искать:")
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(90, 360, 1021, 371))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.delete_btn = QtWidgets.QPushButton(self)
        self.delete_btn.setGeometry(QtCore.QRect(1020, 320, 93, 28))
        self.delete_btn.setObjectName("delete_btn")
        self.return_btn = QtWidgets.QPushButton(self)
        self.return_btn.setGeometry(QtCore.QRect(910, 320, 93, 28))
        self.return_btn.setObjectName("return_btn")
        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setGeometry(QtCore.QRect(1020, 740, 93, 28))
        self.cancel_button.setObjectName("cancel_button")
        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setGeometry(QtCore.QRect(910, 740, 93, 28))
        self.save_button.setObjectName("save_button")

        self.disable_buttons()
        self.print_row_data()
        self.support_instance = SupportClass(self.table_name, self.cursor, self.table_widget)
        self.initial_result_data, result_data, count_columns = (
            self.support_instance.display_table_data(self.row_data[0]))
        self.search_edit.textChanged.connect(lambda text: self.support_instance.search_table(text))
        self.table_widget.horizontalHeader().sectionClicked.connect(
            lambda clicked_column: self.support_instance.sort_data_by_column(clicked_column))
        self.delete_btn.clicked.connect(lambda: self.button_action("delete"))
        self.save_button.clicked.connect(lambda: self.button_action("save"))
        self.cancel_button.clicked.connect(lambda: self.button_action("cancel"))
        self.return_btn.clicked.connect(self.return_product)

        self.re_translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.open_word_btn.setText(_translate("Dialog", "Открыть word-документ"))
        self.open_excel_btn.setText(_translate("Dialog", "Открыть excel-документ"))
        self.delete_btn.setText(_translate("Dialog", "Удалить"))
        self.return_btn.setText(_translate("Dialog", "Вернуть"))
        self.cancel_button.setText(_translate("Dialog", "Отмена"))
        self.save_button.setText(_translate("Dialog", "Сохранить"))

    def return_product(self):
        tab_name = 'Current_product'
        if self.row_data[1] in ['Продажа товара', 'Списание товара']:
            added_row_ids = self.support_instance.delete()

            for added_row_id in added_row_ids:
                for item_data in self.initial_result_data:
                    if item_data[0] == int(added_row_id):
                        product_id = item_data[1]
                        quantity = item_data[3]

                        update_query = f"UPDATE Current_product SET quantity = quantity + ? WHERE id = ?"
                        self.cursor.execute(update_query, (quantity, product_id))

        elif self.row_data[1] == 'Принятие товара':
            deleted_row_ids = self.support_instance.delete()

            for deleted_row_id in deleted_row_ids:
                for item_data in self.initial_result_data:
                    if item_data[0] == int(deleted_row_id):
                        product_id = item_data[1]
                        delete_query = f"DELETE FROM {tab_name} WHERE id = ?"
                        self.cursor.execute(delete_query, (product_id, ))

        elif self.row_data[1] == 'Перемещение товара на другой склад':
            updated_row_ids = self.support_instance.delete()

            for updated_row_id in updated_row_ids:
                for item_data in self.initial_result_data:
                    if item_data[0] == int(updated_row_id):
                        new_warehouse_id = item_data[2]
                        update_query = f"UPDATE {tab_name} SET warehouse_id = ? WHERE id = ?"
                        self.cursor.execute(update_query, (new_warehouse_id, updated_row_id))

        self.enable_buttons()

    def print_row_data(self):
        client = self.row_data[2] if self.row_data[2] is not None else ''
        additional_info = self.row_data[5] if self.row_data[5] is not None else ''

        self.data_edit.setPlainText(f"Тип проведенной операции: {self.row_data[1]}\n"
                                    f"Клиент, который запросил операцию: {client}\n"
                                    f"Сотрудник, который произвел операцию: {self.row_data[3]}\n"
                                    f"Время, в которое провели операцию: {self.row_data[4]}\n"
                                    f"Дополнительные характеристики операции: {additional_info}\n")

    def button_action(self, action_type):
        if action_type == "delete":
            self.support_instance.delete()
            self.enable_buttons()
        elif action_type == "save":
            self.support_instance.save()
            self.disable_buttons()
        elif action_type == "cancel":
            self.support_instance.cancel()
            self.disable_buttons()

    def disable_buttons(self):
        self.cancel_button.setEnabled(False)
        self.save_button.setEnabled(False)

    def enable_buttons(self):
        self.cancel_button.setEnabled(True)
        self.save_button.setEnabled(True)


if __name__ == "__main__":
    import sys
    curs = None
    data_row = None
    app = QtWidgets.QApplication(sys.argv)
    ui = UiOperationTableWindow(curs, data_row)
    ui.show()
    sys.exit(app.exec_())
