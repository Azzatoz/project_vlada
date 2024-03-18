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
                    operation_id NOT NULL,
                    warehouse_id INT NOT NULL,
                    delivery_date INT NOT NULL,
                    expiration_date_operation INT,
                    FOREIGN KEY(operation_id) REFERENCES Operation(id),
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
                    warehouse_id INT,
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

    tables = ['Position', 'Warehouse', 'Client', 'Worker', 'Operation', 'Current_product', 'Product_property',
              'Operation_product']

    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]

        if count == 0:
            if table == 'Position':
                positions = [('Директор', 50000, 5), ('Менеджер', 50000, 4), ('Кладовщик', 50000, 3),
                             ('Кассир', 50000, 2), ('Новый пользователь', 0, 1)]
                c.executemany("INSERT INTO Position (name_position, salary, access_level) "
                              "VALUES (?, ?, ?)", positions)

            elif table == 'Warehouse':
                warehouses = [('Склад 1', 'г.Минск, ул.Богдановича, дом 71', 37.7749, '37.7749', 'Товар 1, товар 2'),
                              ('Склад 2', 'г.Минск, ул.Богдановича, дом 72', 37.7749, '37.7749', 'Товар 3, товар 4'),
                              ('Склад 3', 'г.Минск, ул.Богдановича, дом 73', 37.7749, '37.7749', 'Товар 5, товар 6')]
                c.executemany("INSERT INTO Warehouse (name, address, coordinates, geolocation, json_product) "
                              "VALUES (?, ?, ?, ?, ?)", warehouses)

            elif table == 'Client':
                clients = [('Клиент 1', 1234567890, 'Любит гулять'),
                           ('Клиент 2', 1256787890, 'Любит играть'),
                           ('Клиент 3', 4567567890, 'Не любит играть'),
                           ('Клиент 4', 9876543210, 'Не любит гулять')]
                c.executemany("INSERT INTO Client (name, phone_number, json_note) VALUES (?, ?, ?)", clients)

            elif table == 'Worker':
                workers = [('Иван Иванов', '2000-01-01', 1233467890, 1, 'admin1', 'admin'),
                           ('Коля Черничка', '2000-05-02', 1234457890, 2, 'admin2', 'admin'),
                           ('Вася Васильков', '2005-04-01', 1223467890, 3, 'admin3', 'admin'),
                           ('Илья Котиков', '2003-02-01', 1298567890, 4, 'admin4', 'admin')]
                c.executemany(
                    "INSERT INTO Worker (name, birthday, phone_number, position_id, username, password)"
                    " VALUES (?, ?, ?, ?, ?, ?)", workers)

            elif table == 'Operation':
                operations = [('Перемещение товара на другой склад', 1, 1, '2024-03-17', 'Доп характеристики'),
                              ('Продажа товара', 2, 1, '2024-03-18', None),
                              ('Принятие товара', 2, 2, '2024-03-19', 'Доп характеристики'),
                              ('Списание товара', 3, 3, '2024-03-20', None)]
                c.executemany(
                    "INSERT INTO Operation (type, client_id, worker_id, time, additional_characteristics) "
                    "VALUES (?, ?, ?, ?, ?)", operations)

            elif table == 'Current_product':
                current_products = [(10, 1, 1, '2024-03-17', '2024-03-17'),
                                    (15, 1, 2, '2024-03-18', '2024-03-17'),
                                    (20, 2, 1, '2024-03-19', '2024-03-17'),
                                    (25, 3, 3, '2024-03-20', '2024-03-17'),
                                    (30, 4, 2, '2024-03-21', '2024-03-17')]
                c.executemany(
                    "INSERT INTO Current_product (quantity, operation_id, warehouse_id, delivery_date, "
                    "expiration_date_operation) VALUES (?, ?, ?, ?, ?)", current_products)

            elif table == 'Product_property':
                product_properties = [(1, 'Товар 1', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12340, None),
                                      (1, 'Товар 1', 'Категория 1', 'Характеристики', '2024-03-17', 100, 12340, None),
                                      (2, 'Товар 2', 'Категория 2', 'Характеристики', '2024-03-17', 200, 12341, None),
                                      (3, 'Товар 3', 'Категория 3', 'Характеристики', '2024-03-17', 100, 12342, None),
                                      (4, 'Товар 4', 'Категория 4', 'Характеристики', '2024-03-17', 170, 12343, None)]
                c.executemany(
                    "INSERT INTO Product_property (current_product_id, current_product_name, category, "
                    "characteristics, expiration_date, price, article_number, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    product_properties)

            elif table == 'Operation_product':
                operation_products = [(1, 1, None, 10, 'Доставлен'),
                                      (2, 2, 1, 11, 'На складе'),
                                      (2, 3, None, 12, 'На складе'),
                                      (3, 3, 1, 13, 'На складе'),
                                      (4, 1, None, 14, 'Доставлен')]
                c.executemany(
                    "INSERT INTO Operation_product (operation_id, product_id, warehouse_id, quantity, condition) "
                    "VALUES (?, ?, ?, ?, ?)", operation_products)

    conn.commit()
    conn.close()
