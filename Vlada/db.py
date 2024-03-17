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
                    json_note VARCHAR(255)
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

    c.execute("SELECT COUNT(*) FROM Position")
    position_count = c.fetchone()[0]

    if position_count == 0:
        positions = [('Директор', 50000, 5), ('Менеджер', 50000, 4), ('Кладовщик', 50000, 3),
                     ('Кассир', 50000, 2), ('Новый пользователь', 0, 1)]

        for position, salary, access_level in positions:
            c.execute("INSERT INTO Position (name_position, salary, access_level) VALUES (?, ?, ?)",
                      (position, salary, access_level))

        names = [('Иван', 'Иванов')]
        for name, surname in names:
            username = "admin"
            password = "admin"
            c.execute("INSERT INTO Worker (name, phone_number, birthday, username, password, position_id) "
                      "VALUES (?, ?, ?, ?, ?, ?)",
                      (f"{name} {surname}", '1234567890', '2000-01-01', username, password, 1))  # Директор с id = 1

        conn.commit()

    conn.close()
