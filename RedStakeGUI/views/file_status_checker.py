import ttkbootstrap as ttk

from RedStakeGUI.models.file_status_checker import FileStatusCheckerModel
from RedStakeGUI.views.base_view import BaseView


class FileStatusCheckerView(BaseView):
    """This class will be used to create a file status checker for the
    user to check on the status of any file number in the database.

    Args:
        BaseView (BaseView): The base view class.
    """

    def __init__(self, master: ttk.Notebook = None):
        super().__init__(master)
        self.create_header("File Status Lookup")

        # Input values will be populated in the create_fields method.
        self.inputs = {"File Number": None}

        # These inputs will not be entered by the user. They will be
        # programmatically entered by the program.
        programmable_inputs = [
            "Property Address",
            "Lot",
            "Block",
            "Subdivision",
            "Active",
            "Order Date",
            "Scope of Work",
            "Fieldwork Status",
            "Inhouse Status",
            "County",
            "Parcel ID",
            "Signed",
            "Signed Scope of Work",
            "Signature Date",
            "Signature Notes",
        ]
        self.programmable_inputs = {key: None for key in programmable_inputs}

        self.create_fields()

        # Threw this together quickly. Should probably be refactored.
        for key in self.programmable_inputs.keys():
            frame = ttk.Frame(self)
            self.create_widget("Label", frame, text=f"{key}:", width=23).pack(
                side="left", padx=10, anchor="w"
            )
            entry = self.create_widget(
                "Entry", frame, state="readonly", width=23
            )
            self.programmable_inputs[key] = entry
            entry.pack(side="left", padx=10, expand=True, fill="x", anchor="e")
            frame.pack(padx=30, pady=5, fill="x")

        # Used to display any info or error messages to the user.
        self.info_label = self.create_status_info_label()

        # Contains the backend logic for the view.
        self.model = FileStatusCheckerModel(self)

        # Keys are the button labels and values are the functions to be
        # executed when the button is clicked.
        self.buttons = {
            "Lookup File": self.model.lookup_file,
            "Clear": self.model.clear_inputs,
        }
        self.create_buttons()
