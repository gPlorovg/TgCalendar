import psycopg2 as pg


class DataBase:
    def __init__(self, db, user, host, password):
        try:
            self.connection = pg.connect(f"dbname={db} user={user} host={host} password={password}")
        except:
            print("DB connection error!")
        finally:
            if self.connection:
                self.close_connection()
        self.cursor = self.connection.cursor()

    def create(self, table: str, values: dict):
        self.cursor.execute(f"""
        INSERT INTO {table} VALUES ({",".join(["%s " for _ in range(len(values))])})
        """, list(values.values()))

    def read(self, table: str) -> tuple:
        self.cursor.execute(f"""
        SELECT * FROM {table}
        """)
        return self.cursor.fetchall()[-1]

    def update(self, table: str, params: dict, primary_key: dict):
        self.cursor.execute(f"""
        UPDATE {table}
        SET {", ".join([f"{key} = '{params[key]}'" for key in params])}
        WHERE {" AND ".join([f"{key} = '{primary_key[key]}'" for key in primary_key])}
        """)

    def delete(self, table: str, primary_key: dict):
        self.cursor.execute(f"""
        DELETE FROM {table} WHERE {" AND ".join([f"{key} = '{primary_key[key]}'" for key in primary_key])}
        """)

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.commit()
        self.cursor.close()
        self.connection.close()
