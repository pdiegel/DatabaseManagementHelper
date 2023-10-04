from tkinter import TclError

import pytest

from RedStakeGUI.main import MainApp
from RedStakeGUI.views.cad_opener import CADOpenerView
from RedStakeGUI.views.close_job_search import CloseJobSearchView
from RedStakeGUI.views.file_entry import FileEntryView
from RedStakeGUI.views.file_status_checker import FileStatusCheckerView
from RedStakeGUI.views.intake_sheet import IntakeSheetView
from RedStakeGUI.views.website_search import WebsiteSearchView


@pytest.fixture(scope="module")
def test_address() -> str:
    """Fixture to get a test address.

    Returns:
        str: The test address.
    """
    return "1234 main street"


@pytest.fixture(scope="module")
def main_app() -> MainApp:
    """Fixture to get the main app.

    Returns:
        MainApp: The main app.
    """
    try:
        app = MainApp()  # Initialize your Tkinter app here
    except (
        TclError
    ):  # Tkinter might raise a TclError if GUI can't be initialized
        pytest.skip("Unable to initialize Tkinter GUI")
    else:
        yield app
        app.destroy()


@pytest.fixture(scope="module")
def close_job_tab(main_app: MainApp) -> CloseJobSearchView:
    """Fixture to get the close job tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Returns:
        CloseJobSearchView: The close job tab.
    """
    tab = main_app.notebook_tabs["Close Job Search"]
    return tab


@pytest.fixture(scope="module")
def file_status_tab(main_app: MainApp) -> FileStatusCheckerView:
    """Fixture to get the file status tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Returns:
        FileStatusCheckerView: The file status tab.
    """
    tab = main_app.notebook_tabs["File Status"]
    return tab
