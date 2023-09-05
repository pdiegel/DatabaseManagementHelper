import pyodbc
from typing import Tuple
from pyodbc import Connection, Cursor


class AccessDB:
    """Class to interact with the access database."""

    DRIVER = "{Microsoft Access Driver (*.mdb, *.accdb)}"

    def __init__(self, db_path: str):
        self.connection_string = f"DRIVER={self.DRIVER};DBQ={db_path}"
        self.connection, self.cursor = self.connect_to_database()

    def connect_to_database(self) -> Tuple[Connection, Cursor]:
        """Attempts to connect to the database.

        Returns:
            Tuple[Connection, Cursor]: The connection and cursor
            objects.
        """
        try:
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()
        except pyodbc.Error as error:
            print(error)
            raise error
        else:
            for table_info in cursor.tables(tableType="TABLE"):
                print(table_info.table_name)
            return connection, cursor
