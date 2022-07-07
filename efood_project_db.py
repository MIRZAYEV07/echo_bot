import sqlite3


class Database():
    def __init__(self):
        self.db_name = " efood_2_0.db"
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS "food_menu"(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    parent_id INTEGER,
                    FOREIGN KEY (parent_id)
                    REFERENCES food_menu(id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                                    )

            """)

        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS "food_type"(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                    )        
            """)

        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS "food_product"(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    about TEXT NOT NULL,
                    photo TEXT NOT NULL,
                    price TEXT NOT NULL,
                    menu_id INTEGER NOT NULL,
                    type_id INTEGER NOT NULL,
                    FOREIGN KEY(menu_id) REFERENCES food_menu(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
                    FOREIGN KEY(type_id) REFERENCES food_type(id)
                    ON UPDATE CASCADE ON DELETE CASCADE


                )
            """)
        self.conn.commit()

    def get_menu(self):
        a = self.conn.execute("""
            SELECT * FROM food_menu
            WHERE parent_id is NULL

        """).fetchall()
        return a

    def get_child_menu(self, id):
        a = self.conn.execute("""
            SELECT * FROM food_menu
            WHERE parent_id = ?
        """, [id]).fetchall()
        return a

    def type_1(self, id):
        b = self.conn.execute("""
          SELECT t.name, t.id FROM food_product as p
            INNER JOIN food_type as t
            ON p.type_id = t.id
            WHERE p.menu_id = ?  
        """, [id]).fetchall()
        return b

    def product(self, b, id):
        a = self.conn.execute("""
        SELECT * FROM food_product
        WHERE menu_id = ? and type_id = ?

        """, [b, id]).fetchone()
        return a

    def make_savatcha(self, id):
        self.conn.execute(f"""
        CREATE TABLE IF NOT EXISTS "{id}"(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
        """)
        self.conn.commit()

    def savatcha(self, id, q, d):
        self.conn.execute(f"""
            INSERT INTO "{d}" (name,price)
            VALUES(?,?)
        """, [id, q])
        self.conn.commit()

    def del_savatcha(self, id):
        self.conn.execute(f"""
            DROP TABLE IF  EXISTS "{id}"
        """)

    def get_savatcha(self, d):
        b = ''
        a = self.conn.execute(f"""
        SELECT name FROM {d}
        """).fetchall()
        for j in a:
            b += j['name']
        return b

    def get_price(self, d):
        b = 0
        a = self.conn.execute(f"""
        SELECT price FROM {d}
        """).fetchall()
        for j in a:
            b += j['price']
        return b


a = Database()

print(a.get_menu())