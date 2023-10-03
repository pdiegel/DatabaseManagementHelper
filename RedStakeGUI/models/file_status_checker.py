import logging
import pyperclip
import ttkbootstrap as ttk
from sqlalchemy import text
from RedStakeGUI.constants import ACCESS_DATABASE
from tkinter import Event


class FileStatusCheckerModel:
    INFO_LABEL_CODES = {
        1: "File Number {file_number} not found.",
        2: "File Number {file_number} found.",
        3: "File number copied to clipboard.",
        4: "Input field cleared.",
    }

    def __init__(self, view: ttk.Frame):
        self.inputs = view.inputs
        self.programmable_inputs = view.programmable_inputs
        self.info_label = view.info_label
        self.inputs["File Number"].bind("<Return>", self.on_enter)

    def lookup_file(self) -> None:
        access_db = ACCESS_DATABASE
        file_number = self.inputs["File Number"].get()

        existing_jobs_query = f"""SELECT Lot, block, subdivision FROM\
 [Existing Jobs] WHERE [Job Number] = '{file_number}'"""
        active_jobs_query = f"""SELECT [Order Date], [Fieldwork Status],\
 [Inhouse Status], [Address], [County], [Parcel ID], [Requested Services]\
 FROM [Active Jobs] WHERE [Job Number] = '{file_number}'"""
        signature_status_query = f"""SELECT [Signed], [Type of Survey],\
 [Signature Date], [Notes] FROM [Signature Status] WHERE [Job Number] =\
 '{file_number}'"""

        active_job_data = access_db.execute_generic_query(active_jobs_query)
        existing_job_data = access_db.execute_generic_query(existing_jobs_query)
        signature_status_data = access_db.execute_generic_query(
            signature_status_query
        )

        (
            order_date,
            fieldwork_status,
            inhouse_status,
            address,
            county,
            parcel_id,
            scope_of_work,
        ) = (
            active_job_data[0] if active_job_data else [""] * 7
        )

        lot, block, subdivision = (
            existing_job_data[0] if existing_job_data else ([""] * 3)
        )

        (
            signed,
            signed_scope_of_work,
            signature_date,
            signature_notes,
        ) = (
            signature_status_data[0] if signature_status_data else [""] * 4
        )

        active = "Yes" if active_job_data else "No"

        order_date = order_date.strftime("%m/%d/%Y") if order_date else None

        data_map = {
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
        for label, entry_data in data_map.items():
            entry_data = str(entry_data).title() if entry_data else ""
            # Cannot insert text into a readonly entry
            self.programmable_inputs[label].config(state="normal")
            self.programmable_inputs[label].delete(0, "end")
            self.programmable_inputs[label].insert(0, entry_data)
            self.programmable_inputs[label].config(state="readonly")

        if not existing_job_data:
            self.update_info_label(1, file_number=file_number)
        else:
            self.update_info_label(2, file_number=file_number)

    def clear_inputs(self) -> None:
        """Clears all the input fields. Ignore the search type field."""
        input_objects = list(self.inputs.values())
        programmable_input_objects = list(self.programmable_inputs.values())

        for input_field in input_objects:
            input_field.delete(0, "end")

        for input_field in programmable_input_objects:
            input_field.config(state="normal")
            input_field.delete(0, "end")
            input_field.config(state="readonly")

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
