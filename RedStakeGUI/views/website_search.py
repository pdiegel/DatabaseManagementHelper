import ttkbootstrap as ttk
from RedStakeGUI.models.website_search import WebsiteSearchModel
from RedStakeGUI.constants import PARCEL_DATA_COUNTIES
from RedStakeGUI.views.base_view import BaseView


class WebsiteSearchView(BaseView):
    """This class will be used to create a website search form for the
    user to fill out. It will be used to automatically open the parcel
    websites for the user. Inherits from BaseView.

    Args:
        BaseView (BaseView): The base view class.
    """

    GEOMETRY = (450, 250)

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master
        self.create_header("Website Search")

        self.inputs = {"County": None, "Parcel ID": None}
        self.dropdowns = {"County": PARCEL_DATA_COUNTIES}
        self.create_fields()

        self.info_label = self.create_status_info_label()
        self.model = WebsiteSearchModel(self.inputs, self.info_label)

        self.buttons = {
            "Open Websites": self.model.open_parcel_websites,
            "Clear": self.model.clear_inputs,
        }
        self.create_buttons()
