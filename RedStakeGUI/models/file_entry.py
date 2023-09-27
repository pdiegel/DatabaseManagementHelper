import logging

import ttkbootstrap as ttk

from RedStakeGUI.constants import ACCESS_DATABASE
from RedStakeGUI.models.access_database import Table
from RedStakeGUI.models.data_collection import DataCollector
from RedStakeGUI.models.job_number_storage import JobNumberStorage


class DatabaseHelper:
    """Contains all the database-related logic"""

    def update_table(
        self,
        table: Table,
        commit: bool = True,
    ) -> None:
        """Updates the given table with the given data.

        Args:
            table (Table): The table to be updated.
            commit (bool, optional): Whether or not to commit the
                changes to the database. Defaults to True.
        """
        ACCESS_DATABASE.run_query(table, "UPDATE", commit)

    def insert_into_table(
        self,
        table: Table,
        commit: bool = True,
    ) -> None:
        """Inserts the given data into the given table.

        Args:
            table (Table): The table to insert the data into.
            commit (bool, optional): Whether or not to commit the
                changes to the database. Defaults to True.
        """
        ACCESS_DATABASE.run_query(table, "INSERT", commit)

    def gather_existing_job_contacts(self, job_number: str) -> tuple:
        """Gathers the existing job contacts from the access database.

        Returns:
            tuple: The existing job contacts.
        """
        existing_job_contacts = ACCESS_DATABASE.connection.execute(
            f"SELECT [Additional Information], [Customer Contact Information],\
[Customer Requests] FROM [Existing Jobs] WHERE [Job Number] = '{job_number}'"
        )
        return existing_job_contacts.fetchall()


