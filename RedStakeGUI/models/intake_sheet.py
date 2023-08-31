import os
import smtplib

import ttkbootstrap as ttk

from ..constants import PARCEL_DATA_COUNTIES, QUOTES_DIRECTORY
from .data_collection import DataCollector
from .quote_emailer import QuoteEmail


class IntakeSheetModel:
    INFO_LABEL_CODES = {
        1: "Please enter a County.",
        2: "Please enter a Parcel ID number.",
        3: "Please enter a Parcel ID number and a county.",
        4: "Error: Parcel ID number {parcel_id} not found in {county}.",
        5: "Please enter a Phone Number and/or Email Address.",
        6: "Please enter the name of the person requesting the survey.",
        7: "Please enter the property address.",
        8: "Please enter the Scope of Work.",
        9: "Retrieving data for Parcel ID number: {parcel_id}...",
        10: "Data retrieved for Parcel ID number: {parcel_id}.",
        11: "Data unavailable for County: {county}.",
        12: "User Inputs Cleared.",
        13: "Quote for {property_address} saved.",
        14: "Error saving quote for {property_address}.",
        15: "Error saving quote: File is open in another program.",
        16: "Quote for {property_address} updated with new data.",
        17: "Invalid email login credentials. Please update settings.",
        18: "Quote for {property_address} sent via email.",
        19: "Error printing quote: File is open in another program.",
        20: "Quote for {property_address} printed.",
        21: "Error printing quote.",
    }

    GUI_TO_PARCEL_KEY_MAP = {
        "Address": "PRIMARY_ADDRESS",
        "Zip Code": "PROP_ZIP",
        "Plat": "SUBDIVISION",
    }

    def __init__(self, inputs: dict, info_label: ttk.Label):
        self.inputs = inputs
        self.info_label = info_label

    def validate_parcel_inputs(self, parcel_id: str, county: str) -> bool:
        """Validates the Parcel ID and County fields. Displays an error
        message if either field is empty. Displays an error message if
        the county is not in the PARCEL_DATA_COUNTIES list.

        Args:
            parcel_id (str): The parcel ID number.
            county (str): The county for the parcel ID number.

        Returns:
            bool: True if the Parcel ID and County fields are valid,
        """
        if parcel_id == "" and county == "":
            self.update_info_label(3)
            return False
        if parcel_id == "":
            self.update_info_label(2)
            return False
        if county == "":
            self.update_info_label(1)
            return False
        if county not in PARCEL_DATA_COUNTIES:
            self.update_info_label(11, county=county)
            return False
        return True

    def display_parcel_data(self) -> None:
        """Displays the parcel data for the parcel ID number entered in
        the Parcel ID field. Also displays the address, zip code, and
        plat name for the parcel ID number."""
        parcel_id = self.inputs["Parcel ID"].get().strip()
        county = self.inputs["County"].get().strip()

        if not self.validate_parcel_inputs(parcel_id, county):
            return

        try:
            parcel_data = self.get_parcel_data(parcel_id, county)
        except IndexError:
            return

        self.update_inputs(parcel_data)
        self.update_info_label(10, parcel_id=parcel_id)

    def get_parcel_data(self, parcel_id: str, county: str) -> dict:
        """Gets the parcel data for the parcel ID number.

        Args:
            parcel_id (str): The parcel ID number.
            county (str): The county for the parcel ID number.

        Returns:
            dict: The parcel data dictionary.

        Raises:
            IndexError: If the parcel ID number is not found in the
                county.
        """
        try:
            parcel = DataCollector(parcel_id, county)
            parcel_data = parcel.parcel_data
            self.update_info_label(9, parcel_id=parcel_id)
        except IndexError:
            self.update_info_label(4, parcel_id=parcel_id, county=county)
            raise IndexError
        return parcel_data

    def update_inputs(self, parcel_data: dict) -> None:
        """Updates the Address, Zip Code, and Plat fields with the data
        from the parcel data dictionary. Also updates the Lot & Block
        and Plat Book & Page fields.

        Args:
            parcel_data (dict): The parcel data dictionary.
        """
        for gui_key, parcel_data_key in self.GUI_TO_PARCEL_KEY_MAP.items():
            self.inputs[gui_key].delete(0, "end")
            self.inputs[gui_key].insert(0, parcel_data[parcel_data_key])

        self.update_lot_and_block(parcel_data)
        self.update_plat_book_and_page(parcel_data)

    def update_lot_and_block(self, parcel_data: dict) -> None:
        """Updates the Lot & Block field with the data from the parcel
        data dictionary.

        Args:
            parcel_data (dict): The parcel data dictionary.
        """
        lot = parcel_data["LOT"]
        block = parcel_data["BLOCK"]
        lot_and_block = ""
        if lot != "":
            if block != "":
                lot_and_block = f"LOT {lot}, BLOCK {block}"
            else:
                lot_and_block = f"LOT {lot}"

        self.inputs["Lot & Block"].delete(0, "end")
        self.inputs["Lot & Block"].insert(0, lot_and_block)

    def update_plat_book_and_page(self, parcel_data: dict) -> None:
        """Updates the Plat Book & Page field with the data from the
        parcel data dictionary.

        Args:
            parcel_data (dict): The parcel data dictionary.
        """
        plat_book = parcel_data["PLAT_BOOK"]
        plat_page = parcel_data["PLAT_PAGE"]
        plat_book_and_page = ""
        if plat_book != "":
            if plat_page != "":
                plat_book_and_page = f"BOOK {plat_book}, PAGE {plat_page}"
            else:
                plat_book_and_page = f"BOOK {plat_book}"

        self.inputs["Plat Book & Page"].delete(0, "end")
        self.inputs["Plat Book & Page"].insert(0, plat_book_and_page)

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

    def clear_inputs(self) -> None:
        """Clears all the input fields."""
        for input_field in self.inputs.values():
            input_field.delete(0, "end")
        self.update_info_label(12)

    def save_inputs(self) -> bool:
        """Saves the input fields to a text file.

        Returns:
            bool: True if the file was saved successfully, False if not."""
        address = self.inputs["Address"].get().strip()

        if not address:
            self.update_info_label(7)
            return False

        file_name = f"{address}.txt"
        self.file_save_path = os.path.join(QUOTES_DIRECTORY, file_name)
        quote_exists = os.path.exists(self.file_save_path)
        try:
            with open(self.file_save_path, "w") as quote_file:
                for key, input_field in self.inputs.items():
                    quote_file.write(f"{key}: {input_field.get()}\n")
        except PermissionError:
            self.update_info_label(15)
        except OSError:
            self.update_info_label(14, property_address=address)
        else:
            if quote_exists:
                self.update_info_label(16, property_address=address)
            else:
                self.update_info_label(13, property_address=address)
            return True
        return False

    def email_quote(self) -> None:
        """Emails the quote to the email address specified in the
        settings. It will also save the quote. You can manually change
        the settings in the data/settings.json file, or you can use the
        Settings button to open the Settings window."""
        parcel_id = self.inputs["Parcel ID"].get().strip()
        county = self.inputs["County"].get().strip()

        if not self.validate_parcel_inputs(parcel_id, county):
            return

        try:
            parcel_data = self.get_parcel_data(parcel_id, county)
        except IndexError:
            return

        if not self.save_inputs():
            return

        try:
            emailer = QuoteEmail(self.inputs, parcel_data, self.file_save_path)
            emailer.send_email()
            self.update_info_label(
                18, property_address=parcel_data.get("PRIMARY_ADDRESS", "")
            )
        except smtplib.SMTPAuthenticationError:
            self.update_info_label(17)

    def print_quote(self) -> None:
        """Saves and prints the current quote. Updates the quote if it
        already exists. If the quote is already open in another program,
        displays an error message. Windows is the only operating system
        that is supported at the moment."""
        if not self.save_inputs():
            return

        try:
            os.startfile(self.file_save_path, "print")
            self.update_info_label(
                20, property_address=self.inputs["Address"].get()
            )
        except PermissionError:
            self.update_info_label(19)
        except OSError:
            self.update_info_label(21)
