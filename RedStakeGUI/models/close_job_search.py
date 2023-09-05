import ttkbootstrap as ttk
from ..constants import ACCESS_DATABASE


class CloseJobSearchModel:
    INFO_LABEL_CODES = {
        1: "{num_results} results found.",
        2: "Keyword and Search View Cleared.",
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
        """Searches the database for the keyword in the search keyword
        input field. The search type is determined by the search type
        input field. The search type input field is a dropdown menu
        with the options "Street Name" and "Subdivision Name". The
        search type determines which column in the database to search
        for the keyword.
        """
        search_results = self.get_search_results()
        if not search_results:
            return

    def get_search_results(self) -> list[dict]:
        """Gets the search results from the database.

        Returns:
            list[dict]: The search results from the database.
        """
        search_keyword = self.inputs["Search Keyword"].get()
        if not search_keyword:
            self.update_info_label(1, num_results=0)
            return []

    def copy_selected_rows(self) -> None:
        return

    def clear_inputs(self) -> None:
        """Clears all the input fields. Ignore the search type field."""
        input_objects = list(self.inputs.values())
        search_type_object = self.inputs["Search Type"]
        input_objects.remove(search_type_object)

        for input_field in input_objects:
            input_field.delete(0, "end")

        self.update_info_label(2)
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
        text = self.INFO_LABEL_CODES[code].format(**kwargs)
        self.info_label.config(text=text)
