import pytest

from RedStakeGUI.main import MainApp

# pytest -s -v RedStakeGUI/tests/test_main.py


def test_notebook_tabs(main_app: MainApp) -> None:
    """Testing if the notebook tabs are created correctly.

    Args:
        main_app (MainApp): The main app.
    """
    tab_names = list(main_app.notebook_tabs.keys())
    expected_tab_names = [
        "Close Job Search",
        "File Status",
        "File Entry",
        "Intake Sheet",
        "Website Search",
        "CAD Opener",
    ]
    for tab_name in tab_names:
        assert tab_name in expected_tab_names
