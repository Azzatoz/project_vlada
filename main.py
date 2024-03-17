from PyQt5 import QtWidgets
from my.vlada.db import create_database, generate_data
from my.AutorizationWindow import Ui_AuthorizationWindow

# Создание базы данных
create_database()

# Генерация данных
generate_data()

# Запуск приложения
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    authorization_window = Ui_AuthorizationWindow()
    authorization_window.show()
    sys.exit(app.exec_())
