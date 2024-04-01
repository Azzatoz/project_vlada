import mysql.connector


def create_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345'
        )

        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS warehouse")
        cursor.execute("USE warehouse")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Client (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(70) NOT NULL,
                phone_number BIGINT NOT NULL,
                json_note VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Positions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name_position VARCHAR(30) NOT NULL,
                salary INT NOT NULL,
                access_level INT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Worker (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(70) NOT NULL,
                birthday DATE NOT NULL,
                phone_number BIGINT NOT NULL,
                position_id INT NOT NULL,
                username VARCHAR(30) NOT NULL,
                password VARCHAR(30) NOT NULL,
                FOREIGN KEY(position_id) REFERENCES Positions(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Operation (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(60) NOT NULL,
                client_id INT,
                worker_id INT NOT NULL,
                time DATE NOT NULL,
                additional_characteristics VARCHAR(255),
                FOREIGN KEY(client_id) REFERENCES Client(id),
                FOREIGN KEY(worker_id) REFERENCES Worker(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Warehouse (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                address VARCHAR(50) NOT NULL,
                coordinates FLOAT NOT NULL,
                geolocation VARCHAR(50) NOT NULL,
                json_product VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Current_product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                current_product_id INT NOT NULL,
                quantity INT NOT NULL,
                delivery_id INT NOT NULL,
                warehouse_id INT NOT NULL,
                delivery_date DATE NOT NULL,
                expiration_date_operation DATE,
                destination VARCHAR(30),
                FOREIGN KEY(delivery_id) REFERENCES Operation(id),
                FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Product_property (
                id INT AUTO_INCREMENT PRIMARY KEY,
                current_product_name VARCHAR(30) NOT NULL,
                category VARCHAR(30) NOT NULL,
                characteristics VARCHAR(255) NOT NULL,
                expiration_date DATE,
                price INT NOT NULL,
                article_number INT NOT NULL,
                photo LONGBLOB,
                FOREIGN KEY(id) REFERENCES Current_product(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Operation_product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                operation_id INT NOT NULL,
                product_id INT NOT NULL,
                warehouse_id INT NOT NULL,
                quantity INT NOT NULL,
                condition_type VARCHAR(30) NOT NULL,
                FOREIGN KEY(operation_id) REFERENCES Operation(id),
                FOREIGN KEY(product_id) REFERENCES Product_property(id)
            )
        """)

        cursor.close()
        conn.close()
    except Exception as e:
        print("Ошибка при создании базы данных:", e)


def generate_data():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='warehouse'
        )

        cursor = conn.cursor()

        tables_data = {
            'Positions': [
                ('Директор', 50000, 5),
                ('Менеджер', 50000, 4),
                ('Кладовщик', 50000, 3),
                ('Кассир', 50000, 2),
                ('Новый пользователь', 0, 1)
            ],
            'Warehouse': [
                ('Склад 1', 'г.Минск, ул.Богдановича, дом 71', 37.7749, '37.7749', 'Товар 1, товар 2'),
                ('Склад 2', 'г.Минск, ул.Богдановича, дом 72', 37.7749, '37.7749', 'Товар 3, товар 4'),
                ('Склад 3', 'г.Минск, ул.Богдановича, дом 73', 37.7749, '37.7749', 'Товар 5, товар 6')
            ],
            'Client': [
                ('Клиент 1', 1234567890, 'Любит гулять'),
                ('Клиент 2', 1256787890, 'Любит играть'),
                ('Клиент 3', 4567567890, 'Не любит играть'),
                ('Клиент 4', 9876543210, 'Не любит гулять')
            ],
            'Worker': [
                ('Иван Иванов', '2000-01-01', 1233467890, 1, 'admin1', 'Password123@'),
                ('Коля Черничка', '2000-05-02', 1234457890, 2, 'admin2', 'Password123@'),
                ('Вася Васильков', '2005-04-01', 1223467890, 3, 'admin3', 'Password123@'),
                ('Илья Котиков', '2003-02-01', 1298567890, 4, 'admin4', 'Password123@')
            ],
            'Operation': [
                ('Перемещение товара на другой склад', None, 1, '2024-03-17', 'Доп характеристики'),
                ('Продажа товара', 2, 1, '2024-03-18', None),
                ('Принятие товара', None, 2, '2024-03-19', 'Доп характеристики'),
                ('Списание товара', None, 3, '2024-03-20', None)
            ],
            'Current_product': [
                (1, 10, 1, 1, '2024-03-01', '2024-03-17', None),
                (2, 10, 1, 1, '2024-03-02', '2024-03-17', None),
                (3, 10, 1, 1, '2024-03-03', '2024-03-17', None),
                (4, 15, 2, 2, '2024-03-04', '2024-03-17', None),
                (5, 0, 2, 2, '2024-03-05', '2024-03-17', None),
                (6, 15, 2, 2, '2024-03-06', '2024-03-17', None),
                (7, 20, 3, 3, '2024-03-07', '2024-03-17', None),
                (8, 20, 3, 3, '2024-03-08', '2024-03-17', None),
                (9, 20, 3, 3, '2024-03-09', '2024-03-17', None),
                (10, 25, 4, 3, '2024-03-10', '2024-03-17', None),
                (11, 20, 4, 1, '2024-03-11', '2024-03-17', None),
                (12, 0, 4, 2, '2024-03-12', '2024-03-17', None),
                (13, 10, 1, 2, '2024-03-01', '2024-03-17', None),
                (14, 5, 1, 2, '2024-03-02', '2024-03-17', None),
                (15, 0, 1, 2, '2024-03-03', '2024-03-17', None)
            ],
            'Product_property': [
                ('Товар 1', 'Категория 1', 'Характеристики', '2024-03-13', 100, 12340, None),
                ('Товар 2', 'Категория 1', 'Характеристики', '2024-03-12', 100, 12341, None),
                ('Товар 3', 'Категория 2', 'Характеристики', '2024-03-11', 200, 12342, None),
                ('Товар 4', 'Категория 2', 'Характеристики', '2024-03-17', 100, 12343, None),
                ('Товар 5', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12344, None),
                ('Товар 6', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12345, None),
                ('Товар 7', 'Категория 2', 'Характеристики', '2024-03-17', 100, 12346, None),
                ('Товар 8', 'Категория 2', 'Характеристики', '2024-03-17', 100, 12347, None),
                ('Товар 9', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12348, None),
                ('Товар 10', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12349, None),
                ('Товар 11', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12310, None),
                ('Товар 12', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12311, None),
                ('Товар 1', 'Категория 1', 'Характеристики', '2024-03-13', 100, 12340, None),
                ('Товар 2', 'Категория 1', 'Характеристики', '2024-03-12', 100, 12341, None),
                ('Товар 3', 'Категория 2', 'Характеристики', '2024-03-11', 100, 12342, None)
            ],
            'Operation_product': [
                (1, 1, 2, 10, 'Доставлен'),
                (1, 2, 2, 10, 'Доставлен'),
                (1, 3, 2, 10, 'Доставлен'),
                (2, 4, 2, 11, 'На складе'),
                (2, 5, 2, 12, 'На складе'),
                (2, 6, 2, 12, 'На складе'),
                (3, 7, 3, 13, 'На складе'),
                (3, 8, 3, 13, 'На складе'),
                (3, 9, 3, 13, 'На складе'),
                (4, 10, 3, 14, 'Доставлен'),
                (4, 11, 1, 14, 'Доставлен'),
                (4, 12, 2, 14, 'Доставлен'),
                (3, 13, 2, 20, 'Доставлен'),
                (3, 14, 2, 15, 'Доставлен'),
                (3, 15, 2, 10, 'Доставлен')
            ]
        }

        for table, data in tables_data.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]

            if count == 0:
                query_columns = f"SHOW COLUMNS FROM {table}"
                cursor.execute(query_columns)
                columns = ', '.join([column[0] for column in cursor.fetchall() if column[0] != 'id'])

                placeholders = ', '.join(['%s' for _ in range(len(data[0]))])
                query_insert = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

                cursor.executemany(query_insert, data)

    finally:
        conn.commit()
        conn.close()
