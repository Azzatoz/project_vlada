import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OperationWindow(object):
    def __init__(self, operation):

        self.operation = operation
        self.original_data = {}

        # Подключение к базе данных
        self.conn = sqlite3.connect('warehouse.db')
        self.c = self.conn.cursor()

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

    def retranslateUi(self, OperationWindow):
        _translate = QtCore.QCoreApplication.translate
        OperationWindow.setWindowTitle(_translate("OperationWindow", "OperationWindow"))
        self.choose_button.setText(_translate("OperationWindow", operation))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.confirm_button.setText(_translate("OperationWindow", "Выполнить"))
        self.cancel_button.setText(_translate("OperationWindow", "Отмена"))

    def show(self):
        self.operationWindow.show()

    def set_info(self, operation):
        if operation == "списать":
            self.choose_button.setText("Списать")
        elif operation == "продать":
            self.choose_button.setText("продать...")
            # выбор клиента, если клиента нет - добавить
        elif operation == "переместить":
            # выбор склада куда переместить товар
            self.choose_button.setText("Выбрать товар для перемещения")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_OperationWindow("Current_product")  # тест
    ui.show()
    sys.exit(app.exec_())
