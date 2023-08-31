import ttkbootstrap as ttk
from ..constants import INTAKE_LABELS, PARCEL_DATA_COUNTIES
from ..models.intake_sheet import IntakeSheetModel


class IntakeSheetView(ttk.Frame):
    """This class will be used to create a land surveying intake sheet
    for the user to fill out. It will be used to gather information
    about the subject property so a quote can be generated. Inherits
    from ttk.Frame."""

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master

        self.dropdowns = {"County": PARCEL_DATA_COUNTIES}
        self.inputs = {}
        self.create_header()
        self.create_sheet_fields()
        self.info_label = self.create_status_info_label()

        self.model = IntakeSheetModel(self.inputs, self.info_label)
        self.buttons = {
            "Get Parcel Info": self.model.display_parcel_data,
            "Save": self.model.save_inputs,
            "Email": None,
            "Print": None,
            "Clear": self.model.clear_inputs,
            "Settings": None,
        }
        self.create_buttons()

        self.pack()

    def create_header(self) -> None:
        """This method will create the header for the intake sheet."""
        ttk.Label(self, text="Intake Sheet", font="Helvetica 16 bold").pack(
            pady=10
        )

    def create_sheet_fields(self) -> None:
        """This method will create the fields for the intake sheet. It
        will read the labels from the intake_labels.txt file and create
        a ttk.Entry widget for each label."""

        try:
            with open(INTAKE_LABELS, "r") as file:
                labels = [line.strip() for line in file]
        except FileNotFoundError:
            labels = []

        for label in labels:
            if label in self.dropdowns:
                self.create_dropdown_field(label)
                continue
            self.create_label_entry_field(label)

    def create_dropdown_field(self, label: str) -> None:
        """This method will create a dropdown menu for the intake sheet.

        Args:
            label (str): The label for the dropdown menu.
        """
        dropdown_row = ttk.Frame(self)
        ttk.Label(dropdown_row, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )
        self.inputs[label] = ttk.Combobox(
            dropdown_row, values=self.dropdowns[label], width=21
        )
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        dropdown_row.pack(expand=True, fill="x", padx=10, pady=5)

    def create_label_entry_field(self, label: str) -> None:
        """This method will create a label and entry field for the
        intake sheet.

        Args:
            label (str): The label for the entry field.
        """
        label_row = ttk.Frame(self)
        ttk.Label(label_row, text=f"{label.strip()}:").pack(
            side="left", anchor="w"
        )
        self.inputs[label] = ttk.Entry(label_row, width=25)
        self.inputs[label].pack(side="left", expand=True, anchor="e")
        label_row.pack(expand=True, fill="x", padx=10, pady=5)

    def create_status_info_label(self) -> ttk.Label:
        """This method will create a label to display status information
        to the user.

        Returns:
            ttk.Label: The label to display status information.
        """
        info_label = ttk.Label(self, text="")
        info_label.pack(pady=10, anchor="center")
        return info_label

    def create_buttons(self) -> None:
        """This method will create the buttons for the intake sheet."""

        button_row = ttk.Frame(self)
        for button_label, button_function in self.buttons.items():
            ttk.Button(
                button_row, text=button_label, command=button_function
            ).pack(side="left", padx=5, pady=5)
        button_row.pack(expand=True, fill="x", pady=5)


if __name__ == "__main__":
    sheet = IntakeSheetView()
