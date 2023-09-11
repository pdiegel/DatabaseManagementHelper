import logging

import sv_ttk
import ttkbootstrap as ttk

from RedStakeGUI.constants import MAIN_TITLE, LOG_FILE_PATH
from RedStakeGUI.views.intake_sheet import IntakeSheetView
from RedStakeGUI.views.website_search import WebsiteSearchView
from RedStakeGUI.views.cad_opener import CADOpenerView
from RedStakeGUI.views.close_job_search import CloseJobSearchView
from RedStakeGUI.views.file_entry import FileEntryView


class MainApp(ttk.Window):
    """This class will be used as the main application window. It will
    contain a ttk.Notebook widget that will contain all the other
    widgets. Inherits from ttk.Window."""

    def __init__(self):
        super().__init__()
        self.title(MAIN_TITLE)
        self.notebook_tabs = {
            CloseJobSearchView: "Close Job Search",
            IntakeSheetView: "Intake Sheet",
            WebsiteSearchView: "Website Search",
            CADOpenerView: "CAD Opener",
            FileEntryView: "File Entry",
        }
        self.notebook = self.create_notebook()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.resizable(False, False)

        sv_ttk.set_theme("light")

    def create_notebook(self) -> ttk.Notebook:
        """Creates a ttk.Notebook widget and adds it to the main window.

        Returns:
            ttk.Notebook: The ttk.Notebook widget.
        """
        notebook = ttk.Notebook(self)
        for tab_class, tab_label in self.notebook_tabs.items():
            notebook.insert("end", tab_class(notebook), text=tab_label)
        notebook.pack(expand=True, fill="both")
        return notebook

    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())

        # Get the class of the selected tab object
        notebook_tabs_keys = list(self.notebook_tabs.keys())
        new_width = notebook_tabs_keys[selected_tab].GEOMETRY[0]
        new_height = notebook_tabs_keys[selected_tab].GEOMETRY[1]
        self.geometry(f"{new_width}x{new_height}")


if __name__ == "__main__":
    logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)
    app = MainApp()
    app.mainloop()
