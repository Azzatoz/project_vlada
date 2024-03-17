from PyQt5 import QtWidgets
from Vlada.db import create_database, generate_data
from Dima.AutorizationWindow import Ui_AuthorizationWindow

# Создание базы данных
create_database()

# Генерация данных
generate_data()

# Запуск приложения
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AutorizationDialog = QtWidgets.QDialog()
    ui_autorization_dialog = Ui_AuthorizationWindow(AutorizationDialog)
    ui_autorization_dialog.show()
    sys.exit(app.exec_())
