import pytest
from RedStakeGUI.views.file_entry import FileEntryView


@pytest.fixture(scope="module")
def setup_file_entry_tab(
    file_entry_tab: FileEntryView,
    test_file_number: str,
    test_sarasota_parcel_id: str,
) -> FileEntryView:
    """Fixture to set up the file entry tab for testing.

    Args:
        file_entry_tab (FileEntryView): The file entry tab.
        test_file_number (str): The test file number.
        test_sarasota_parcel_id (str): The test parcel id.

    Yields:
        FileEntryView: The initialized file entry tab.
    """
    file_entry_tab.inputs["Job Number"].insert(0, test_file_number)
    file_entry_tab.inputs["Parcel ID"].insert(0, test_sarasota_parcel_id)
    file_entry_tab.inputs["County"].current(0)

    yield file_entry_tab
    file_entry_tab.destroy()


# def test_file_entry_lookup_file_button(
#     setup_file_status_checker_tab: FileEntryView, test_file_number: str
# ) -> None:
#     """Testing if the lookup file button works correctly.

#     Args:
#         setup_file_status_checker_tab (FileEntryView): The file
#             status checker tab.
#         test_file_number (str): The test file number.
#     """
#     file_status_tab = setup_file_status_checker_tab
#     program_inputs = file_status_tab.programmable_inputs

#     assert file_status_tab.inputs["File Number"].get() == test_file_number

#     file_status_tab.buttons["Lookup File"]()
#     assert program_inputs["Property Address"].get().upper() == "7607 LINKS CT"
#     assert program_inputs["Parcel ID"].get() == "1920561105"
#     assert program_inputs["Lot"].get() == "1"
#     assert program_inputs["Block"].get() == ""
#     assert program_inputs["Subdivision"].get().upper() == "LINKS AT PALM-AIRE"


# def test_file_status_checker_clear_button(
#     setup_file_status_checker_tab: FileEntryView,
# ) -> None:
#     file_status_tab = setup_file_status_checker_tab

#     file_status_tab.buttons["Clear"]()

#     assert (
#         file_status_tab.info_label["text"]
#         == file_status_tab.model.INFO_LABEL_CODES[4]
#     )

#     assert file_status_tab.inputs["File Number"].get() == ""
#     for entry in file_status_tab.programmable_inputs.values():
#         assert entry.get() == ""
