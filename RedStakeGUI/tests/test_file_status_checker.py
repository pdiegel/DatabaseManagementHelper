import pytest
from RedStakeGUI.views.file_status_checker import FileStatusCheckerView
from typing import Generator


@pytest.fixture(scope="module")
def setup_file_status_checker_tab(
    file_status_tab: FileStatusCheckerView, test_file_data: dict[str, str]
) -> Generator[FileStatusCheckerView, None, None]:
    """Fixture to set up the file status checker tab for testing.

    Args:
        file_status_tab (FileStatusCheckerView): The file status checker tab.
        test_file_data (dict[str, str]): The test file number.

    Yields:
        FileStatusCheckerView: The initialized file status checker tab.
    """
    file_status_tab.inputs["File Number"].insert(
        0, test_file_data["Job Number"]
    )
    yield file_status_tab
    file_status_tab.destroy()


def test_file_status_checker_lookup_file_button(
    setup_file_status_checker_tab: FileStatusCheckerView,
    test_file_data: dict[str, str],
) -> None:
    """Testing if the lookup file button works correctly.

    Args:
        setup_file_status_checker_tab (FileStatusCheckerView): The file
            status checker tab.
        test_file_number (str): The test file number.
    """
    file_status_tab = setup_file_status_checker_tab
    program_inputs = file_status_tab.programmable_inputs

    assert (
        file_status_tab.inputs["File Number"].get()
        == test_file_data["Job Number"]
    )

    file_status_tab.buttons["Lookup File"]()
    assert (
        file_status_tab.inputs["Parcel ID"].get() == test_file_data["Parcel ID"]
    )
    assert (
        program_inputs["Property Address"].get().upper()
        == test_file_data["Property Address"].upper()
    )
    assert program_inputs["Lot"].get() == test_file_data["Lot"]
    assert program_inputs["Block"].get() == test_file_data["Block"]
    assert (
        program_inputs["Subdivision"].get().upper()
        == test_file_data["Subdivision"].upper()
    )

    file_status_tab.buttons["Clear"]()
    file_status_tab.inputs["Parcel ID"].insert(0, test_file_data["Parcel ID"])

    file_status_tab.buttons["Lookup File"]()
    assert (
        file_status_tab.inputs["File Number"].get()
        == test_file_data["Job Number"]
    )
    assert (
        file_status_tab.inputs["Parcel ID"].get() == test_file_data["Parcel ID"]
    )
    assert (
        program_inputs["Property Address"].get().upper()
        == test_file_data["Property Address"].upper()
    )
    assert program_inputs["Lot"].get() == test_file_data["Lot"]
    assert program_inputs["Block"].get() == test_file_data["Block"]
    assert (
        program_inputs["Subdivision"].get().upper()
        == test_file_data["Subdivision"].upper()
    )


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
