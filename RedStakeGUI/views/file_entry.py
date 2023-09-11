import ttkbootstrap as ttk
from RedStakeGUI.views.base_view import BaseView
from RedStakeGUI.constants import PARCEL_DATA_COUNTIES


class FileEntryView(BaseView):
    """This class will be used to enter new jobs into the access
    database and update existing jobs. Inherits from BaseView.

    Args:
        BaseView (BaseView): The base view class.
    """

    GEOMETRY = (500, 400)

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master
        self.header = "File Entry"
        self.create_header()

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
        }
        self.dropdowns = {"County": PARCEL_DATA_COUNTIES}
        self.datefields = ["Job Date", "Fieldwork Date", "Inhouse Date"]
        self.create_fields()

        self.info_label = self.create_status_info_label()

        self.buttons = {
            "Submit": self.model.submit_job_data,
            "Generate FN": self.model.generate_fn,
            "Gather Contacts": self.model.gather_job_data,
            "Clear": self.model.clear_inputs,
        }
        self.create_listbox("Requested Services")
        self.create_listbox("Contact Information")
        self.create_listbox("Additional Information")
        self.create_buttons()

        self.model.late_initialize()
