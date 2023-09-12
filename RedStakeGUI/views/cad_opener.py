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

    GEOMETRY = (450, 300)

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master
        self.create_header("CAD File Opener")

        self.inputs = {
            "File Number": None,
        }
        self.create_fields()

        self.info_label = self.create_status_info_label()
        self.model = CADOpenerModel(self.inputs, self.info_label)

        self.buttons = {
            "Search": self.model.display_cad_files,
            "Open": self.model.open_selected_file,
            "Clear": self.model.clear_inputs,
        }
        self.create_listbox()
        self.create_buttons()

        self.model.late_initialize()
