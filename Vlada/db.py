import sqlite3 as sl


def create_database():
    try:
        con = sl.connect('warehouse.db')

        with con:
            con.execute("""
                    CREATE TABLE IF NOT EXISTS Client (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(70) NOT NULL,
                        phone_number INT NOT NULL,
                        json_note VARCHAR(255)
                    );
                """)

            con.execute("""
                CREATE TABLE IF NOT EXISTS Position (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_position VARCHAR(30) NOT NULL,
                    salary INT NOT NULL,
                    access_level INT NOT NULL
                );
            """)

            con.execute("""
                CREATE TABLE IF NOT EXISTS Worker (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(70) NOT NULL,
                    birthday INT NOT NULL,
                    phone_number INT NOT NULL,
                    position_id INT NOT NULL,
                    username VARCHAR(30) NOT NULL,
                    password VARCHAR(30) NOT NULL,
                    FOREIGN KEY(position_id) REFERENCES Position(id)
                );
            """)

            con.execute("""
                CREATE TABLE IF NOT EXISTS Operation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type VARCHAR(60) NOT NULL,
                    client_id INT,
                    worker_id INT NOT NULL,
                    time INT NOT NULL,
                    additional_characteristics VARCHAR(255),
                    FOREIGN KEY(client_id) REFERENCES Client(id),
                    FOREIGN KEY(worker_id) REFERENCES Worker(id)
                );
            """)

            con.execute("""
                CREATE TABLE IF NOT EXISTS Warehouse (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(30) NOT NULL,
                    address VARCHAR(50) NOT NULL,
                    coordinates INT NOT NULL,
                    geolocation VARCHAR(50) NOT NULL,
                    json_product VARCHAR(255)
                );
            """)

            con.execute("""
                CREATE TABLE IF NOT EXISTS Current_product (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quantity INT NOT NULL,
                    delivery_id NOT NULL,
                    warehouse_id INT NOT NULL,
                    delivery_date INT NOT NULL,
                    expiration_date_operation INT,
                    destination VARCHAR(30),
                    FOREIGN KEY(delivery_id) REFERENCES Operation(id),
                    FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id)
                );
            """)

            con.execute("""
                CREATE TABLE IF NOT EXISTS Product_property (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    current_product_id INT NOT NULL,
                    current_product_name VARCHAR(30) NOT NULL,
                    category VARCHAR(30) NOT NULL,
                    characteristics VARCHAR(255) NOT NULL,
                    expiration_date INT,
                    price INT NOT NULL,
                    article_number INT NOT NULL,
                    photo BLOB,
                    FOREIGN KEY(current_product_id) REFERENCES Current_product(id)
                );
            """)

            con.execute("""
                CREATE TABLE IF NOT EXISTS Operation_product (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_id INT NOT NULL,
                    product_id INT NOT NULL,
                    warehouse_id INT NOT NULL,
                    quantity INT NOT NULL,
                    condition VARCHAR(30) NOT NULL,
                    FOREIGN KEY(operation_id) REFERENCES Operation(id),
                    FOREIGN KEY(product_id) REFERENCES Product_property(current_product_id)
                );
            """)
    except Exception as e:
        print("Ошибка при создании базы данных:", e)


def generate_data():
    conn = sl.connect('warehouse.db')
    c = conn.cursor()

    tables_data = {
        'Position': [
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
            ('Перемещение товара на другой склад', 1, 1, '2024-03-17', 'Доп характеристики'),
            ('Продажа товара', 2, 1, '2024-03-18', None),
            ('Принятие товара', 2, 2, '2024-03-19', 'Доп характеристики'),
            ('Списание товара', 3, 3, '2024-03-20', None)
        ],
        'Current_product': [
            (10, 1, 1, '2024-03-01', '2024-03-17', None),
            (10, 1, 1, '2024-03-02', '2024-03-17', None),
            (10, 1, 1, '2024-03-03', '2024-03-17', None),
            (15, 2, 2, '2024-03-04', '2024-03-17', None),
            (0, 2, 2, '2024-03-05', '2024-03-17', None),
            (15, 2, 2, '2024-03-06', '2024-03-17', None),
            (20, 3, 3, '2024-03-07', '2024-03-17', None),
            (20, 3, 3, '2024-03-08', '2024-03-17', None),
            (20, 3, 3, '2024-03-09', '2024-03-17', None),
            (25, 4, 3, '2024-03-10', '2024-03-17', None),
            (20, 4, 1, '2024-03-11', '2024-03-17', None),
            (0, 4, 2, '2024-03-12', '2024-03-17', None)
        ],
        'Product_property': [
            (1, 'Товар 1', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12340, None),
            (2, 'Товар 2', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12341, None),
            (3, 'Товар 3', 'Категория 2', 'Характеристики', '2024-03-17', 200, 12342, None),
            (4, 'Товар 4', 'Категория 2', 'Характеристики', '2024-03-17', 100, 12343, None),
            (5, 'Товар 5', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12344, None),
            (6, 'Товар 6', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12345, None),
            (7, 'Товар 7', 'Категория 2', 'Характеристики', '2024-03-17', 100, 12346, None),
            (8, 'Товар 8', 'Категория 2', 'Характеристики', '2024-03-17', 100, 12347, None),
            (9, 'Товар 9', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12348, None),
            (10, 'Товар 10', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12349, None),
            (11, 'Товар 11', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12310, None),
            (12, 'Товар 12', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12311, None),
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
            (4, 12, 2, 14, 'Доставлен')
        ]
    }

    for table, data in tables_data.items():
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        query_headers = f"PRAGMA table_info({table})"
        headers = c.execute(query_headers).fetchall()

        if count == 0:
            columns = ', '.join([column[1] for column in headers[1:]])
            placeholders = ', '.join(['?' for _ in range(len(data[0]))])
            c.executemany(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", data)

    conn.commit()
    conn.close()
