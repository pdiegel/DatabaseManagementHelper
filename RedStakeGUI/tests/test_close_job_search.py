import pytest
from RedStakeGUI.views.close_job_search import CloseJobSearchView
import pyperclip


@pytest.fixture(scope="module")
def setup_close_job_search_tab(
    close_job_tab: CloseJobSearchView, test_address: str
) -> CloseJobSearchView:
    """Fixture to set up the Close Job Search tab for testing.

    Args:
        close_job_tab (CloseJobSearchView): The close job tab.

    Yields:
        CloseJobSearchView: The initialized close job tab.
    """
    close_job_tab.inputs["Search Keyword"].insert(0, test_address)
    close_job_tab.buttons["Search"]()
    yield close_job_tab


def test_close_job_search_tab_clear_button(
    close_job_tab: CloseJobSearchView, test_address: str
) -> None:
    """Testing search functionality of the clear button.

    Args:
        close_job_tab (CloseJobSearchView): The close job tab.
    """
    close_job_tab.inputs["Search Keyword"].insert(0, test_address)
    close_job_tab.buttons["Clear"]()

    assert close_job_tab.inputs["Search Keyword"].get() == ""
    assert close_job_tab.inputs["Search Type"].get() == "Property Address"

    treeview = close_job_tab.model.tree
    assert treeview is None


def test_close_job_search_tab_search_button(
    setup_close_job_search_tab: CloseJobSearchView,
) -> None:
    """Testing search functionality of the search button.

    Args:
        close_job_tab (CloseJobSearchView): The close job tab.
    """
    close_job_tab = setup_close_job_search_tab
    treeview = close_job_tab.model.tree
    treeview_items = treeview.get_children()
    num_treeview_items = len(treeview_items)

    assert treeview is not None
    assert treeview_items is not None
    assert num_treeview_items > 0


def test_close_job_search_tab_copy_selection_button(
    setup_close_job_search_tab: CloseJobSearchView,
) -> None:
    """Testing search functionality of the copy selection button.

    Args:
        close_job_tab (CloseJobSearchView): The close job tab.
    """
    close_job_tab = setup_close_job_search_tab

    treeview = close_job_tab.model.tree
    treeview_items = treeview.get_children()
    treeview.selection_set(treeview_items[0])
    selected_item = treeview.item(treeview.selection(), "values")
    print(selected_item)
    property_address = selected_item[1]
    close_job_tab.buttons["Copy Selection"]()

    assert property_address in close_job_tab.clipboard_get()

    close_job_tab.clipboard_clear()
