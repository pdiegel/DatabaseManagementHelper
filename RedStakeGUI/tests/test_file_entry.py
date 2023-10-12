import pytest

from RedStakeGUI.views.file_entry import FileEntryView
from ttkbootstrap import Entry, Combobox, DateEntry
from RedStakeGUI.constants import ACCESS_DATABASE
from sqlalchemy import text


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


def test_file_entry_generate_fn_button(file_entry_tab: FileEntryView) -> None:
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
    file_entry_tab.model.clear_inputs()


def test_file_entry_submit_button(
    file_entry_tab: FileEntryView, test_file_entry_data: dict[str, str]
) -> None:
    """Testing if the submit button works correctly.

    Args:
        file_entry_tab (FileEntryView): The file entry tab.
        test_file_entry_data (dict[str, str]): The test file entry data.
    """
    for input, data in test_file_entry_data.items():
        gui_object = file_entry_tab.inputs[input]
        if isinstance(gui_object, Combobox):
            gui_object.current(0)
            continue
        elif isinstance(gui_object, DateEntry):
            gui_object = gui_object.entry
        gui_object.insert(0, data)

    for input, data in file_entry_tab.inputs.items():
        if input not in test_file_entry_data.keys():
            continue
        if isinstance(data, Entry):
            assert data.get() == test_file_entry_data[input]
        elif isinstance(data, Combobox):
            assert data.get() == test_file_entry_data[input]
        elif isinstance(data, DateEntry):
            assert data.entry.get() == test_file_entry_data[input]

    file_entry_tab.model.submit_job_data(commit=False)
    print(file_entry_tab.info_label.cget("text"))

    # ACCESS_DATABASE.session.flush()
    result = ACCESS_DATABASE.session.execute(
        text(
            f"SELECT * FROM [Existing Jobs] WHERE [Job Number] = \
'{test_file_entry_data['Job Number']}'",
        )
    )
    job = result.fetchone()

    assert (
        job is not None
    ), f"Job Number {test_file_entry_data['Job Number']} \
not found in the database"


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
