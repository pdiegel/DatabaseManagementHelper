import webbrowser

import ttkbootstrap as ttk

from RedStakeGUI.constants import PARCEL_DATA_COUNTIES
from RedStakeGUI.models.data_collection import DataCollector


class WebsiteSearchModel:
    INFO_LABEL_CODES = {
        1: "Please enter a County.",
        2: "Please enter a Parcel ID number.",
        3: "Please enter a Parcel ID number and a county.",
        4: "Error: Parcel ID number {parcel_id} not found in {county}.",
        5: "Retrieving data for Parcel ID number: {parcel_id}...",
        6: "Data retrieved for Parcel ID number: {parcel_id}.",
        7: "User Inputs Cleared.",
        8: "Data unavailable for County: {county}.",
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
            self.update_info_label(8, county=county)
            return False
        return True

    def open_parcel_websites(self):
        parcel_id = self.inputs["Parcel ID"].get()
        county = self.inputs["County"].get()
        if not self.validate_parcel_inputs(parcel_id, county):
            return

        try:
            parcel_data = self.get_parcel_data(parcel_id, county)
        except IndexError:
            return

        links_to_open = {"PROPERTY_APPRAISER", "DEED", "MAP", "PLAT", "FEMA"}

        for link_name, link in parcel_data["LINKS"].items():
            if link_name in links_to_open and link != "":
                webbrowser.open(link, new=2, autoraise=True)

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
            self.update_info_label(6, parcel_id=parcel_id)
        except IndexError:
            self.update_info_label(4, parcel_id=parcel_id, county=county)
            raise IndexError
        return parcel_data

    def clear_inputs(self) -> None:
        """Clears all the input fields."""
        for input_field in self.inputs.values():
            input_field.delete(0, "end")
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
