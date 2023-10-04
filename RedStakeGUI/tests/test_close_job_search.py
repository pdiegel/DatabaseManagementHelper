from tkinter import TclError

import pytest

from RedStakeGUI.views.close_job_search import CloseJobSearchView

# pytest -s -v RedStakeGUI/tests/test_close_job_search.py


@pytest.fixture(scope="module")
def setup_close_job_search_tab_by_address(
    close_job_tab: CloseJobSearchView, test_address: str
) -> CloseJobSearchView:
    """Fixture to set up the Close Job Search tab for testing.

    Args:
        close_job_tab (CloseJobSearchView): The close job tab.
        test_address (str): The test address.

    Yields:
        CloseJobSearchView: The initialized close job tab.
    """
    close_job_tab.inputs["Search Keyword"].insert(0, test_address)
    close_job_tab.buttons["Search"]()
    yield close_job_tab
    close_job_tab.destroy()


@pytest.fixture(scope="module")
def setup_close_job_search_tab_by_subdivision(
    close_job_tab: CloseJobSearchView, test_subdivision: str
) -> CloseJobSearchView:
    """Fixture to set up the Close Job Search tab for testing.

    Args:
        close_job_tab (CloseJobSearchView): The close job tab.
        test_subdivision (str): The subdivision to search for.

    Yields:
        CloseJobSearchView: The initialized close job tab.
    """
    close_job_tab.inputs["Search Keyword"].insert(0, test_subdivision)
    close_job_tab.inputs["Search Type"].set("Subdivision Name")
    close_job_tab.buttons["Search"]()
    yield close_job_tab
    close_job_tab.destroy()


def test_close_job_search_tab_empty_search(
    close_job_tab: CloseJobSearchView,
) -> None:
    close_job_tab.buttons["Search"]()
    treeview = close_job_tab.model.tree

    assert treeview is None


def test_close_job_search_tab_search_by_address(
    setup_close_job_search_tab_by_address: CloseJobSearchView,
) -> None:
    """Testing search functionality of the search button.

    Args:
        setup_close_job_search_tab_by_address (CloseJobSearchView):
            The close job tab.
    """
    close_job_tab = setup_close_job_search_tab_by_address

    treeview = close_job_tab.model.tree
    treeview_items = treeview.get_children()
    num_treeview_items = len(treeview_items)

    assert treeview is not None
    assert treeview_items is not None
    assert num_treeview_items > 0


def test_close_job_search_tab_search_by_subdivision(
    setup_close_job_search_tab_by_subdivision: CloseJobSearchView,
) -> None:
    """Testing search functionality of the search button.

    Args:
        setup_close_job_search_tab_by_subdivision (CloseJobSearchView):
            The close job tab.
    """
    close_job_tab = setup_close_job_search_tab_by_subdivision

    treeview = close_job_tab.model.tree
    treeview_items = treeview.get_children()
    num_treeview_items = len(treeview_items)

    assert treeview is not None
    assert treeview_items is not None
    assert num_treeview_items > 0


def test_close_job_search_tab_copy_selection_button(
    setup_close_job_search_tab_by_address: CloseJobSearchView,
) -> None:
    """Testing search functionality of the copy selection button.

    Args:
        setup_close_job_search_tab_by_address (CloseJobSearchView):
            The close job tab.
    """
    close_job_tab = setup_close_job_search_tab_by_address

    treeview = close_job_tab.model.tree
    treeview_items = treeview.get_children()
    treeview.selection_set(treeview_items[0])
    selected_item = treeview.item(treeview.selection(), "values")
    property_address = selected_item[1]
    close_job_tab.buttons["Copy Selection"]()

    assert property_address in close_job_tab.clipboard_get()
    close_job_tab.clipboard_clear()

    # Test that the clipboard is cleared after the copy button is pressed.
    # Should raise a TclError if the clipboard is empty.
    try:
        close_job_tab.clipboard_get()
        assert False
    except TclError:
        assert True


def test_close_job_search_tab_clear_button(
    setup_close_job_search_tab_by_subdivision: CloseJobSearchView,
) -> None:
    """Testing search functionality of the clear button.

    Args:
        setup_close_job_search_tab_by_subdivision (CloseJobSearchView):
            The close job tab.
    """
    close_job_tab = setup_close_job_search_tab_by_subdivision

    treeview = close_job_tab.model.tree
    assert close_job_tab.inputs["Search Keyword"].get() != ""
    assert close_job_tab.inputs["Search Type"].get() == "Subdivision Name"
    assert treeview is not None
    assert treeview.get_children()

    close_job_tab.buttons["Clear"]()
    treeview = close_job_tab.model.tree

    assert close_job_tab.inputs["Search Keyword"].get() == ""
    assert treeview is None
