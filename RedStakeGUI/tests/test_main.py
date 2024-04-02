from RedStakeGUI.main import MainApp

# pytest -s -v RedStakeGUI/tests/test_main.py


def test_notebook_tabs(main_app: MainApp) -> None:
    """Testing if the notebook tabs are created correctly.

    Args:
        main_app (MainApp): The main app.
    """
    # Notebook tabs are a constant.
    expected_tab_names = set(main_app.notebook_tabs.keys())
    tab_names = set(
        main_app.notebook.tab(i, "text")
        for i in range(main_app.notebook.index("end"))
    )

    assert expected_tab_names == tab_names
