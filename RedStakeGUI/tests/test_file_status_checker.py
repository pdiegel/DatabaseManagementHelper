import pytest
from RedStakeGUI.views.file_status_checker import FileStatusCheckerView


@pytest.fixture(scope="module")
def setup_file_status_checker_tab(
    file_status_tab: FileStatusCheckerView, test_file_number: str
) -> FileStatusCheckerView:
    """Fixture to set up the file status checker tab for testing.

    Args:
        file_status_tab (FileStatusCheckerView): The file status checker tab.
        test_file_number (str): The test file number.

    Yields:
        FileStatusCheckerView: The initialized file status checker tab.
    """
    file_status_tab.inputs["File Number"].insert(0, test_file_number)
    yield file_status_tab
    file_status_tab.destroy()


def test_file_status_checker_lookup_file_button(
    setup_file_status_checker_tab: FileStatusCheckerView, test_file_number: str
) -> None:
    """Testing if the lookup file button works correctly.

    Args:
        setup_file_status_checker_tab (FileStatusCheckerView): The file
            status checker tab.
        test_file_number (str): The test file number.
    """
    file_status_tab = setup_file_status_checker_tab
    program_inputs = file_status_tab.programmable_inputs

    assert file_status_tab.inputs["File Number"].get() == test_file_number

    file_status_tab.buttons["Lookup File"]()
    assert program_inputs["Property Address"].get().upper() == "7607 LINKS CT"
    assert file_status_tab.inputs["Parcel ID"].get() == "1920561105"
    assert program_inputs["Lot"].get() == "1"
    assert program_inputs["Block"].get() == ""
    assert program_inputs["Subdivision"].get().upper() == "LINKS AT PALM-AIRE"


def test_file_status_checker_clear_button(
    setup_file_status_checker_tab: FileStatusCheckerView,
) -> None:
    file_status_tab = setup_file_status_checker_tab

    file_status_tab.buttons["Clear"]()

    assert (
        file_status_tab.info_label["text"]
        == file_status_tab.model.INFO_LABEL_CODES[4]
    )

    assert file_status_tab.inputs["File Number"].get() == ""
    for entry in file_status_tab.programmable_inputs.values():
        assert entry.get() == ""
