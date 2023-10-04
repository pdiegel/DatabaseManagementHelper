import logging
import re
from typing import Tuple

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

        # Get the choices that have a fuzzy score of 60 or better
        fuzzy_scores = [
            choice
            for choice in choices
            if self.weighted_fuzzy_score(
                search_keyword.upper(), choice.upper(), search_type
            )
            >= 70
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
        weights: Tuple[float, float, float] = (0, 0.9, 0.1),
    ) -> int:
        """Calculates the weighted fuzzy score for the search key and
        target key. The weights are used to determine how much each
        component of the fuzzy score is worth. Property Address in this case
        is worth 70% of the fuzzy score, house number is worth 20% and
        street type is worth 10%.

        Args:
            search_key (str): The search key.
            target_key (str): The target key.
            search_type (str): The search type. Either "Property Address" or
                "Subdivision".
            weights (Tuple[float, float, float], optional): The weights
                for the fuzzy score. Defaults to (0.2, 0.7, 0.1).

        Returns:
            int: The weighted fuzzy score.
        """

        # Tokenize the search and target addresses
        if search_type == "Subdivision":
            return fuzz.ratio(search_key, target_key)

        search_tokens = self.tokenize_address(search_key)
        target_tokens = self.tokenize_address(target_key)

        if search_tokens == ("", "", "") or target_tokens == ("", "", ""):
            return 0

        # Make sure both have the same number of tokens
        # (you might want more robust handling here)
        if len(search_tokens) != len(target_tokens):
            return 0

        # Calculate individual fuzzy scores for each token
        token_scores = [
            fuzz.ratio(search_tokens[i], target_tokens[i])
            for i in range(len(search_tokens))
        ]

        # Calculate the weighted score
        weighted_score = sum(
            token_scores[i] * weights[i] for i in range(len(token_scores))
        )
        weighted_score /= sum(weights)

        return weighted_score

    def tokenize_address(self, address: str) -> Tuple[str, str, str]:
        """Tokenizes the address into Property Address, house number and
        street type.

        Args:
            address (str): The address to tokenize.

        Returns:
            Tuple[str, str, str]: The Property Address, house number and
                street type.
        """

        # Handle multiple address types
        match = re.match(r"(\d*)\s*(.*?)(?=\s*\w*\s*$)(\s+\w+\s*)?$", address)
        if not match:
            return "", "", ""

        house_number, street_name, street_type = match.groups()

        symbols_to_remove = ("#", "(", ")", "-", ".", ",", ":", ";", "'")
        for symbol in symbols_to_remove:
            street_name = street_name.replace(symbol, "")

        # Handle common abbreviations
        street_type_abbr = {
            "ROAD": "RD",
            "STREET": "ST",
            "AVENUE": "AVE",
            "DRIVE": "DR",
            "LANE": "LN",
            "COURT": "CT",
            "CIRCLE": "CIR",
            "BOULEVARD": "BLVD",
            "TERRACE": "TER",
            "PLACE": "PL",
            "SQUARE": "SQ",
            "GROVE": "GRV",
            "AVN": "AVE",
        }

        if street_type:
            for key, value in street_type_abbr.items():
                street_type = street_type.upper().replace(key, value)
                if street_type not in street_type_abbr.values():
                    street_type = ""
        else:
            street_type = ""

        return house_number, street_name, street_type

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
