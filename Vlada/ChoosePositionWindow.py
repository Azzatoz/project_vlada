from PyQt5 import QtCore, QtWidgets
from support_file import SupportClass


class UiChoosePositionWindow(QtWidgets.QDialog):
    def __init__(self, connection):
        super(UiChoosePositionWindow, self).__init__()

        self.connection = connection
        self.table_name = 'Position'
        self.name_position = []
        self.initial_db_data = []
        self.change_db_data = []

        self.setObjectName("Dialog")
        self.resize(1200, 800)
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(90, 150, 1011, 571))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.search_edit = QtWidgets.QLineEdit(self)
        self.search_edit.setGeometry(QtCore.QRect(90, 120, 551, 22))
        self.search_edit.setObjectName("search_edit")
        self.search_edit.setPlaceholderText("Искать:")

        self.support_instance = SupportClass(self.table_name, self.connection, self.table_widget)
        self.initial_db_data, self.change_db_data, count_columns, headers = (
            self.support_instance.display_table_data())
        self.search_edit.textChanged.connect(lambda text: self.support_instance.search_table(text))
        self.table_widget.horizontalHeader().sectionClicked.connect(
            lambda clicked_column: self.support_instance.sort_data_by_column(clicked_column))
        self.table_widget.cellDoubleClicked.connect(self.cell_double_clicked)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))

        QtCore.QMetaObject.connectSlotsByName(self)

    def cell_double_clicked(self, row):
        item = self.table_widget.item(row - 1, 0)
        item_text = item.text()
        self.name_position.append(self.change_db_data[int(item_text)][1])
        self.name_position.append(self.change_db_data[int(item_text)][0])
        self.close()

    def exec_(self):
        super(UiChoosePositionWindow, self).exec_()
        return self.name_position


if __name__ == "__main__":
    import sys
    con = None
    app = QtWidgets.QApplication(sys.argv)
    ui = UiChoosePositionWindow(con)
    ui.show()
    sys.exit(app.exec_())
