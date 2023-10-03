import logging
import urllib

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


class Table:
    EXISTING_JOBS_SCHEMA = {
        "Job Date": "",
        "Address Number": "",
        "Street Name": "",
        "Job Number": "",
        "Parcel ID": "",
        "subdivision": "",
        "Lot": "",
        "block": "",
        "Plat Book": "",
        "Plat Page": "",
        "Legal Description": "",
        "Entry By": "",
        "Additional Information": "",
        "Customer Contact Information": "",
        "Customer Requests": "",
        "Benchmark": "",
    }

    ACTIVE_JOBS_SCHEMA = {
        "Order Date": "",
        "Job Number": "",
        "Parcel ID": "",
        "County": "",
        "Address": "",
        "Zip Code": "",
        "Requested Services": "",
        "Fieldwork Status": "",
        "Inhouse Status": "",
        "Invoice Status": "",
        "Customer Contact Information": "",
        "Legal Description": "",
        "Additional Information": "",
    }

    def __init__(self, name: str, columns: dict):
        self.name = name
        self.columns = columns

    def set_data(self, column: str, data: str):
        self.columns[column] = data

    @property
    def columns_with_data(self) -> list:
        return [column for column in self.columns if self.columns[column]]

    @property
    def column_data_values(self) -> list:
        return [self.columns[column] for column in self.columns_with_data]

    @property
    def sql_formatted_columns(self) -> list:
        columns = [f"[{column}]" for column in self.columns_with_data]
        return ", ".join(columns)

    @property
    def sql_formatted_values(self) -> list:
        values = ", ".join(
            [f":{column.replace(' ','')}" for column in self.columns_with_data]
        )
        print(values)
        return values


class AccessDB:
    """Class to interact with the access database."""

    DRIVER = "{Microsoft Access Driver (*.mdb, *.accdb)}"

    def __init__(self, db_path: str):
        """Initializes the AccessDB class.

        Args:
            db_path (str): The path to the access database.
        """
        connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            rf"DBQ={db_path};"
            r"ExtendedAnsiSQL=1;"
        )
        urllib_parse = urllib.parse.quote_plus(connection_string)
        connection_uri = f"access+pyodbc:///?odbc_connect={urllib_parse}"

        logging.debug(f"Connection string: {connection_uri}")

        self.engine = create_engine(connection_uri)
        logging.debug(f"Engine created: {self.engine}")

        self.session = sessionmaker(bind=self.engine)()
        logging.debug(f"Session created: {self.session}")

        self.all_job_data = self.get_all_job_data()
        logging.debug(f"All job data: {self.all_job_data}")

        self.query_types = {
            "INSERT": self.insert_query,
            "UPDATE": self.update_query,
        }

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

        df1 = pd.read_sql(existing_jobs_query, self.engine)
        df2 = pd.read_sql(hebb_hanskin_query, self.engine)
        df3 = pd.read_sql(mckinzie_query, self.engine)

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

    def run_query(
        self,
        table: Table,
        query_type: str,
        commit: bool = False,
    ) -> bool:
        """Runs a query on the active database engine.

        Args:
            table (Table): The Table object to retrieve the table name
                and column data from.
            query_type (str): The type of query to run with the data.
            commit (bool): Whether or not to commit the query to the
                database after execution. Defaults to False

        Returns:
            bool: True if query was successful. False otherwise.
        """
        invalid_query_type = query_type not in self.query_types.keys()
        invalid_commit_statement = not isinstance(commit, bool)
        invalid_table = not isinstance(table, Table)

        if invalid_query_type or invalid_commit_statement or invalid_table:
            return False

        try:
            self.query_types[query_type](table)
            if commit:
                self.session.commit()
                logging.info(f"Committed {table.name} with {table.columns}")
            else:
                logging.info(f"Dry run of {table.name} with {table.columns}")
            return True

        except Exception as e:
            logging.error(
                f"Error running query {query_type}. {table.name},\
 {table.columns}, {e}"
            )
            return False

    def insert_query(self, table: Table) -> None:
        """Runs an insert query on the active database connection.

        Args:
            table (Table): The Table object to retrieve the table name
                and column data from.
        """
        logging.debug(
            f"Running insert query on {table.name} with {table.columns}"
        )
        if not self.is_valid(table):
            return

        query = f"INSERT INTO [{table.name}] ({table.sql_formatted_columns})\
 VALUES ({table.sql_formatted_values})"
        logging.debug(f"Query: {query}")

        values = {
            column.replace(" ", ""): table.columns[column]
            for column in table.columns_with_data
        }
        logging.debug(f"Values: {values}")

        self.session.execute(text(query), values)
        logging.info(f"Inserted {table.name} with {table.columns}")

    def update_query(self, table: Table) -> None:
        """Runs an update query on the active database connection.

        Args:
            table (Table): The Table object to retrieve the table name
                and column data from.
        """
        logging.debug(
            f"Running update query on {table.name} with {table.columns}"
        )
        if not self.is_valid(table):
            return

        set_statement = ", ".join(
            [
                f"[{column}] = '{table.columns[column]}'"
                for column in table.columns_with_data
            ]
        )

        query = f"UPDATE [{table.name}] SET {set_statement} WHERE [Job Number]\
 = '{table.columns['Job Number']}'"

        self.session.execute(text(query))
        logging.info(f"Updated {table.name} with {table.columns}")

    def is_valid(self, table: Table) -> bool:
        """Checks if the table is valid.

        Args:
            table (Table): The table to check.

        Returns:
            bool: True if the table is valid. False otherwise.
        """
        if not isinstance(table, Table):
            return False
        if not table.columns_with_data:
            return False
        if not table.columns.get("Job Number"):
            return False
        return True

    def execute_generic_query(self, query: str) -> list:
        """Executes a generic query on the database.

        Args:
            query (str): The query to execute.

        Returns:
            list: The results of the query.
        """
        return self.session.execute(text(query)).fetchall()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    db = AccessDB("\\\\server\\access\\Database Backup\\MainDB_be.accdb")
    table = Table("Existing Jobs", Table.EXISTING_JOBS_SCHEMA)
    table.set_data("Job Number", "12345")
    table.set_data("Address Number", "12345")
    table.set_data("Street Name", "12345")
    table.set_data("subdivision", "12345")
    db.run_query(table, "INSERT", False)

    table.set_data("subdivision", "5251")
    db.run_query(table, "UPDATE", False)
    print(
        db.session.execute(
            text("SELECT * FROM [Existing Jobs] WHERE [Job Number] = '12345'")
        ).fetchall()
    )
