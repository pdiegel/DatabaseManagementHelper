import logging
from tkinter import Event
from typing import List, Tuple
from datetime import datetime

import ttkbootstrap as ttk

from DatabaseManager.constants import ACCESS_DATABASE
from DatabaseManager.models.access_database import AccessDB


class FileStatusCheckerModel:
    INFO_LABEL_CODES = {
        1: "File Number {file_number} not found.",
        2: "File Number {file_number} found.",
        3: "File number copied to clipboard.",
        4: "Inputs cleared.",
        5: "Please enter a file number or parcel ID.",
        6: "Parcel ID {parcel_id} not found.",
        7: "Parcel ID {parcel_id} found.",
        8: "Unable to find file number or parcel ID.",
    }

    def __init__(self, view: ttk.Frame):
        self.inputs = view.inputs
        self.programmable_inputs = view.programmable_inputs
        self.info_label = view.info_label
        self.inputs["File Number"].bind("<Return>", self.on_enter)
        self.inputs["Parcel ID"].bind("<Return>", self.on_enter)

    def lookup_file(self) -> None:
        """Looks up the file number in the database and populates the
        input fields with the data from the database.

        If the file number is not found, the info label will display
        an error message. If the file number is found, the info label
        will display a success message.
        """
        access_db = ACCESS_DATABASE
        entered_file_number = self.inputs["File Number"].get().strip()
        entered_parcel_id = self.inputs["Parcel ID"].get().strip()
        if not entered_file_number and not entered_parcel_id:
            logging.info("No file number or parcel ID entered.")
            self.update_info_label(5)
            return

        logging.info(
            f"Looking up file number {entered_file_number} in database."
        )

        (
            active_job_data,
            existing_job_data,
            signature_status_data,
        ) = self.get_job_data(access_db, entered_file_number, entered_parcel_id)

        (
            order_date,
            fieldwork_status,
            inhouse_status,
            county,
            scope_of_work,
        ) = (
            active_job_data[0] if active_job_data else [""] * 5
        )

        (
            file_number,
            parcel_id,
            address_number,
            street_name,
            lot,
            block,
            subdivision,
        ) = (
            existing_job_data[0] if existing_job_data else [""] * 7
        )

        (
            signed,
            signed_scope_of_work,
            signature_date,
            signature_notes,
        ) = (
            signature_status_data[0] if signature_status_data else [""] * 4
        )

        address_number = address_number if address_number else ""
        address = f"{address_number} {street_name}".strip()
        active = "Yes" if active_job_data else "No"

        dates_to_format = [
            "Order Date",
            "Signature Date",
            "Fieldwork Status",
            "Inhouse Status",
        ]

        logging.info("Successfully formatted data from database.")

        data_map = {
            "File Number": file_number,
            "Order Date": order_date,
            "Active": active,
            "Fieldwork Status": fieldwork_status,
            "Inhouse Status": inhouse_status,
            "Property Address": address,
            "County": county,
            "Parcel ID": parcel_id,
            "Lot": lot,
            "Block": block,
            "Subdivision": subdivision,
            "Scope of Work": scope_of_work,
            "Signed": signed,
            "Signed Scope of Work": signed_scope_of_work,
            "Signature Date": signature_date,
            "Signature Notes": signature_notes,
        }

        for date in dates_to_format:
            data_map[date] = (
                data_map[date].strftime("%m/%d/%Y")
                if data_map[date] and isinstance(data_map[date], datetime)
                else ""
            )
        logging.info(f"Determined data map: {data_map}.")

        for label, entry_data in data_map.items():
            if label in self.inputs.keys():
                if not existing_job_data:
                    break
                if not entry_data:
                    entry_data = ""
                self.inputs[label].delete(0, "end")
                self.inputs[label].insert(0, entry_data)
                continue
            entry_data = str(entry_data).title() if entry_data else ""
            entry = self.programmable_inputs[label]
            # Cannot insert text into a readonly entry
            entry.config(state="normal")
            entry.delete(0, "end")
            entry.insert(0, entry_data)
            entry.config(state="readonly")

        if not existing_job_data:
            if entered_parcel_id and not entered_file_number:
                self.update_info_label(6, parcel_id=entered_parcel_id)
            elif entered_parcel_id and entered_file_number:
                self.update_info_label(8)
            else:
                self.update_info_label(1, file_number=entered_file_number)
        else:
            self.update_info_label(2, file_number=file_number)

    def get_job_data(
        self, access_db: AccessDB, file_number: str, parcel_id: str
    ) -> Tuple[List[Tuple], List[Tuple], List[Tuple]]:
        """Gets the job data from the database. If the job is not found,
        an empty list will be returned.

        Args:
            access_db (AccessDB): The AccessDB object.
            file_number (str): The file number to look up.
            parcel_id (str): The parcel ID to look up.

        Returns:
            Tuple[List[Tuple], List[Tuple], List[Tuple]]: A tuple of
                lists containing the job data.
        """

        if not file_number or len(file_number) != 8:
            file_number = access_db.execute_generic_query(
                f"SELECT \
[Job Number] FROM [Existing Jobs] WHERE [Parcel ID] = '{parcel_id}'"
            )
            if file_number:
                file_number = file_number[0][0]

        search_query = f"[Job Number] = '{file_number}'"

        existing_jobs_query = f"""SELECT [Job Number], [Parcel ID], \
[Address Number], [Street Name], Lot, block, subdivision FROM [Existing Jobs] \
WHERE {search_query}"""
        active_jobs_query = f"""SELECT [Order Date], [Fieldwork Status],\
 [Inhouse Status], [County], [Requested Services]\
 FROM [Active Jobs] WHERE {search_query}"""
        signature_status_query = f"""SELECT [Signed], [Type of Survey],\
 [Signature Date], [Notes] FROM [Signature Status] WHERE {search_query}"""

        logging.info("Running query for active job data..")
        try:
            active_job_data = access_db.execute_generic_query(active_jobs_query)
            logging.info("Successfully ran query for active job data.")
        except Exception as e:
            logging.error(f"Failed to run query for active job data: {e}")
            active_job_data = []

        logging.info("Running query for existing job data..")
        try:
            existing_job_data = access_db.execute_generic_query(
                existing_jobs_query
            )
            logging.info("Successfully ran query for existing job data.")
        except Exception as e:
            logging.error(f"Failed to run query for existing job data: {e}")
            existing_job_data = []

        logging.info("Running query for signature status data..")
        try:
            signature_status_data = access_db.execute_generic_query(
                signature_status_query
            )
            logging.info("Successfully ran query for signature status data.")
        except Exception as e:
            logging.error(f"Failed to run query for signature status data: {e}")
            signature_status_data = []

        return active_job_data, existing_job_data, signature_status_data

    def clear_inputs(self) -> None:
        """Clears all the input fields."""
        input_objects = list(self.inputs.values())
        programmable_input_objects = list(self.programmable_inputs.values())

        for input_field in input_objects:
            input_field.delete(0, "end")

        for input_field in programmable_input_objects:
            input_field.config(state="normal")
            input_field.delete(0, "end")
            input_field.config(state="readonly")

        logging.info("Cleared input fields.")
        self.update_info_label(4)
        input_objects[0].focus()

    def update_info_label(self, code: int, **kwargs) -> None:
        """Updates the info label with the text from the
        INFO_LABEL_CODES dictionary.

        Args:
            code (int): The code for the text to be displayed in the
                info label.
            **kwargs: The format keyword arguments for the text to be
                displayed in the info label.
        """
        info_text = self.INFO_LABEL_CODES[code].format(**kwargs)
        self.info_label.config(text=info_text)

    def on_enter(self, _event: Event) -> None:
        """Executes the lookup_file method when the user presses the
        enter key.

        Args:
            _event (Event): The event that triggered this function.
                Not used.
        """
        self.lookup_file()
