import mysql.connector
from PyQt5 import QtCore, QtWidgets
from Vlada.MainWindow import UiMainWindow
from Vlada.db import create_database
from support_file import show_notification


class Ui_AuthorizationWindow(object):

    # Конструктор класса
    def __init__(self, authorization_dialog, conn):

        # Создание окна приложения
        self.authorization_dialog = authorization_dialog
        self.authorization_dialog.setObjectName("AuthorizationWindow")
        self.authorization_dialog.resize(1620, 960)

        # Создание вертикального макета
        self.verticalLayoutWidget = QtWidgets.QWidget(self.authorization_dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(620, 255, 400, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Создание элементов управления
        self.Name_of_project = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Name_of_project.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Name_of_project.setAutoFillBackground(False)
        self.Name_of_project.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.Name_of_project.setObjectName("Name_of_project")
        self.verticalLayout.addWidget(self.Name_of_project)

        spacerItem = QtWidgets.QSpacerItem(20, 500, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_1.setObjectName("label_1")
        self.label_1.setVisible(False)
        self.verticalLayout.addWidget(self.label_1)
        self.FirstName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.FirstName.setObjectName("FirstName")
        self.FirstName.setVisible(False)
        self.verticalLayout.addWidget(self.FirstName)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setVisible(False)
        self.verticalLayout.addWidget(self.label_2)
        self.LastName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.LastName.setObjectName("LastName")
        self.LastName.setVisible(False)
        self.verticalLayout.addWidget(self.LastName)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setVisible(False)
        self.verticalLayout.addWidget(self.label_3)
        self.MiddleName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.MiddleName.setObjectName("MiddleName")
        self.MiddleName.setVisible(False)
        self.verticalLayout.addWidget(self.MiddleName)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setVisible(False)
        self.verticalLayout.addWidget(self.label_4)
        self.Phone = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.Phone.setObjectName("Phone")
        self.Phone.setVisible(False)
        self.verticalLayout.addWidget(self.Phone)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setVisible(False)
        self.verticalLayout.addWidget(self.label_5)
        self.BirthDate = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.BirthDate.setObjectName("BirthDate")
        self.BirthDate.setVisible(False)
        self.verticalLayout.addWidget(self.BirthDate)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.Username = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.Username.setObjectName("Username")
        self.verticalLayout.addWidget(self.Username)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.Password = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.Password.setObjectName("Password")
        self.verticalLayout.addWidget(self.Password)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LogIn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.LogIn.setObjectName("LogIn")
        self.LogIn.clicked.connect(self.login)
        self.horizontalLayout.addWidget(self.LogIn)
        self.LogUp = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.LogUp.setObjectName("LogUp")
        self.LogUp.clicked.connect(self.register)
        self.horizontalLayout.addWidget(self.LogUp)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(self.authorization_dialog)
        QtCore.QMetaObject.connectSlotsByName(self.authorization_dialog)

        # Подключение к базе данных
        self.conn = conn
        self.cursor = conn.cursor()

    def retranslateUi(self, authorization_dialog):
        _translate = QtCore.QCoreApplication.translate
        authorization_dialog.setWindowTitle(_translate("authorizationWindow", "Авторизация"))
        self.Name_of_project.setText(_translate("authorizationWindow", "Название"))
        self.label_1.setText(_translate("authorizationWindow", "Имя"))
        self.label_2.setText(_translate("authorizationWindow", "Фамилия"))
        self.label_3.setText(_translate("authorizationWindow", "Отчество"))
        self.label_4.setText(_translate("authorizationWindow", "Телефон"))
        self.label_5.setText(_translate("authorizationWindow", "Дата рождения"))
        self.label_7.setText(_translate("authorizationWindow", "Логин"))
        self.label_8.setText(_translate("authorizationWindow", "Пароль"))
        self.LogIn.setText(_translate("authorizationWindow", "Войти"))
        self.LogUp.setText(_translate("authorizationWindow", "Зарегистрироваться"))

    def show(self):
        self.authorization_dialog.show()

    def login(self):
        username = self.Username.text()
        password = self.Password.text()
        try:
            # Выполнение SQL-запроса для поиска пользователя в базе данных
            query = 'SELECT * FROM Worker WHERE username = %s AND password = %s'
            self.cursor.execute(query, (username, password))

            # Получение результата запроса
            result = self.cursor.fetchone()

            if result:
                # Создание экземпляра QMainWindow
                main_window = UiMainWindow(result[1], self.conn)
                # Показ основного окна
                main_window.show()
                # Закрытие окна авторизации
                self.authorization_dialog.accept()
            else:
                show_notification("Неверное имя пользователя или пароль")

        except mysql.connector.Error as e:
            # Обработка ошибок подключения или выполнения SQL-запроса
            print("Ошибка при выполнении запроса:", e)

        finally:
            # Закрытие соединения с базой данных
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()

    def register(self):
        if self.LogUp.text() == "Зарегистрироваться":
            # Изменение интерфейса для регистрации
            self.LogIn.setText("Подтвердить")
            self.LogIn.clicked.disconnect(self.login)
            self.LogIn.clicked.connect(self.confirm_registration)
            self.LogUp.setText("Отмена")

            # Показать элементы интерфейса при регистрации
            self.label_1.setVisible(True)
            self.FirstName.setVisible(True)
            self.label_2.setVisible(True)
            self.LastName.setVisible(True)
            self.label_3.setVisible(True)
            self.MiddleName.setVisible(True)
            self.label_4.setVisible(True)
            self.Phone.setVisible(True)
            self.label_5.setVisible(True)
            self.BirthDate.setVisible(True)

        else:
            # Возврат к обычному режиму входа
            self.LogIn.setText("Войти")
            self.LogIn.clicked.disconnect(self.confirm_registration)
            self.LogIn.clicked.connect(self.login)
            self.LogUp.setText("Зарегистрироваться")

            # Скрыть элементы интерфейса при отмене регистрации
            self.label_1.setVisible(False)
            self.FirstName.setVisible(False)
            self.label_2.setVisible(False)
            self.LastName.setVisible(False)
            self.label_3.setVisible(False)
            self.MiddleName.setVisible(False)
            self.label_4.setVisible(False)
            self.Phone.setVisible(False)
            self.label_5.setVisible(False)
            self.BirthDate.setVisible(False)

    def confirm_registration(self):
        firstname = self.FirstName.text()
        lastname = self.LastName.text()
        middlename = self.MiddleName.text()
        phone = self.Phone.text()
        birthdate = self.BirthDate.date().toString("yyyy-MM-dd")
        username = self.Username.text()
        password = self.Password.text()

        try:
            # Проверка на пустые поля
            if not firstname or not lastname or not phone or not birthdate or not username or not password:
                show_notification("Заполните все поля")
                return

            # Проверка на уникальность логина
            self.cursor.execute("SELECT * FROM Worker WHERE username = %s", (username,))
            existing_user = self.cursor.fetchone()
            if existing_user:
                show_notification("Пользователь с таким логином уже существует")
                return

            # Получение ID должности "Новый пользователь"
            self.cursor.execute("SELECT id FROM Position WHERE name_position = 'Новый пользователь'")
            position_id = cursor.fetchone()[0]

            # Вставка данных нового пользователя в таблицу Worker
            self.cursor.execute(
                "INSERT INTO Worker (name, phone_number, birthday, username, password, position_id)"
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (f"{firstname} {lastname} {middlename}", phone, birthdate, username, password, position_id))

            # Создание нового пользователя MySQL
            create_user_query = f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'"
            self.cursor.execute(create_user_query)

            # Назначение привилегий новому пользователю
            grant_privileges_query = f"GRANT ALL PRIVILEGES ON your_database_name.* TO '{username}'@'localhost'"
            self.cursor.execute(grant_privileges_query)

            # Подтверждение изменений
            self.conn.commit()

            # Закрытие соединения с базой данных
            self.cursor.close()
            self.conn.close()

            show_notification("Регистрация завершена")

            # Возврат к обычному режиму входа
            self.label_1.setVisible(False)
            self.FirstName.setVisible(False)
            self.label_2.setVisible(False)
            self.LastName.setVisible(False)
            self.label_3.setVisible(False)
            self.MiddleName.setVisible(False)
            self.label_4.setVisible(False)
            self.Phone.setVisible(False)
            self.label_5.setVisible(False)
            self.BirthDate.setVisible(False)
            self.LogIn.setText("Войти")
            self.LogIn.clicked.disconnect(self.confirm_registration)
            self.LogIn.clicked.connect(self.login)
            self.LogUp.setText("Зарегистрироваться")

        except mysql.connector.Error as e:
            # Обработка ошибок подключения или выполнения SQL-запросов
            print("Ошибка при выполнении запроса:", e)

        finally:
            # Закрытие соединения с базой данных
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
