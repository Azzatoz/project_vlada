from functools import partial
from Dima.OperationWindow import Ui_OperationWindow
from support_file import SupportClass
from PyQt5 import QtCore, QtWidgets
import sqlite3

path = 'warehouse.db'


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()

        self.table_name = 'Operation'
        self.db_data = []
        self.count_columns = None

        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        self.setObjectName("MainWindow")
        self.resize(1200, 800)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.log_out_btn = QtWidgets.QPushButton(self.central_widget)
        self.log_out_btn.setGeometry(QtCore.QRect(850, 700, 251, 41))
        self.log_out_btn.setObjectName("log_out_btn")
        self.open_document_btn = QtWidgets.QPushButton(self.central_widget)
        self.open_document_btn.setGeometry(QtCore.QRect(980, 620, 121, 71))
        self.open_document_btn.setObjectName("open_document_btn")
        self.table_widget = QtWidgets.QTableWidget(self.central_widget)
        self.table_widget.setGeometry(QtCore.QRect(110, 150, 991, 461))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.search_edit = QtWidgets.QLineEdit(self.central_widget)
        self.search_edit.setGeometry(QtCore.QRect(110, 111, 391, 31))
        self.search_edit.setObjectName("search_edit")
        self.search_edit.setPlaceholderText("Искать:")
        self.open_client_btn = QtWidgets.QPushButton(self.central_widget)
        self.open_client_btn.setGeometry(QtCore.QRect(650, 100, 111, 41))
        self.open_client_btn.setObjectName("open_client_btn")
        self.write_off_product_btn = QtWidgets.QPushButton(self.central_widget)
        self.write_off_product_btn.setGeometry(QtCore.QRect(110, 50, 91, 51))
        self.write_off_product_btn.setObjectName("write_off_product_btn")
        self.accept_product_btn = QtWidgets.QPushButton(self.central_widget)
        self.accept_product_btn.setGeometry(QtCore.QRect(410, 50, 91, 51))
        self.accept_product_btn.setObjectName("accept_product_btn")
        self.move_product_btn = QtWidgets.QPushButton(self.central_widget)
        self.move_product_btn.setGeometry(QtCore.QRect(310, 50, 91, 51))
        self.move_product_btn.setObjectName("move_product_btn")
        self.sell_product_btn = QtWidgets.QPushButton(self.central_widget)
        self.sell_product_btn.setGeometry(QtCore.QRect(210, 50, 91, 51))
        self.sell_product_btn.setObjectName("sell_product_btn")
        self.delete_row_btn = QtWidgets.QPushButton(self.central_widget)
        self.delete_row_btn.setGeometry(QtCore.QRect(910, 100, 93, 41))
        self.delete_row_btn.setObjectName("delete_row_btn")
        self.open_worker_btn = QtWidgets.QPushButton(self.central_widget)
        self.open_worker_btn.setGeometry(QtCore.QRect(780, 100, 111, 41))
        self.open_worker_btn.setObjectName("open_worker_btn")
        self.output_edit = QtWidgets.QTextEdit(self.central_widget)
        self.output_edit.setGeometry(QtCore.QRect(110, 620, 731, 121))
        self.output_edit.setObjectName("output_edit")
        self.filter_box = QtWidgets.QComboBox(self.central_widget)
        self.filter_box.setGeometry(QtCore.QRect(110, 10, 391, 28))
        self.filter_box.setObjectName("filter_box")
        self.filter_box.addItem("Все товары")
        self.filter_box.addItem("Списанные товары")
        self.filter_box.addItem("Перемещенные товары")
        self.filter_box.addItem("Проданные товары")
        self.filter_box.addItem("Принятые товары")
        self.open_statistic_btn = QtWidgets.QPushButton(self.central_widget)
        self.open_statistic_btn.setGeometry(QtCore.QRect(850, 620, 121, 71))
        self.open_statistic_btn.setObjectName("open_statistic_btn")
        self.open_warehouse_btn = QtWidgets.QPushButton(self.central_widget)
        self.open_warehouse_btn.setGeometry(QtCore.QRect(520, 100, 111, 41))
        self.open_warehouse_btn.setObjectName("open_warehouse_btn")
        self.cancel_button = QtWidgets.QPushButton(self.central_widget)
        self.cancel_button.setGeometry(QtCore.QRect(1010, 100, 93, 41))
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setEnabled(False)
        self.setCentralWidget(self.central_widget)

        self.support_instance = SupportClass(self.table_name, self.connection, self.table_widget)
        self.db_data, self.count_columns = self.support_instance.display_table_data()
        self.search_edit.textChanged.connect(lambda text: self.support_instance.search_table(text))
        self.table_widget.horizontalHeader().sectionClicked.connect(
            lambda clicked_column: self.support_instance.sort_data_by_column(clicked_column))
        self.filter_box.currentIndexChanged.connect(self.filter_row)
        self.log_out_btn.clicked.connect(self.log_out)
        self.cancel_button.clicked.connect(self.cancel_deletion_row)
        self.delete_row_btn.clicked.connect(self.delete_and_enable_cancel_button)

        self.re_translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.log_out_btn.setText(_translate("MainWindow", "Выйти из системы"))
        self.open_document_btn.setText(_translate("MainWindow", "Документы"))
        self.open_client_btn.setText(_translate("MainWindow", "Клиенты"))
        self.write_off_product_btn.setText(_translate("MainWindow", "Списать"))
        self.accept_product_btn.setText(_translate("MainWindow", "Принять"))
        self.move_product_btn.setText(_translate("MainWindow", "Переместить"))
        self.sell_product_btn.setText(_translate("MainWindow", "Продать"))
        self.delete_row_btn.setText(_translate("MainWindow", "Удалить"))
        self.open_worker_btn.setText(_translate("MainWindow", "Сотрудники"))
        self.open_statistic_btn.setText(_translate("MainWindow", "Статистика"))
        self.open_warehouse_btn.setText(_translate("MainWindow", "Склады"))
        self.cancel_button.setText(_translate("MainWindow", "Отмена"))

        self.write_off_product_btn.clicked.connect(partial(self.operation_window, 'Списать'))
        self.move_product_btn.clicked.connect(partial(self.operation_window, 'Переместить'))
        self.sell_product_btn.clicked.connect(partial(self.operation_window, 'Продать'))
        self.accept_product_btn.clicked.connect(partial(self.operation_window, 'Принять'))

    def operation_window(self, operation):
        operation_window = Ui_OperationWindow(operation, self.cursor)
        operation_window.show()
        UiMainWindow.operation_window_instance = operation_window

    def filter_row(self):
        selected_filter = self.filter_box.currentText()

        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 1)
            text = item.text()
            if selected_filter == "Проданные товары" and text == "Продажа товара":
                self.table_widget.setRowHidden(row, False)
            elif selected_filter == "Списанные товары" and text == "Списание товара":
                self.table_widget.setRowHidden(row, False)
            elif selected_filter == "Перемещенные товары" and text == "Перемещение товара на другой склад":
                self.table_widget.setRowHidden(row, False)
            elif selected_filter == "Принятые товары" and text == "Принятие товара":
                self.table_widget.setRowHidden(row, False)
            elif selected_filter == "Все товары":
                self.table_widget.setRowHidden(row, False)
            else:
                self.table_widget.setRowHidden(row, True)

    def log_out(self):
        from Dima.AutorizationWindow import Ui_AuthorizationWindow
        self.close()
        authorization_dialog = QtWidgets.QDialog()
        auth_window = Ui_AuthorizationWindow(authorization_dialog)
        auth_window.show()
        UiMainWindow.auth_window_instance = auth_window

    def cancel_deletion_row(self):
        db_row_ids = [row[0] for row in self.db_data]

        current_row_ids = []
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 0)
            current_row_ids.append(int(item.text()))

        deleted_row_ids = set(db_row_ids) - set(current_row_ids)

        for deleted_row_id in deleted_row_ids:
            deleted_rows_data = next(deleted_row_data for deleted_row_data in self.db_data
                                     if deleted_row_data[0] == deleted_row_id)
            self.cursor.execute(f"INSERT INTO {self.table_name} VALUES "
                                f"({','.join(['?'] * self.count_columns)})", deleted_rows_data)

        self.connection.commit()
        self.support_instance.display_table_data()
        self.cancel_button.setEnabled(False)

    def delete_and_enable_cancel_button(self):
        self.support_instance.delete()
        self.support_instance.save()
        self.cancel_button.setEnabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UiMainWindow()
    ui.show()
    sys.exit(app.exec_())
