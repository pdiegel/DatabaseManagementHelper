import ttkbootstrap as ttk
from RedStakeGUI.models.cad_opener import CADOpenerModel
from RedStakeGUI.views.base_view import BaseView


class CADOpenerView(BaseView):
    """This class will be used to open CAD/DWG files. It will be used to
    automatically open the CAD/DWG files for the user. Inherits from
    BaseView.

    Args:
        BaseView (BaseView): The base view class.
    """

    def __init__(self, master: ttk.Notebook = None):
        super().__init__(master)
        self.create_header("CAD File Opener")

        # Input values will be populated in the create_fields method.
        self.inputs = {
            "File Number": None,
        }
        self.create_fields()

        # Used to display any info or error messages to the user.
        self.info_label = self.create_status_info_label()

        # Contains the backend logic for the view.
        self.model = CADOpenerModel(self.inputs, self.info_label)

        # Keys are the button labels and values are the functions to be
        # executed when the button is clicked.
        self.buttons = {
            "Search": self.model.display_cad_files,
            "Open": self.model.open_selected_file,
            "Clear": self.model.clear_inputs,
        }
        self.create_listbox()
        self.create_buttons()

        # Event handlers for the view when the user presses the enter key.
        self.inputs["File Number"].bind("<Return>", self.model.search_on_enter)
        self.inputs["ListBox"].bind("<Return>", self.model.open_on_enter)