class FileEntryModel:
    INFO_LABEL_CODES = {
        1: "Please enter a County.",
        2: "Please enter a Parcel ID number.",
        3: "Please enter a Parcel ID number and a county.",
        4: "Error: Parcel ID number {parcel_id} not found in {county}.",
        5: "Retrieving data for Parcel ID number: {parcel_id}...",
        6: "Data retrieved for Parcel ID number: {parcel_id}.",
        7: "User Inputs Cleared.",
        8: "Data unavailable for County: {county}.",
        9: "New Job Number {job_number} generated.",
        10: "Updating job number {job_number}...",
        11: "Job number {job_number} updated.",
        12: "Creating new job number {job_number}...",
        13: "Error creating new job number {job_number}.",
        14: "Activating job number {job_number}...",
        15: "New entry for job number {job_number} created.",
    }

    GUI_TO_PARCEL_KEY_MAP = {
        "Address": "PRIMARY_ADDRESS",
        "Zip Code": "PROP_ZIP",
        "Plat": "SUBDIVISION",
    }

    def __init__(self, inputs: dict, info_label: ttk.Label):
        self.inputs = inputs
        self.info_label = info_label
        self.database_helper = DatabaseHelper()
        self.job_number_storage = JobNumberStorage(ACCESS_DATABASE)

    def gather_job_data(self) -> dict:
        """Gathers the job data from the user inputs and the parcel data
        from the parcel data module.

        Returns:
            dict: The job data to be submitted to the access database.
        """
        job_number = self.inputs["Job Number"].get()

        county = self.inputs["County"].get()
        parcel_id = self.inputs["Parcel ID"].get()
        if not county or not parcel_id:
            return self.update_info_label(3)

        parcel_data = DataCollector(parcel_id, county).parcel_data
        logging.info(parcel_data)

        job_data = {
            "Job Number": job_number,
            "County": county,
            "Address Number": parcel_data["PROP_HN"],
            "Street Name": parcel_data["POSTAL_STREET"],
            "Parcel ID": parcel_id,
            "subdivision": parcel_data["SUBDIVISION"],
            "Lot": parcel_data["LOT"],
            "block": parcel_data["BLOCK"],
            "Plat Book": parcel_data["PLAT_BOOK"],
            "Plat Page": parcel_data["PLAT_PAGE"],
            "Legal Description": parcel_data["LEGAL_DESC"],
            "Entry By": self.inputs["Entry By"].get(),
            "Additional Information": self.inputs[
                "Additional Information"
            ].get(),
            "Customer Contact Information": self.inputs[
                "Contact Information"
            ].get(),
            "Order Date": self.inputs["Job Date"].entry.get(),
            "Job Date": self.inputs["Job Date"].entry.get(),
            "Address": parcel_data["PRIMARY_ADDRESS"],
            "Zip Code": parcel_data["PROP_ZIP"],
            "Requested Services": self.inputs["Requested Services"].get(),
            "Fieldwork Status": self.inputs["Fieldwork Date"].entry.get(),
            "Inhouse Status": self.inputs["Inhouse Date"].entry.get(),
        }
        return job_data

    def configure_tables(self, job_data: dict) -> tuple:
        """Configures the existing job table and the active job table
        with the given job data.

        Args:
            job_data (dict): The job data to be submitted to the access
                database.

        Returns:
            tuple: A tuple containing the existing job table and the
                active job table.
        """
        existing_job_table = Table("Existing Jobs", Table.EXISTING_JOBS_SCHEMA)
        active_job_table = Table("Active Jobs", Table.ACTIVE_JOBS_SCHEMA)

        for dictionary in [
            existing_job_table.columns,
            active_job_table.columns,
        ]:
            for key in dictionary.keys():
                if key in job_data.keys():
                    dictionary[key] = job_data[key]

        return existing_job_table, active_job_table

    def handle_existing_active_job(
        self,
        job_number: str,
        existing_job_table: Table,
        active_job_table: Table,
    ) -> None:
        """Handles the case where the job number already exists in the
        database and is active.

        Args:
            job_number (str): The job number to be updated.
            existing_job_table (Table): The existing job table.
            active_job_table (Table): The active job table.
        """
        self.update_info_label(10, job_number=job_number)
        try:
            logging.info(f"Updating job number {job_number}...")
            self.database_helper.update_table(existing_job_table)
            self.database_helper.update_table(active_job_table)
            self.update_info_label(11, job_number=job_number)
            logging.info(f"Job Number {job_number} updated.")
        except Exception as e:
            logging.error(e)
            self.update_info_label(13, job_number=job_number)

    def handle_existing_inactive_job(
        self,
        job_number: str,
        existing_job_table: Table,
        active_job_table: Table,
    ) -> None:
        """Handles the case where the job number already exists in the
        database but is not active.

        Args:
            job_number (str): The job number to be updated.
            existing_job_table (Table): The existing job table.
            active_job_table (Table): The active job table.
        """
        self.update_info_label(10, job_number=job_number)
        try:
            logging.info(f"Activating job number {job_number}...")
            self.database_helper.update_table(existing_job_table)
            self.database_helper.insert_into_table(active_job_table)
            self.update_info_label(14, job_number=job_number)
            logging.info(f"Job Number {job_number} activated.")
        except Exception as e:
            logging.error(e)
            self.update_info_label(13, job_number=job_number)

    def handle_new_job(
        self,
        job_number: str,
        existing_job_table: Table,
        active_job_table: Table,
    ) -> None:
        """Handles the case where the job number does not exist in the
        database.

        Args:
            job_number (str): The job number to be updated.
            existing_job_table (Table): The existing job table.
            active_job_table (Table): The active job table.
        """
        self.update_info_label(12, job_number=job_number)
        try:
            logging.info(f"Creating new job number {job_number}...")
            self.database_helper.insert_into_table(existing_job_table)
            self.database_helper.insert_into_table(active_job_table)
            self.update_info_label(15, job_number=job_number)
            logging.info(f"Job Number {job_number} created.")
        except Exception as e:
            logging.error(e)
            self.update_info_label(13, job_number=job_number)

    def submit_job_data(self) -> None:
        """Submits the job data to the access database. If the job
        number already exists in the database, the job data will be
        updated. Otherwise, a new job will be created."""
        job_data = self.gather_job_data()
        job_number = job_data["Job Number"]

        existing_job_table, active_job_table = self.configure_tables(job_data)

        job_exists = job_number in self.job_number_storage.existing_job_numbers
        job_is_active = job_number in self.job_number_storage.active_job_numbers

        if job_exists and job_is_active:
            self.handle_existing_active_job(
                job_number, existing_job_table, active_job_table
            )
        elif job_exists and not job_is_active:
            self.handle_existing_inactive_job(
                job_number, existing_job_table, active_job_table
            )
        elif not job_exists:
            self.handle_new_job(
                job_number, existing_job_table, active_job_table
            )
        else:
            self.update_info_label(12, job_number=job_number)

    def generate_fn(self) -> None:
        """Generates a new job number for the user. The job number is
        generated by taking the current year and adding a number to the
        end of it. The number is the next unused job number in the
        database."""
        current_year = self.job_number_storage.year

        existing_current_year_jobs = ACCESS_DATABASE.connection.execute(
            f"SELECT [Job Number] FROM [Existing Jobs] WHERE [Job Number]\
    LIKE '{current_year}%'"
        )
        self.job_number_storage.add_current_year_job_numbers(
            existing_current_year_jobs
        )
        unused_job_number = self.job_number_storage.unused_job_number

        self.inputs["Job Number"].delete(0, "end")
        self.inputs["Job Number"].insert(0, unused_job_number)
        self.update_info_label(9, job_number=unused_job_number)

    def get_unused_job_number(self) -> str:
        """Returns the next unused job number in the database.

        Returns:
            str: The next unused job number in the database.
        """
        num_previous_months = 0
        while num_previous_months < 12:
            prefix = self.get_job_number_prefix(num_previous_months)
            job_numbers = [
                number
                for number in self.get_current_year_job_numbers()
                if number.startswith(prefix)
            ]
            if len(job_numbers) == 0:
                num_previous_months += 1
            else:
                highest_existing_fn = max(job_numbers)
                last_four_digits = str(int(highest_existing_fn[4:8]) + 1).zfill(
                    4
                )
                new_fn = self.get_job_number_prefix() + last_four_digits
                break
        else:
            new_fn = self.get_job_number_prefix() + "0100"

        return new_fn

    def gather_existing_job_contacts(self) -> None:
        """Gathers the existing job contacts from the access database
        and populates the contact information input field with the
        contact information."""
        job_number = self.inputs["Job Number"].get()
        contact_info = self.database_helper.gather_existing_job_contacts(
            job_number
        )[0]

        additional_info = contact_info[0]
        contact_info = contact_info[1]
        requested_services = contact_info[2]

        contacts = {
            "Additional Information": additional_info,
            "Contact Information": contact_info,
            "Requested Services": requested_services,
        }

        for key, value in contacts.items():
            if value == "N":
                value = ""
            if value:
                self.inputs[key].delete(0, "end")
                self.inputs[key].insert(0, value)

    def clear_inputs(self) -> None:
        """Clears all the input fields."""
        for input_field in self.inputs.values():
            if isinstance(input_field, ttk.Entry):
                input_field.delete(0, "end")
            elif isinstance(input_field, ttk.DateEntry):
                input_field.entry.delete(0, "end")
        self.update_info_label(7)

    def update_info_label(self, code: int, **kwargs) -> None:
        """Updates the info label with the text from the
        INFO_LABEL_CODES dictionary.

        Args:
            code (int): The code for the text to be displayed in the
                info label.
            **kwargs: The format keyword arguments for the text to be
                displayed in the info label.

        """
        text = self.INFO_LABEL_CODES[code].format(**kwargs)
        self.info_label.config(text=text)
