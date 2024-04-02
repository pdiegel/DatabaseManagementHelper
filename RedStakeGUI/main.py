# Import the logging config before any other imports.
import RedStakeGUI.logging_config

# These sqlalchemy imports are necessary for pyinstaller integration.
import sqlalchemy_access as sa_a
import sqlalchemy_access.pyodbc as sa_a_pyodbc

import logging
from tkinter import Event

import ttkbootstrap as ttk

import RedStakeGUI.constants as constants

from RedStakeGUI.views.cad_opener import CADOpenerView
from RedStakeGUI.views.close_job_search import CloseJobSearchView
from RedStakeGUI.views.file_entry import FileEntryView
from RedStakeGUI.views.intake_sheet import IntakeSheetView
from RedStakeGUI.views.website_search import WebsiteSearchView
from RedStakeGUI.views.file_status_checker import FileStatusCheckerView


class MainApp(ttk.Window):
    """This class will be used as the main application window. It will
    contain a ttk.Notebook widget that will contain all the other
    widgets. Inherits from ttk.Window."""

    def __init__(self):
        super().__init__()
        self.title(constants.MAIN_TITLE)
        self.notebook = ttk.Notebook(self)

        logging.info("Creating notebook tabs.")
        self.notebook_tabs = {
            "Close Job Search": CloseJobSearchView(self.notebook),
            "File Status": FileStatusCheckerView(self.notebook),
            "File Entry": FileEntryView(self.notebook),
            "Intake Sheet": IntakeSheetView(self.notebook),
            "Website Search": WebsiteSearchView(self.notebook),
            "CAD Opener": CADOpenerView(self.notebook),
        }
        logging.info("Notebook tabs created.")

        logging.info("Adding tabs to notebook.")
        for label, frame in self.notebook_tabs.items():
            self.notebook.add(frame, text=label)
            logging.info(f"Added {label} tab to notebook.")
        logging.info("Tabs added to notebook.")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        logging.info("Notebook tab change event bound.")
        self.notebook.pack(fill="both", expand=True)
        logging.info("Notebook packed.")

    def on_tab_change(self, _event: Event) -> None:
        """Resizes the window to fit the selected tab. This is done
        because the window is created before the widgets are created,
        so the window is not the correct size until the widgets are
        created.

        Args:
            _event (Event): The event that triggered this function.
                Not used.
        """
        logging.info("Resizing window to fit selected tab.")
        self.update_idletasks()

        selected_tab_index = self.notebook.index(self.notebook.select())
        selected_tab_object = self.notebook_tabs[
            self.notebook.tab(selected_tab_index, "text")
        ]

        required_window_width = selected_tab_object.winfo_reqwidth() + 120
        required_window_height = selected_tab_object.winfo_reqheight() + 50
        new_geometry = f"{required_window_width}x{required_window_height}"
        self.geometry(new_geometry)
        logging.info(f"Window resized to {new_geometry}.")


if __name__ == "__main__":
    logging.info("Starting RedStakeGUI.")
    app = MainApp()
    app.mainloop()
