from sys import exc_info
import psycopg2 as pg


def error_print(err) -> None:
    err_type, err_obj, traceback = exc_info()
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


class DataBase:
    def __init__(self, db: str, user: str, host: str, password: str):
        try:
            self.connection = pg.connect(f"dbname={db} user={user} host={host} password={password}")
        except pg.OperationalError as e:
            error_print(e)
            self.connection = None
        else:
            print("Successful connected.")
            self.cursor = self.connection.cursor()

    # def create(self, table: str, values: dict) -> None:
    #     self.cursor.execute(f"""
    #     INSERT INTO {table} VALUES ({",".join(["%s " for _ in range(len(values))])})
    #     """, list(values.values()))
    #
    # def read(self, table: str) -> tuple:
    #     self.cursor.execute(f"""
    #     SELECT * FROM {table}
    #     """)
    #     return self.cursor.fetchall()[-1]
    #
    # def update(self, table: str, params: dict, primary_key: dict) -> None:
    #     self.cursor.execute(f"""
    #     UPDATE {table}
    #     SET {", ".join([f"{key} = '{params[key]}'" for key in params])}
    #     WHERE {" AND ".join([f"{key} = '{primary_key[key]}'" for key in primary_key])}
    #     """)
    #
    # def delete(self, table: str, primary_key: dict) -> None:
    #     self.cursor.execute(f"""
    #     DELETE FROM {table} WHERE {" AND ".join([f"{key} = '{primary_key[key]}'" for key in primary_key])}
    #     """)

    def create_calendar(self, event_id: int, group_id: int, event_name: str, calendar_grid: list[str],
                        active: bool = True) -> None:
        if self.connection:
            try:
                self.cursor.execute("""
                    INSERT INTO calendars VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    );
                """, (event_id, group_id, event_name, calendar_grid, active))
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
        else:
            print("Data Base doesn't connected")

    def create_vote(self, event_id: int,  chat_id: int, username: str, positions: list[bool]) -> None:
        if self.connection:
            try:
                self.cursor.execute("""
                    INSERT INTO marks VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                    );
                """, (event_id, chat_id, username, positions))
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
        else:
            print("Data Base doesn't connected")

    def read_calendar(self, event_id: int) -> tuple:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT calendar_grid FROM calendars, positions FROM marks
                    WHERE event_id = %s;
                """, event_id)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None, False
            else:
                return self.cursor.fetchall()
        else:
            print("Data Base doesn't connected")
            return None, False

    def update_vote(self, event_id: int, chat_id: int, positions: list[bool]) -> None:
        if self.connection:
            try:
                self.cursor.execute("""
                    UPDATE marks
                    SET positions = %s
                    WHERE event_id = %s AND chat_id = %s
                """, (positions, event_id, chat_id))
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
        else:
            print("Data Base doesn't connected")

    def commit(self) -> None:
        if self.connection:
            self.connection.commit()
        else:
            print("Data Base doesn't connected")

    def close_connection(self) -> None:
        if self.connection:
            self.commit()
            self.cursor.close()
            self.connection.close()
        else:
            print("Data Base doesn't connected")

    def refresh_conn(self, db: str, user: str, host: str, password: str):
        try:
            self.connection = pg.connect(f"dbname={db} user={user} host={host} password={password}")
        except pg.OperationalError as e:
            error_print(e)
            self.connection = None
        else:
            print("Successful connected.")
            self.cursor = self.connection.cursor()
