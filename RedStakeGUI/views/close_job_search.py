import ttkbootstrap as ttk
from ..models.close_job_search import CloseJobSearchModel
from .base_view import BaseView


class CloseJobSearchView(BaseView):
    """This class will be used to create a close job search form for the
    user to find nearby surveys that can be referenced for the current
    job. It can also be used as a simple lookup tool for any existing
    survey in our database.

    Args:
        BaseView (BaseView): The base view class.
    """

    GEOMETRY = (500, 300)

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master
        self.header = "Close Job Search"
        self.create_header()

        self.inputs = {"Search Type": None, "Search Keyword": None}
        self.dropdowns = {"Search Type": ("Street Name", "Subdivision Name")}
        self.create_fields()
        self.inputs["Search Type"].current(0)

        self.info_label = self.create_status_info_label()
        self.model = CloseJobSearchModel(self)

        self.buttons = {
            "Search": self.model.create_search_treeview,
            "Clear": self.model.clear_inputs,
            "Copy Selection": self.model.copy_selected_rows,
        }
        self.create_buttons()
