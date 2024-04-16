from tkinter import TclError

import pytest

from DatabaseManager.main import MainApp
from DatabaseManager.views.cad_opener import CADOpenerView
from DatabaseManager.views.close_job_search import CloseJobSearchView
from DatabaseManager.views.file_entry import FileEntryView
from DatabaseManager.views.file_status_checker import FileStatusCheckerView
from DatabaseManager.views.intake_sheet import IntakeSheetView
from DatabaseManager.views.website_search import WebsiteSearchView

from typing import Generator


@pytest.fixture(scope="module")
def test_address() -> str:
    """Fixture to get a test address.

    Returns:
        str: The test address.
    """
    return "1234 main street"


@pytest.fixture(scope="module")
def test_subdivision() -> str:
    """Fixture to get a test subdivision.

    Returns:
        str: The test subdivision.
    """
    return "Whitakers Landing"


@pytest.fixture(scope="module")
def test_file_number() -> str:
    """Fixture to get a test file number.

    Returns:
        str: The test file number.
    """
    return "23050226"


@pytest.fixture(scope="module")
def test_sarasota_parcel_id() -> str:
    """Fixture to get a test parcel id.

    Returns:
        str: The test parcel id.
    """
    return "0057150069"


@pytest.fixture(scope="module")
def test_file_data() -> dict[str, str]:
    """Fixture to get a test file data.

    Returns:
        dict[str, str]: The test file data.
    """
    fields = {
        "Job Date": "",
        "Job Number": "23060232",
        "Parcel ID": "7880000000",
        "County": "Manatee",
        "Property Address": "741 Emerald Harbor Drive",
        "Lot": "50",
        "Block": "",
        "Subdivision": "Dream Island",
    }
    return fields


@pytest.fixture(scope="module")
def test_file_entry_data() -> dict[str, str]:
    """Fixture to get a test file entry data.

    Returns:
        dict[str, str]: The test file entry data.
    """
    fields = {
        "Job Date": "2021-01-01",
        "Fieldwork Date": "2021-01-01",
        "Inhouse Date": "2021-01-01",
        "Job Number": "50050101",
        "Parcel ID": "0057150069",
        "County": "Sarasota",
        "Entry By": "TEST",
        "Fieldwork Crew": "CREW",
        "Inhouse Assigned To": "ASSIGNED",
        "Requested Services": "SURVEY",
        "Contact Information": "CONTACT",
        "Additional Information": "ADDITIONAL",
    }
    return fields


@pytest.fixture(scope="module")
def main_app() -> Generator[MainApp, None, None]:
    """Fixture to get the main app.

    Yields:
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
def close_job_tab(
    main_app: MainApp,
) -> Generator[CloseJobSearchView, None, None]:
    """Fixture to get the close job tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Yields:
        CloseJobSearchView: The close job tab.
    """
    tab = main_app.notebook_tabs["Close Job Search"]
    yield tab
    tab.destroy()


@pytest.fixture(scope="module")
def file_status_tab(
    main_app: MainApp,
) -> Generator[FileStatusCheckerView, None, None]:
    """Fixture to get the file status tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Yields:
        FileStatusCheckerView: The file status tab.
    """
    tab = main_app.notebook_tabs["File Status"]
    yield tab
    tab.destroy()


@pytest.fixture(scope="module")
def file_entry_tab(main_app: MainApp) -> Generator[FileEntryView, None, None]:
    """Fixture to get the file entry tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Yields:
        FileEntryView: The file entry tab.
    """
    tab = main_app.notebook_tabs["File Entry"]
    yield tab
    tab.destroy()


@pytest.fixture(scope="module")
def intake_sheet_tab(main_app: MainApp) -> IntakeSheetView:
    """Fixture to get the intake sheet tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Yields:
        IntakeSheetView: The intake sheet tab.
    """
    tab = main_app.notebook_tabs["Intake Sheet"]
    yield tab
    tab.destroy()
