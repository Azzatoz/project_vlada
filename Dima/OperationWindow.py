import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OperationWindow(object):

    def __init__(self, table_name):
        self.operationWindow = QtWidgets.QDialog()
        self.operationWindow.setObjectName("OperationWindow")
        self.operationWindow.resize(1620, 960)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.operationWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(100, 60, 1400, 860))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.choose_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.choose_button.setEnabled(False)
        self.choose_button.setObjectName("choose_button")
        self.horizontalLayout_2.addWidget(self.choose_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(5)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.confirm_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.confirm_button.setEnabled(True)
        self.confirm_button.setMouseTracking(False)
        self.confirm_button.setCheckable(False)
        self.confirm_button.setObjectName("confirm_button")
        self.horizontalLayout.addWidget(self.confirm_button)
        self.cancel_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(self.operationWindow)
        QtCore.QMetaObject.connectSlotsByName(self.operationWindow)
        self.table_name = table_name

        # Подключение к базе данных
        self.conn = sqlite3.connect('warehouse.db')
        self.c = self.conn.cursor()

    def retranslateUi(self, OperationWindow):
        _translate = QtCore.QCoreApplication.translate
        OperationWindow.setWindowTitle(_translate("OperationWindow", "OperationWindow"))
        self.choose_button.setText(_translate("OperationWindow", "Выбрать склад / клиента"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.confirm_button.setText(_translate("OperationWindow", "Выполнить"))
        self.cancel_button.setText(_translate("OperationWindow", "Отмена"))

    def show(self):
        self.operationWindow.show()

    def operation_window(self, operation_type):
        if operation_type == "списать":
            ui_table = Ui_OperationWindow("таблица_для_списания")
        elif operation_type == "продать":
            ui_table = Ui_OperationWindow("таблица_для_продажи")
        elif operation_type == "переместить":
            ui_table = Ui_OperationWindow("таблица_для_перемещения")

        ui_table.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_OperationWindow("Current_product")
    ui.show()
    sys.exit(app.exec_())
