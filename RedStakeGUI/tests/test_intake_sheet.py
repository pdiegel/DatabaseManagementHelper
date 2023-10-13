import pytest
from RedStakeGUI.views.intake_sheet import IntakeSheetView


@pytest.fixture(scope="module")
def setup_intake_sheet_tab(
    intake_sheet_tab: IntakeSheetView, test_sarasota_parcel_id: str
) -> IntakeSheetView:
    """Fixture to set up the intake sheet tab for testing.

    Args:
        intake_sheet_tab (IntakeSheetView): The intake sheet tab.
        test_sarasota_parcel_id (str): The test parcel id.

    Yields:
        IntakeSheetView: The initialized intake sheet tab.
    """
    intake_sheet_tab.inputs["Parcel ID"].insert(0, test_sarasota_parcel_id)
    yield intake_sheet_tab
    intake_sheet_tab.destroy()


def test_intake_sheet_get_parcel_info_button(
    setup_intake_sheet_tab: IntakeSheetView, test_sarasota_parcel_id: str
) -> None:
    """Testing if the lookup file button works correctly.

    Args:
        setup_intake_sheet_tab (IntakeSheetView): The intake sheet tab.
        test_sarasota_parcel_id (str): The test parcel id.
    """
    intake_sheet_tab = setup_intake_sheet_tab
    inputs = intake_sheet_tab.inputs

    assert inputs["Parcel ID"].get() == test_sarasota_parcel_id
    assert inputs["Red Stake File Number"].get() == ""
    assert inputs["Address"].get() == ""
    assert inputs["Lot & Block"].get() == ""
    assert inputs["Plat"].get() == ""

    intake_sheet_tab.buttons["Get Parcel Info"]()

    for key, value in inputs.items():
        print(f"{key}: '{value.get()}'")
        if key in {
            "Zip Code",
            "Address",
            "Lot & Block",
            "Plat",
            "Plat Book & Page",
        }:
            assert value.get() != ""


def test_intake_sheet_clear_button(
    setup_intake_sheet_tab: IntakeSheetView,
) -> None:
    """Testing if the clear button works correctly.

    Args:
        setup_intake_sheet_tab (IntakeSheetView): The intake sheet tab.
    """
    intake_sheet_tab = setup_intake_sheet_tab
    inputs = intake_sheet_tab.inputs

    assert inputs["Parcel ID"].get() != ""

    intake_sheet_tab.buttons["Clear"]()

    for entry in inputs.values():
        assert entry.get() == ""
