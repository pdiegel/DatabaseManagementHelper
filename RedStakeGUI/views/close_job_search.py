import ttkbootstrap as ttk

from RedStakeGUI.models.close_job_search import CloseJobSearchModel
from RedStakeGUI.views.base_view import BaseView


class CloseJobSearchView(BaseView):
    """This class will be used to create a close job search form for the
    user to find nearby surveys that can be referenced for the current
    job. It can also be used as a simple lookup tool for any existing
    survey in our database.

    Args:
        BaseView (BaseView): The base view class.
    """

    def __init__(self, master: ttk.Notebook = None):
        super().__init__(master)
        self.create_header("Close Job Search")

        # Input values will be populated in the create_fields method.
        self.inputs = {"Search Type": None, "Search Keyword": None}

        # Dropdown values are used to determine if an input field should
        # be a dropdown or a text field.
        self.dropdowns = {
            "Search Type": ["Property Address", "Subdivision Name"]
        }
        self.create_fields()

        # Sets the default value for the dropdown to 'Property Address'.
        self.inputs["Search Type"].current(0)

        # Used to display any info or error messages to the user.
        self.info_label = self.create_status_info_label()

        # Contains the backend logic for the view.
        self.model = CloseJobSearchModel(self)

        # Keys are the button labels and values are the functions to be
        # executed when the button is clicked.
        self.buttons = {
            "Search": self.model.create_search_treeview,
            "Clear": self.model.clear_inputs,
            "Copy Selection": self.model.copy_selected_rows,
        }
        self.create_buttons()
