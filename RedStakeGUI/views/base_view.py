import ttkbootstrap as ttk


class BaseView(ttk.Frame):
    def __init__(
        self,
        master: ttk.Notebook = None,
        dropdowns: dict = None,
        buttons: dict = None,
        model: object = None,
        header: str = None,
        **kwargs,
    ):
        super().__init__()
        self.master = master
        self.header = header
        self.inputs = {}
        self.dropdowns = dropdowns
        self.buttons = buttons
        if model:
            self.model = model(**kwargs)
        else:
            self.model = None
        self.pack()

    def create_header(self, font: str = "Helvetica 16 bold") -> None:
        """This method will create the header for the intake sheet.

        Args:
            font (str, optional): The font for the header. Defaults to
                "Helvetica 16 bold".
        """
        ttk.Label(self, text=self.header, font=font).pack(pady=10)

    def create_sheet_fields(self, field_width: int = 25) -> None:
        """This method will create the fields for the intake sheet. It
        will read the labels from the intake_labels.txt file and create
        a ttk.Entry widget for each label.

        Args:
            field_width (int): The width of the entry fields.
                Defaults to 25.
        """
        for label in self.inputs:
            if label in self.dropdowns:
                self.create_dropdown_field(label, field_width)
                continue
            self.create_label_entry_field(label, field_width)

    def create_status_info_label(self) -> ttk.Label:
        """This method will create a label to display status information
        to the user.

        Returns:
            ttk.Label: The label to display status information.
        """
        info_label = ttk.Label(self, text="")
        info_label.pack(pady=5, anchor="center")
        return info_label

    def create_buttons(self) -> None:
        """This method will create the buttons for the intake sheet."""

        button_row = ttk.Frame(self)
        for button_label, button_function in self.buttons.items():
            ttk.Button(
                button_row, text=button_label, command=button_function
            ).pack(side="left", padx=5, pady=5)
        button_row.pack(expand=True, fill="x", pady=5)

    def create_dropdown_field(self, label: str, field_width: int) -> None:
        """This method will create a dropdown menu for the intake sheet.

        Args:
            label (str): The label for the dropdown menu.
            field_width (int): The width of the entry fields.
        """
        dropdown_row = ttk.Frame(self)
        ttk.Label(dropdown_row, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )
        self.inputs[label] = ttk.Combobox(
            dropdown_row,
            values=self.dropdowns[label],
            width=field_width - 4 if field_width > 4 else 5,
        )
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        dropdown_row.pack(expand=True, fill="x", padx=10, pady=5)

    def create_label_entry_field(self, label: str, field_width) -> None:
        """This method will create a label and entry field for the
        intake sheet.

        Args:
            label (str): The label for the entry field.
            field_width (int): The width of the entry fields.
        """
        label_row = ttk.Frame(self)
        ttk.Label(label_row, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )
        self.inputs[label] = ttk.Entry(label_row, width=field_width)
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        label_row.pack(expand=True, fill="x", padx=10, pady=5)
