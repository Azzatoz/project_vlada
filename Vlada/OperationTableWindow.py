from PyQt5 import QtCore, QtWidgets


class UiOperationTableWindow(QtWidgets.QDialog):
    def __init__(self, cursor):
        super(UiOperationTableWindow, self).__init__()

        self.cursor = cursor

        self.setObjectName("Dialog")
        self.resize(1200, 800)
        self.data_edit = QtWidgets.QTextEdit(self)
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
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(90, 360, 1021, 371))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.delete_btn = QtWidgets.QPushButton(self)
        self.delete_btn.setGeometry(QtCore.QRect(1020, 320, 93, 28))
        self.delete_btn.setObjectName("delete_btn")
        self.add_btn = QtWidgets.QPushButton(self)
        self.add_btn.setGeometry(QtCore.QRect(910, 320, 93, 28))
        self.add_btn.setObjectName("add_btn")
        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setGeometry(QtCore.QRect(1020, 740, 93, 28))
        self.cancel_button.setObjectName("cancel_button")
        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setGeometry(QtCore.QRect(910, 740, 93, 28))
        self.save_button.setObjectName("save_button")

        self.re_translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.open_word_btn.setText(_translate("Dialog", "Открыть word-документ"))
        self.open_excel_btn.setText(_translate("Dialog", "Открыть excel-документ"))
        self.delete_btn.setText(_translate("Dialog", "Удалить"))
        self.add_btn.setText(_translate("Dialog", "Добавить"))
        self.cancel_button.setText(_translate("Dialog", "Отмена"))
        self.save_button.setText(_translate("Dialog", "Сохранить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UiOperationTableWindow()
    ui.show()
    sys.exit(app.exec_())
