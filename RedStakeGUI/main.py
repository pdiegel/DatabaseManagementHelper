import logging

import sv_ttk
import ttkbootstrap as ttk

from .views.intake_sheet import IntakeSheetView


class MainApp(ttk.Window):
    """This class will be used as the main application window. It will
    contain a ttk.Notebook widget that will contain all the other
    widgets. Inherits from ttk.Window."""

    def __init__(self):
        super().__init__()
        self.title("Red Stake Surveyors, Inc.")
        self.notebook = self.create_notebook()
        self.resizable(False, False)

        sv_ttk.set_theme("light")

    def create_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.insert("end", IntakeSheetView(notebook), text="Intake Sheet")
        notebook.pack(expand=True, fill="both")
        return notebook


if __name__ == "__main__":
    logging.basicConfig(filename="gui.log", level=logging.INFO)
    app = MainApp()
    app.mainloop()
