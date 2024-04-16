import ttkbootstrap as ttk

from DatabaseManager.constants import SETTINGS_MANAGER, load_env_vars


class EmailSettings(ttk.Toplevel):
    """This class will be used to create a window that will allow the
    user to enter their email settings. Inherits from ttk.Window."""

    INFO_LABEL_CODES = {
        1: "Settings saved successfully.",
        2: "Error: {error}. Please try again.",
        3: "Please enter all fields.",
    }

    def __init__(self, model: object):
        super().__init__()
        self.model = model
        self.title("Email Settings")
        self.resizable(False, False)
        self.settings_manager = SETTINGS_MANAGER
        load_env_vars()
        (
            self.sender,
            self.receiver,
            self.password,
        ) = self.settings_manager.get_email_settings()

        # Input values will be populated in the create_window_content method.
        # Keys are the input labels and values are the current settings.
        self.inputs = {
            "Sender Email Address": self.sender,
            "Sender Password": self.password,
            "Receiver Email Address": self.receiver,
        }

        self.buttons = {
            "Save": self.save_email_settings,
            "Cancel": self.destroy,
        }

        self.create_window_content()

    def create_window_content(self) -> None:
        """Creates the content for the email settings window."""
        for text, current_setting in self.inputs.items():
            row_frame = ttk.Frame(self)
            ttk.Label(row_frame, text=text).pack(side="left", padx=10)
            entry = ttk.Entry(row_frame, width=30)
            entry.pack(side="left", padx=10, anchor="e", expand=True)
            entry.insert(0, current_setting)
            self.inputs[text] = entry

            row_frame.pack(pady=10, fill="x", expand=True)

        for text, command in self.buttons.items():
            ttk.Button(self, text=text, command=command).pack(
                padx=10, pady=5, side="left"
            )

        self.info_label = ttk.Label(self, text="")
        self.info_label.pack(pady=10, anchor="center")

    def save_email_settings(self) -> None:
        """Saves the email settings to the settings file."""

        fields_to_check = (
            "Sender Email Address",
            "Sender Password",
            "Receiver Email Address",
        )

        for field in fields_to_check:
            if self.inputs[field].get().strip() == "":
                # Empty field found. Display error message and return.
                self.update_info_label(3)
                return

        sender = self.inputs["Sender Email Address"].get()
        sender_password = self.inputs["Sender Password"].get()
        receiver = self.inputs["Receiver Email Address"].get()

        try:
            self.settings_manager.save_email_settings(
                sender, sender_password, receiver
            )
            # Update the model with the new settings.
            self.update_info_label(1)
        except Exception as e:
            # Error saving settings. Display error message and return.
            self.update_info_label(2, error=e)

    def update_info_label(self, code: int, **kwargs) -> None:
        """Updates the info label with the text from the
        INFO_LABEL_CODES dictionary.

        Args:
            code (int): The code for the text to be displayed in the
                info label.
            **kwargs: The format arguments.
        """
        text = self.INFO_LABEL_CODES[code].format(**kwargs)
        self.info_label.config(text=text)

    def destroy(self) -> None:
        """Destroys the email settings window."""
        self.model.reset_settings_window()
        return super().destroy()


if __name__ == "__main__":
    app = EmailSettings()
    app.mainloop()
