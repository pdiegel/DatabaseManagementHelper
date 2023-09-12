import ttkbootstrap as ttk
from RedStakeGUI.constants import INTAKE_LABELS, PARCEL_DATA_COUNTIES
from RedStakeGUI.models.intake_sheet import IntakeSheetModel
from RedStakeGUI.views.base_view import BaseView
import logging


class IntakeSheetView(BaseView):
    """This class will be used to create a land surveying intake sheet
    for the user to fill out. It will be used to gather information
    about the subject property so a quote can be generated. Inherits
    from ttk.Frame.

    Args:
        BaseView (BaseView): The base view class.
    """

    GEOMETRY = (450, 700)

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        self.master = master
        self.create_header("Intake Sheet")

        self.inputs = {label: None for label in self.get_input_labels()}
        self.dropdowns = {"County": PARCEL_DATA_COUNTIES}

        self.create_fields()

        self.info_label = self.create_status_info_label()
        self.model = IntakeSheetModel(self.inputs, self.info_label)

        self.buttons = {
            "Get Parcel Info": self.model.display_parcel_data,
            "Save": self.model.save_inputs,
            "Email": self.model.email_quote,
            "Print": self.model.print_quote,
            "Clear": self.model.clear_inputs,
            "Settings": self.model.create_settings_window,
        }
        self.create_buttons()

    def get_input_labels(self) -> list[str]:
        """Reads the intake_labels.txt file and returns a list of the
        labels.

        Returns:
            list[str]: A list of the labels for the intake sheet.
        """
        try:
            with open(INTAKE_LABELS, "r") as file:
                labels = [line.strip() for line in file]
        except FileNotFoundError:
            logging.error(f"File {INTAKE_LABELS} was not found.")
        except PermissionError:
            logging.error(f"Permission denied to open {INTAKE_LABELS}.")
        except Exception as e:
            logging.error(f"Error reading {INTAKE_LABELS}: {e}")
        else:
            return labels


if __name__ == "__main__":
    sheet = IntakeSheetView()
