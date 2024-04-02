import logging
import re

import pyperclip
import ttkbootstrap as ttk
from thefuzz import fuzz

from RedStakeGUI.constants import ACCESS_DATABASE


class CloseJobSearchModel:
    INFO_LABEL_CODES = {
        1: "{num_results} results found.",
        2: "Keyword and Search cleared.",
        3: "{num_selections} rows copied to clipboard.",
    }

    GUI_TO_PARCEL_KEY_MAP = {
        "Address": "PRIMARY_ADDRESS",
        "Zip Code": "PROP_ZIP",
        "Plat": "SUBDIVISION",
    }

    def __init__(self, view: ttk.Frame):
        self.inputs = view.inputs
        self.info_label = view.info_label
        self.view_frame = view
        self.tree = None
        self.tree_scrollbar = None

        self.inputs["Search Keyword"].bind("<Return>", self.search_on_enter)

    def get_search_results(self) -> list[dict]:
        """Gets the search results from the database.

        Returns:
            list[dict]: The search results from the database.
        """
        search_keyword = self.inputs["Search Keyword"].get().strip()
        if not search_keyword:
            self.update_info_label(1, num_results=0)
            return []

        jobs_df = ACCESS_DATABASE.all_job_data
        search_type = self.inputs["Search Type"].get().strip()

        if search_type == "Property Address":
            choices = jobs_df["Property Address"]
        else:
            choices = jobs_df["Subdivision"]

        # Get the choices that have a fuzzy score of 75 or higher
        fuzzy_scores = [
            choice
            for choice in choices
            if self.weighted_fuzzy_score(
                search_keyword.upper(), choice.upper(), search_type
            )
            >= 75
        ]

        # Get the corresponding rows in the DataFrame
        if search_type == "Property Address":
            matched_rows = jobs_df[
                jobs_df["Property Address"].isin(fuzzy_scores)
            ]
        else:
            matched_rows = jobs_df[jobs_df["Subdivision"].isin(fuzzy_scores)]

        # Remove duplicates
        matched_rows = matched_rows.drop_duplicates()
        self.update_info_label(1, num_results=len(matched_rows))

        # Convert the DataFrame to a list of dictionaries
        return matched_rows.to_dict("records")

    def weighted_fuzzy_score(
        self,
        search_key: str,
        target_key: str,
        search_type: str,
    ) -> int:
        """Calculates the weighted fuzzy score for the search key and
        target key.

        Args:
            search_key (str): The search key.
            target_key (str): The target key.
            search_type (str): The search type. Either "Property Address" or
                "Subdivision".

        Returns:
            int: The weighted fuzzy score.
        """

        if search_type == "Subdivision Name":
            return fuzz.token_sort_ratio(search_key, target_key)

        standardized_address = self.standardize_address(search_key)
        standardized_target = self.standardize_address(target_key)

        return fuzz.token_sort_ratio(standardized_address, standardized_target)

    def copy_selected_rows(self) -> None:
        """Copies the selected rows from the treeview widget to the
        clipboard.
        """
        selected_rows = self.get_selected_treeview_rows()
        if not selected_rows:
            return

        # Update the info label with the number of rows copied.
        self.update_info_label(3, num_selections=len(selected_rows))

        text_to_copy = ""
        for row in selected_rows:
            # Convert any non-string values to strings and join by tab key.
            row_text = "\t".join([str(item) for item in row])
            # Extra newline at the end of the text allows for multiple copies.
            text_to_copy += row_text + "\n"

        pyperclip.copy(text_to_copy)

    def create_search_treeview(self) -> None:
        """Creates a ttk.Treeview widget for displaying the search
        results.
        """
        matched_rows = self.get_search_results()
        if not matched_rows:
            return
        self.destroy_existing_treeview()

        tree = ttk.Treeview(self.view_frame, height=15, selectmode="extended")
        tree["columns"] = (
            "Job Number",
            "Property Address",
            "Subdivision",
            "Lot",
            "Block",
        )

        tree.column("#0", width=0, stretch="NO")
        tree.column("Job Number", anchor="w", width=90)
        tree.column("Property Address", anchor="w", minwidth=150)
        tree.column("Subdivision", anchor="w", width=150)
        tree.column("Lot", anchor="w", width=40)
        tree.column("Block", anchor="w", width=40)

        tree.heading("#0", text="", anchor="w")
        for heading in tree["columns"]:
            tree.heading(
                heading,
                text=heading,
                anchor="w",
                command=lambda h=heading: self.sort_treeview(tree, h, False),
            )

        for index, row in enumerate(matched_rows):
            for key, _ in row.items():
                while "  " in row[key]:
                    row[key] = row[key].replace("  ", " ")
                row[key] = row[key].strip()
                row[key] = row[key].upper().replace("NONE", "")

            tree.insert(
                parent="",
                index="end",
                iid=index,
                text="",
                values=(
                    row["Job Number"],
                    row["Property Address"],
                    row["Subdivision"],
                    row["Lot"],
                    row["Block"],
                ),
            )

        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.view_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        self.tree_scrollbar = scrollbar
        self.tree = tree
        self.update_view_geometry()

    def clear_inputs(self) -> None:
        """Clears all the input fields. Ignore the search type field."""
        input_objects = list(self.inputs.values())
        search_type_object = self.inputs["Search Type"]
        input_objects.remove(search_type_object)

        for input_field in input_objects:
            input_field.delete(0, "end")

        self.destroy_existing_treeview()
        self.update_info_label(2)
        input_objects[0].focus()

    def destroy_existing_treeview(self) -> None:
        """Destroys the existing treeview widget."""
        if self.tree:
            self.tree.destroy()
            self.tree_scrollbar.destroy()
            self.tree = None
        self.update_view_geometry()

    def update_view_geometry(self) -> None:
        """Updates the view geometry.

        Args:
            width (int): The width of the view.
            height (int): The height of the view.
        """
        self.view_frame.master.master.on_tab_change(None)

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

    def search_on_enter(self, event) -> None:
        """Called when the user presses the enter key. Calls the search
        for keyword method.

        Args:
            event: The event object.
        """
        if event.widget == self.inputs["Search Keyword"]:
            self.create_search_treeview()

    def sort_treeview(
        self, tree: ttk.Treeview, col: str, reverse: bool
    ) -> None:
        """Sorts the treeview contents when the user clicks on a column
        heading.

        Args:
            tree (ttk.Treeview): The treeview widget.
            col (str): The column to sort.
            reverse (bool): Whether to sort in reverse order.
        """
        items = [(tree.set(key, col), key) for key in tree.get_children("")]
        items.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (_, key) in enumerate(items):
            tree.move(key, "", index)

        # Reverse sort next time
        tree.heading(
            col, command=lambda: self.sort_treeview(tree, col, not reverse)
        )

    def get_selected_treeview_rows(self) -> list:
        """Gets the selected rows from the treeview widget.

        Returns:
            list: The selected rows from the treeview widget.
        """
        if not self.tree:
            return
        selection_index = self.tree.selection()
        if not selection_index:
            return

        rows = [self.tree.item(row, "values") for row in selection_index]
        return rows

    def standardize_address(self, address: str) -> str:
        if not address:
            return ""

        split_address = address.split(" ")
        if len(split_address) > 1:
            if split_address[0].isdigit():
                address = " ".join(split_address[1:])

        address = address.replace("None", "").strip()

        while "(" in address:
            starting_point = address.index("(")
            if ")" in address:
                ending_point = address.index(")")
            else:
                ending_point = len(address) - 1
            address = (
                address[:starting_point] + " " + address[ending_point + 1 :]
            )

        while "  " in address:
            address = address.replace("  ", " ")

        string_format_abbr = {
            " ST ": " ",
            " RD ": " ",
            " DR ": " ",
            " AVE ": " ",
            " BLVD ": " ",
            " LN ": " ",
            " CT ": " ",
            " PL ": " ",
            " CIR ": " ",
            " TRL ": " ",
            " PKWY ": " ",
            " HWY ": " ",
            "N.": "NORTH",
            "S.": "SOUTH",
            "E.": "EAST",
            "W.": "WEST",
            " N ": "NORTH ",
            " S ": "SOUTH ",
            " E ": "EAST ",
            " W ": "WEST ",
            "ST.": "STREET",
            "RD.": "ROAD",
            "DR.": "DRIVE",
            "AVE.": "AVENUE",
            "BLVD.": "BOULEVARD",
            "LN.": "LANE",
            "CT.": "COURT",
            "PL.": "PLACE",
            "CIR.": "CIRCLE",
            "TRL.": "TRAIL",
            "PKWY.": "PARKWAY",
            "HWY.": "HIGHWAY",
            "EXPY.": "EXPRESSWAY",
            "#": "",
            "APT.": "APARTMENT",
            "UNIT": "APARTMENT",
            "LOT": "",
            "BLOCK": "",
            "SECTION": "",
            "TOWNSHIP": "",
            "RANGE": "",
            "SUBDIVISION": "",
            "-": "",
            "  ": " ",
            ".": "",
            ",": "",
            ":": "",
            ";": "",
            "'": "",
        }

        address = address.upper()

        for key, value in string_format_abbr.items():
            address = address.replace(key, value)

        ending_replacements = {
            " ST": " STREET",
            " RD": " ROAD",
            " DR": " DRIVE",
            " AVE": " AVENUE",
            " BLVD": " BOULEVARD",
            " LN": " LANE",
            " CT": " COURT",
            " PL": " PLACE",
            " CIR": " CIRCLE",
            " TRL": " TRAIL",
            " PKWY": " PARKWAY",
            " HWY": " HIGHWAY",
            " E": " EAST",
            " W": " WEST",
            " N": " NORTH",
            " S": " SOUTH",
            " STREET": "",
            " ROAD": "",
            " DRIVE": "",
            " AVENUE": "",
            " BOULEVARD": "",
            " LANE": "",
            " COURT": "",
            " PLACE": "",
            " CIRCLE": "",
            " TRAIL": "",
            " PARKWAY": "",
        }

        for key, value in ending_replacements.items():
            if address.endswith(key):
                address = address.replace(key, value)

        return address.strip()
