import ttkbootstrap as ttk


class CloseJobSearchModel:
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

    def search_for_keyword(self) -> None:
        return

    def copy_selected_rows(self) -> None:
        return

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
