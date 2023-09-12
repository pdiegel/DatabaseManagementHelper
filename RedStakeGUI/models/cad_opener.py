from tkinter import Event, Listbox

import ttkbootstrap as ttk

from RedStakeGUI.models.dwg_file_opener import DWGFiles


class CADOpenerModel:
    INFO_LABEL_CODES = {
        1: "File Number {file_number} not found.",
        2: "CAD File {file_name} opened.",
        3: "{num_results} results found.",
        4: "User Interface Cleared.",
    }

    def __init__(self, inputs: dict, info_label: ttk.Label):
        self.inputs = inputs
        self.info_label = info_label

    def display_cad_files(self):
        """Searches for DWG files with the inputted job number."""
        listbox = self.inputs["ListBox"]
        file_number = self.inputs["File Number"].get().strip()
        self.clear_listbox(listbox)
        try:
            self.dwg_file = DWGFiles(file_number)
        except (ValueError, TypeError):
            self.dwg_file = None
            self.update_info_label(1, file_number=file_number)
            return

        file_dict = self.dwg_file.file_dict
        file_list = []

        for file, (date, _) in file_dict.items():
            file_list.append(f"{file} | {date}")

        sorted_file_list = self.dwg_file.sort_dwg_files(file_list)

        for _, _, _, file in sorted_file_list:
            listbox.insert("end", file)

        num_results = len(sorted_file_list)
        self.update_info_label(3, num_results=num_results)

    def open_selected_file(self) -> None:
        """Opens a DWG job in AutoCAD."""
        listbox = self.inputs["ListBox"]
        selected_index = listbox.curselection()
        if not selected_index:
            return

        selected_file = listbox.get(selected_index[0])
        file_name = selected_file.split(" | ")[0]
        self.dwg_file.open_file(selected_file)
        self.update_info_label(2, file_name=file_name)

    def clear_inputs(self) -> None:
        """Clears all the input fields."""
        for input_field in self.inputs.values():
            input_field.delete(0, "end")
        self.update_info_label(4)

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

    def clear_listbox(self, listbox_widget: Listbox) -> None:
        """Clears the specified listbox widget.

        Args:
            listbox_widget (Listbox): The listbox widget to clear.
        """
        listbox_widget.delete(0, "end")

    def search_on_enter(self, _event: Event = None) -> None:
        """Event handler for when the user presses the enter key in the
        search field.

        Args:
            _event (Event): The event object. Not used.
        """
        self.display_cad_files()

    def open_on_enter(self, _event: Event = None) -> None:
        """Event handler for when the user presses the enter key in the
        listbox field.

        Args:
            _event (Event): The event object. Not used.
        """
        self.open_selected_file()
