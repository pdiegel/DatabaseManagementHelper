import pytest

from RedStakeGUI.views.file_entry import FileEntryView
from ttkbootstrap import Entry, Combobox, DateEntry


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


def test_file_entry_generate_fn_button(file_entry_tab: FileEntryView):
    """Testing if the generate fn button works correctly.

    Args:
        file_entry_tab (FileEntryView): The file entry tab.
    """
    job_number_storage = file_entry_tab.model.job_number_storage
    current_year_job_numbers = job_number_storage.get_current_year_job_numbers()

    # Some of our file number have letters as suffixes, so we need to
    # strip the letters and convert to integers to get the largest
    # number.
    largest_job_number = max(
        map(lambda x: int(strip_non_numeric(x)), current_year_job_numbers)
    )

    assert int(job_number_storage.unused_job_number) > largest_job_number
    assert len(job_number_storage.unused_job_number) == 8

    assert file_entry_tab.inputs["Job Number"].get() == ""
    file_entry_tab.buttons["Generate FN"]()
    assert (
        file_entry_tab.inputs["Job Number"].get()
        == job_number_storage.unused_job_number
    )


def test_file_entry_submit_button(
    file_entry_tab: FileEntryView, test_file_entry_data: dict[str, str]
):
    for input, data in test_file_entry_data.items():
        gui_object = file_entry_tab.inputs[input]
        if isinstance(gui_object, Combobox):
            gui_object.current(0)
        elif isinstance(gui_object, DateEntry):
            gui_object = gui_object.entry
        gui_object.insert(0, data)

    file_entry_tab.model.submit_job_data(commit=False)
    existing_job_numbers = (
        file_entry_tab.model.job_number_storage.get_existing_job_numbers()
    )
    assert test_file_entry_data["Job Number"] in existing_job_numbers


def strip_non_numeric(string: str) -> str:
    """Strips all non-numeric characters from a string.

    Args:
        string (str): The string to strip.

    Returns:
        str: The stripped string.
    """
    numeric_string = "".join(filter(lambda x: x.isnumeric(), string))
    if string != numeric_string:
        print(f"\nString before filter: {string}")
        print(f"String after filter: {numeric_string}")
    return numeric_string


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
