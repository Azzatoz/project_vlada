from PyQt5 import QtCore, QtWidgets
from support_file import SupportClass


class UiStandardDataWindow(QtWidgets.QDialog):
    def __init__(self, table_name, connection):
        super(UiStandardDataWindow, self).__init__()

        self.table_name = table_name
        self.connection = connection

        self.setObjectName("Dialog")
        self.resize(1200, 800)
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(130, 120, 941, 461))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.search_edit = QtWidgets.QLineEdit(self)
        self.search_edit.setGeometry(QtCore.QRect(130, 90, 551, 21))
        self.search_edit.setObjectName("search_edit")
        self.search_edit.setPlaceholderText("Искать:")
        self.add_btn = QtWidgets.QPushButton(self)
        self.add_btn.setGeometry(QtCore.QRect(850, 70, 101, 41))
        self.add_btn.setObjectName("add_btn")
        self.delete_btn = QtWidgets.QPushButton(self)
        self.delete_btn.setGeometry(QtCore.QRect(970, 70, 101, 41))
        self.delete_btn.setObjectName("delete_btn")
        self.output_edit = QtWidgets.QTextEdit(self)
        self.output_edit.setGeometry(QtCore.QRect(130, 590, 551, 141))
        self.output_edit.setObjectName("output_edit")
        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setGeometry(QtCore.QRect(850, 590, 101, 41))
        self.save_button.setObjectName("save_button")
        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setGeometry(QtCore.QRect(970, 590, 101, 41))
        self.cancel_button.setObjectName("cancel_button")

        self.disable_buttons()
        self.support_instance = SupportClass(self.table_name, self.connection, self.table_widget)
        self.support_instance.display_table_data()
        self.search_edit.textChanged.connect(lambda text: self.support_instance.search_table(text))
        self.table_widget.horizontalHeader().sectionClicked.connect(
            lambda clicked_column: self.support_instance.sort_data_by_column(clicked_column))
        self.add_btn.clicked.connect(lambda: self.button_action("add"))
        self.delete_btn.clicked.connect(lambda: self.button_action("delete"))
        self.save_button.clicked.connect(lambda: self.button_action("save"))
        self.cancel_button.clicked.connect(lambda: self.button_action("cancel"))

        self.re_translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add_btn.setText(_translate("Dialog", "Добавить"))
        self.delete_btn.setText(_translate("Dialog", "Удалить"))
        self.save_button.setText(_translate("Dialog", "Сохранить"))
        self.cancel_button.setText(_translate("Dialog", "Отмена"))

    # TODO: Нужно перенести в support_file.py
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
        elif action_type == "add":
            self.support_instance.add()
            self.enable_buttons()

    def disable_buttons(self):
        self.cancel_button.setEnabled(False)
        self.save_button.setEnabled(False)

    def enable_buttons(self):
        self.cancel_button.setEnabled(True)
        self.save_button.setEnabled(True)


if __name__ == "__main__":
    import sys
    tab_name = None
    conn = None
    app = QtWidgets.QApplication(sys.argv)
    ui = UiStandardDataWindow(tab_name, conn)
    ui.show()
    sys.exit(app.exec_())
