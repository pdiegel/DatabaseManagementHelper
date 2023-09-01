import ttkbootstrap as ttk
from ..models.website_search import WebsiteSearchModel
from ..constants import PARCEL_DATA_COUNTIES
from .base_view import BaseView


class WebsiteSearchView(BaseView):
    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master
        self.header = "Website Search"
        self.create_header()

        self.inputs = {"County": None, "Parcel ID": None}
        self.dropdowns = {"County": PARCEL_DATA_COUNTIES}
        self.create_sheet_fields(field_width=20)

        self.info_label = self.create_status_info_label()
        self.model = WebsiteSearchModel(self.inputs, self.info_label)

        self.buttons = {
            "Open Websites": self.model.open_parcel_websites,
            "Clear": self.model.clear_inputs,
        }
        self.create_buttons()
