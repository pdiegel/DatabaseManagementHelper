import ttkbootstrap as ttk
from ..constants import ACCESS_DATABASE
from thefuzz import process, fuzz
import pyperclip


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
        self.initial_geometry = self.view_frame.GEOMETRY
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

        if search_type == "Street Name":
            choices = jobs_df["Property Address"]
        else:
            choices = jobs_df["Subdivision"]

        results = process.extract(
            search_keyword, choices, limit=500, scorer=fuzz.WRatio
        )

        filtered_results = [result[0] for result in results if result[1] > 80]

        # Get the corresponding rows in the DataFrame
        if search_type == "Street Name":
            matched_rows = jobs_df[
                jobs_df["Property Address"].isin(filtered_results)
            ]
        else:
            matched_rows = jobs_df[
                jobs_df["Subdivision"].isin(filtered_results)
            ]

        # Remove duplicates
        matched_rows = matched_rows.drop_duplicates()
        self.update_info_label(1, num_results=len(matched_rows))

        # Convert the DataFrame to a list of dictionaries
        return matched_rows.to_dict("records")

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
        tree.heading(
            "Job Number",
            text="Job Number",
            anchor="w",
            command=lambda: self.sort_treeview(tree, "Job Number", False),
        )
        tree.heading(
            "Property Address",
            text="Property Address",
            anchor="w",
            command=lambda: self.sort_treeview(tree, "Property Address", False),
        )
        tree.heading(
            "Subdivision",
            text="Subdivision",
            anchor="w",
            command=lambda: self.sort_treeview(tree, "Subdivision", False),
        )
        tree.heading(
            "Lot",
            text="Lot",
            anchor="w",
            command=lambda: self.sort_treeview(tree, "Lot", False),
        )
        tree.heading(
            "Block",
            text="Block",
            anchor="w",
            command=lambda: self.sort_treeview(tree, "Block", False),
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
        self.update_view_geometry(600, 500)

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
        self.update_view_geometry(*self.initial_geometry)

    def update_view_geometry(self, width: int, height: int) -> None:
        """Updates the view geometry.

        Args:
            width (int): The width of the view.
            height (int): The height of the view.
        """
        self.view_frame.master.master.geometry(f"{width}x{height}")

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

        rows = [self.tree.item(row)["values"] for row in selection_index]
        return rows
