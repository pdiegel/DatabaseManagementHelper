import ttkbootstrap as ttk

from RedStakeGUI.constants import PARCEL_DATA_COUNTIES
from RedStakeGUI.models.file_entry import FileEntryModel
from RedStakeGUI.views.base_view import BaseView


class FileEntryView(BaseView):
    """This class will be used to enter new jobs into the access
    database and update existing jobs. Inherits from BaseView.

    Args:
        BaseView (BaseView): The base view class.
    """

    def __init__(self, master: ttk.Notebook = None):
        super().__init__(master)
        self.create_header("File Entry")

        # Input values will be populated in the create_fields method.
        self.inputs = {
            "Job Date": None,
            "Fieldwork Date": None,
            "Inhouse Date": None,
            "Job Number": None,
            "Parcel ID": None,
            "County": None,
            "Entry By": None,
            "Fieldwork Crew": None,
            "Inhouse Assigned To": None,
            "Requested Services": None,
            "Contact Information": None,
            "Additional Information": None,
        }

        # Datefields are used to determine if an input field should
        # be a date field or a text field.
        self.datefields = ["Job Date", "Fieldwork Date", "Inhouse Date"]

        # Dropdown values are used to determine if an input field should
        # be a dropdown or a text field.
        self.dropdowns = {"County": PARCEL_DATA_COUNTIES}
        self.create_fields()
        self.inputs["County"].current(0)

        # Used to display any info or error messages to the user.
        self.info_label = self.create_status_info_label()

        # Contains the backend logic for the view.
        self.model = FileEntryModel(
            inputs=self.inputs, info_label=self.info_label
        )

        # Keys are the button labels and values are the functions to be
        # executed when the button is clicked.
        self.buttons = {
            "Submit": self.model.submit_job_data,
            "Generate FN": self.model.generate_fn,
            "Gather Contacts": self.model.gather_existing_job_contacts,
            "Clear": self.model.clear_inputs,
        }
        self.create_buttons()
