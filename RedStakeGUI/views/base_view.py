from tkinter import Listbox
from typing import Callable, Dict, List

import ttkbootstrap as ttk


class BaseView(ttk.Frame):
    HEADER_FONT = "Helvetica 16 bold"

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

    def create_status_info_label(self) -> ttk.Label:
        """Creates a label to display status information to the user.

        Returns:
            ttk.Label: The label to display status information.
        """
        info_label = self.create_widget("Label", self)
        info_label.pack(pady=5, anchor="center")
        return info_label

    def create_buttons(self) -> None:
        """Creates the buttons for the view."""
        row_frame = ttk.Frame(self)

        for button_label, button_function in self.buttons.items():
            self.create_widget(
                "Button", row_frame, text=button_label, command=button_function
            ).pack(side="left", padx=5, pady=5)

        row_frame.pack(expand=True, fill="x", pady=5)

    def create_dropdown_field(
        self, label: str, width: int = 23, **kwargs
    ) -> None:
        """Creates a dropdown menu for the view.

        Args:
            label (str): The label for the dropdown menu.
            width (int): The width of the dropdown menu. Defaults to 23.
        """
        row_frame = ttk.Frame(self)
        self.create_widget("Label", row_frame, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )

        self.inputs[label] = self.create_widget(
            "Combobox", row_frame, width=width, **kwargs
        )
        self.inputs[label].pack(side="left", anchor="e")
        row_frame.pack(fill="x", padx=10, pady=5)

    def create_label_entry_field(
        self, label: str, width: int = 25, **kwargs
    ) -> None:
        """Creates a label and entry field for the view.

        Args:
            label (str): The label for the entry field.
            width (int): The width of the entry field. Defaults to 25.
        """
        row_frame = ttk.Frame(self)
        self.create_widget("Label", row_frame, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )

        self.inputs[label] = self.create_widget(
            "Entry", row_frame, width=width, **kwargs
        )
        self.inputs[label].pack(side="left", anchor="e")
        row_frame.pack(fill="x", padx=5, pady=5)

    def create_date_field(self, label: str, **kwargs) -> None:
        """Creates a label and date field for the view.

        Args:
            label (str): The label for the date field.
        """
        row_frame = ttk.Frame(self)
        self.create_widget("Label", row_frame, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )

        self.inputs[label] = self.create_widget(
            "DateEntry", row_frame, **kwargs
        )
        self.inputs[label].pack(side="left", anchor="e")
        row_frame.pack(fill="x", padx=10, pady=5)

    def create_listbox(
        self,
        label: str = "ListBox",
        height: int = 5,
        header_text: str = "",
        **kwargs,
    ) -> None:
        """Creates a listbox widget for the view.

        Args:
            label (str, optional): The label for the listbox. Defaults to
                "ListBox".
            height (int, optional): The height of the listbox. Defaults
                to 5.
        """
        if header_text:
            self.create_widget("Label", self, text=header_text).pack()

        self.inputs[label] = self.create_widget(
            "Listbox", self, height=height, **kwargs
        )
        self.inputs[label].pack(expand=True, fill="both", padx=10, pady=5)

    def create_widget(
        self, widget_type: str, parent_frame: ttk.Frame, **kwargs
    ) -> ttk.Widget:
        """Creates a widget based on the widget type. The widget type
        can be one of the following: Label, Entry, Button, Combobox,
        DateEntry, Listbox.

        Args:
            widget_type (str): The type of widget to create.
            parent_frame (ttk.Frame): The parent frame for the widget.

        Raises:
            ValueError: If the widget type is not one of the following:
                Label, Entry, Button, Combobox, DateEntry, Listbox.

        Returns:
            ttk.Widget: The widget object.
        """
        if widget_type == "Label":
            return ttk.Label(parent_frame, **kwargs)
        elif widget_type == "Entry":
            return ttk.Entry(parent_frame, **kwargs)
        elif widget_type == "Button":
            return ttk.Button(parent_frame, **kwargs)
        elif widget_type == "Combobox":
            kwargs["width"] = kwargs.get("width", 25) - 2
            return ttk.Combobox(parent_frame, **kwargs)
        elif widget_type == "DateEntry":
            return ttk.DateEntry(parent_frame, **kwargs)
        elif widget_type == "Listbox":
            return Listbox(parent_frame, **kwargs)
        else:
            raise ValueError(f"Unknown widget type: {widget_type}")

    def create_field(
        self, label: str, field_type: str, field_width: int = 25, **kwargs
    ):
        row_frame = ttk.Frame(self)
        ttk.Label(row_frame, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )
        self.inputs[label] = self.create_widget(
            field_type, row_frame, width=field_width, **kwargs
        )
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        row_frame.pack(expand=True, fill="x", padx=10, pady=5)
