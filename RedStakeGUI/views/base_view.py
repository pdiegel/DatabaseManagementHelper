from tkinter import Listbox
from typing import Callable, Dict, List

import ttkbootstrap as ttk


class BaseView(ttk.Frame):
    def __init__(
        self,
        master: ttk.Notebook = None,
        inputs: Dict[str, None] = None,
        dropdowns: Dict[str, List[str]] = None,
        datefields: List[str] = None,
        buttons: Dict[str, Callable] = None,
        model: object = None,
        header: str = None,
        **kwargs,
    ):
        """This class is the base view class for all the
        other views. It contains generic methods that can be used by
        all the views. Inherits from ttk.Frame.

        Args:
            master (ttk.Notebook, optional): The root window.
                Defaults to None.
            inputs (Dict[str, None], optional): A dictionary containing
                the label names as keys and widget objects as values.
                All the widgets will be automatically created and added
                to the dictionary. Defaults to None.
            dropdowns (Dict[str, List[str]], optional): A dictionary
                containing the dropdown labels as keys and a list of
                dropdown values as values. Defaults to None.
            datefields (List[str], optional): A list of datefield
                labels. Defaults to None.
            buttons (Dict[str, Callable], optional): A dictionary
                containing the button labels as keys and callable
                functions as values. Defaults to None.
            model (object, optional): The model object to handle the
                logic for the view. Defaults to None.
            header (str, optional): The header text for the view.
                Defaults to None.
        """
        super().__init__()
        self.master = master
        self.inputs = inputs
        self.dropdowns = dropdowns
        self.datefields = datefields
        self.buttons = buttons

        if model:
            self.model = model(**kwargs)
        else:
            self.model = None
        self.header = header

        self.pack()

    def create_header(self, font: str = "Helvetica 16 bold") -> None:
        """Creates the heading text for the view.

        Args:
            font (str, optional): The font for the header. Defaults to
                "Helvetica 16 bold".
        """
        ttk.Label(self, text=self.header, font=font).pack(pady=10)

    def create_fields(self, field_width: int = 25) -> None:
        """Creates the label and entry/dropdown field rows for the view.

        Args:
            field_width (int): The width of the entry fields.
                Defaults to 25.
        """
        for label in self.inputs:
            if self.dropdowns is not None and label in self.dropdowns:
                self.create_dropdown_field(label, field_width)
                continue
            if self.datefields is not None and label in self.datefields:
                self.create_date_field(label)
                continue
            self.create_label_entry_field(label, field_width)

    def create_status_info_label(self) -> ttk.Label:
        """Creates a label to display status information to the user.

        Returns:
            ttk.Label: The label to display status information.
        """
        info_label = ttk.Label(self, text="")
        info_label.pack(pady=5, anchor="center")
        return info_label

    def create_buttons(self) -> None:
        """Creates the buttons for the view."""

        button_row = ttk.Frame(self)
        for button_label, button_function in self.buttons.items():
            ttk.Button(
                button_row, text=button_label, command=button_function
            ).pack(side="left", padx=5, pady=5)
        button_row.pack(expand=True, fill="x", pady=5)

    def create_dropdown_field(self, label: str, field_width: int) -> None:
        """Creates a dropdown menu for the view.

        Args:
            label (str): The label for the dropdown menu.
            field_width (int): The width of the dropdown menu.
        """
        dropdown_row = ttk.Frame(self)
        ttk.Label(dropdown_row, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )
        self.inputs[label] = ttk.Combobox(
            dropdown_row,
            values=self.dropdowns[label],
            width=field_width - 2 if field_width > 4 else 5,
        )
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        dropdown_row.pack(expand=True, fill="x", padx=10, pady=5)

    def create_label_entry_field(self, label: str, field_width: int) -> None:
        """Creates a label and entry field for the view.

        Args:
            label (str): The label for the entry field.
            field_width (int): The width of the entry field.
        """
        label_row = ttk.Frame(self)
        ttk.Label(label_row, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )
        self.inputs[label] = ttk.Entry(label_row, width=field_width)
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        label_row.pack(expand=True, fill="x", padx=10, pady=5)

    def create_date_field(self, label: str) -> None:
        """Creates a label and date field for the view.

        Args:
            label (str): The label for the date field.
            field_width (int): The width of the date field.
        """
        date_row = ttk.Frame(self)
        ttk.Label(date_row, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )

        self.inputs[label] = ttk.DateEntry(date_row)
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        date_row.pack(expand=True, fill="x", padx=10, pady=5)

    def create_listbox(
        self, widget_identifier: str = "ListBox", height: int = 5
    ) -> None:
        """Creates a listbox widget for the view.

        Args:
            widget_identifier (str, optional): The identifier for the
                widget. Defaults to "ListBox".
            height (int, optional): The height of the listbox. Defaults
                to 5.
        """
        self.inputs[widget_identifier] = Listbox(self, height=height)
        self.inputs[widget_identifier].pack(
            expand=True, fill="both", padx=10, pady=5
        )
