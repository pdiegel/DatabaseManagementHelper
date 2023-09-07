import pyodbc
from typing import Tuple
from pyodbc import Connection, Cursor
import pandas as pd


class AccessDB:
    """Class to interact with the access database."""

    DRIVER = "{Microsoft Access Driver (*.mdb, *.accdb)}"

    def __init__(self, db_path: str):
        self.connection_string = f"DRIVER={self.DRIVER};DBQ={db_path}"
        self.connection, self.cursor = self.connect_to_database()
        self.all_job_data = self.get_all_job_data()

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

    def get_all_job_data(self) -> pd.DataFrame:
        """Queries the database for the existing job data, and returns
        a DataFrame with the data merged from each table.

        Returns:
            pd.DataFrame: The existing job data.
        """
        df = self.normalize_dataframes()
        return df

    def normalize_dataframes(self) -> pd.DataFrame:
        """Normalizes the column names in the DataFrames for easier
        data manipulation.

        Returns:
            pd.DataFrame: The DataFrame with the normalized columns.
        """
        existing_jobs_query = """SELECT [Address Number], [Street Name],\
 [Job Number], [subdivision], [Lot], [block] FROM [Existing Jobs]"""
        hebb_hanskin_query = """SELECT [Street Number], [Street Name],\
 [Job Number], [Subdivision], [Lot], [Block] FROM [Hebb & Hanskin]"""
        mckinzie_query = """SELECT [Property Address], [Subdivision],
 [Lot], [Block] FROM [McKinzie]"""
        df1 = pd.read_sql(existing_jobs_query, self.connection)
        df2 = pd.read_sql(hebb_hanskin_query, self.connection)
        df3 = pd.read_sql(mckinzie_query, self.connection)

        df1["Subdivision"] = df1["subdivision"]
        df1["Block"] = df1["block"]

        df1.drop(columns=["subdivision", "block"], inplace=True)

        self.combine_address_columns(
            df1, "Property Address", "Address Number", "Street Name"
        )
        self.combine_address_columns(
            df2, "Property Address", "Street Number", "Street Name"
        )

        df = pd.concat([df1, df2, df3], axis=0, ignore_index=True).fillna("")
        return df

    def combine_address_columns(
        self,
        df: pd.DataFrame,
        output_name: str,
        input_name1: str,
        input_name2: str,
    ) -> pd.DataFrame:
        """Combines the address columns into one column.

        Args:
            df (pd.DataFrame): The DataFrame with the address columns.
            output_name (str): The name of the output address column.
            input_name1 (str): The name of the first address input column.
            input_name2 (str): The name of the second address input column.

        Returns:
            pd.DataFrame: The DataFrame with the address columns
                combined.
        """
        df[output_name] = df[input_name1].astype(str) + " " + df[input_name2]
        df.drop(columns=[input_name1, input_name2], inplace=True)
        return df
