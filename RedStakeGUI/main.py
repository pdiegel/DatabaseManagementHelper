import logging

import sv_ttk
import ttkbootstrap as ttk

from .constants import MAIN_TITLE
from .views.intake_sheet import IntakeSheetView
from .views.website_search import WebsiteSearchView


class MainApp(ttk.Window):
    """This class will be used as the main application window. It will
    contain a ttk.Notebook widget that will contain all the other
    widgets. Inherits from ttk.Window."""

    def __init__(self):
        super().__init__()
        self.title(MAIN_TITLE)
        self.notebook_tabs = {
            IntakeSheetView: "Intake Sheet",
            WebsiteSearchView: "Website Search",
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

        if selected_tab == 0:
            self.geometry("475x750")
        elif selected_tab == 1:
            self.geometry("350x250")


if __name__ == "__main__":
    logging.basicConfig(filename="gui.log", level=logging.INFO)
    app = MainApp()
    app.mainloop()
