import ttkbootstrap as ttk
from RedStakeGUI.views.base_view import BaseView
from RedStakeGUI.constants import PARCEL_DATA_COUNTIES
from RedStakeGUI.models.file_entry import FileEntryModel


class FileEntryView(BaseView):
    """This class will be used to enter new jobs into the access
    database and update existing jobs. Inherits from BaseView.

    Args:
        BaseView (BaseView): The base view class.
    """

    GEOMETRY = (450, 700)

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master
        self.create_header("File Entry")

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
        self.datefields = ["Job Date", "Fieldwork Date", "Inhouse Date"]
        self.dropdowns = {"County": PARCEL_DATA_COUNTIES}
        self.create_fields()

        self.info_label = self.create_status_info_label()

        self.model = FileEntryModel(
            inputs=self.inputs, info_label=self.info_label
        )
        self.buttons = {
            "Submit": self.model.submit_job_data,
            "Generate FN": self.model.generate_fn,
            "Gather Contacts": self.model.gather_job_data,
            "Clear": self.model.clear_inputs,
        }
        self.create_buttons()
