from RedStakeGUI.main import MainApp
import pytest
from tkinter import TclError


# Initialization function to create an instance of your Tkinter app
@pytest.fixture(scope="module")
def main_app():
    try:
        app = MainApp()  # Initialize your Tkinter app here
    except (
        TclError
    ):  # Tkinter might raise a TclError if GUI can't be initialized
        pytest.skip("Unable to initialize Tkinter GUI")
    else:
        return app


# Test if notebook tabs are created correctly
def test_notebook_tabs(main_app):
    tab_names = list(main_app.notebook_tabs.keys())
    expected_tab_names = [
        "Close Job Search",
        "File Entry",
        "Intake Sheet",
        "Website Search",
        "CAD Opener",
    ]
    assert tab_names == expected_tab_names


def test_close_job_tab_functionality(main_app):
    tab = main_app.notebook_tabs["Close Job Search"]
    tab.inputs["Search Keyword"].insert(0, "1234 main street")
    result = tab.model.get_search_results()
    print("\n", len(result))

    assert len(result) > 0
