import ttkbootstrap as ttk

from ..constants import get_email_settings, save_email_settings


class EmailSettings(ttk.Toplevel):
    """This class will be used to create a window that will allow the
    user to enter their email settings. Inherits from ttk.Window."""

    INFO_LABEL_CODES = {
        1: "Settings saved successfully.",
        2: "Settings not saved. Please try again.",
        3: "Please enter all fields.",
    }

    def __init__(self, model: object):
        super().__init__()
        self.model = model
        self.title("Email Settings")
        self.resizable(False, False)
        self.sender, self.receiver, self.password = get_email_settings()
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

    def create_window_content(self):
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
        if self.inputs["Sender Email Address"].get() == "":
            self.update_info_label(3)
            return

        if self.inputs["Sender Password"].get() == "":
            self.update_info_label(3)
            return

        if self.inputs["Receiver Email Address"].get() == "":
            self.update_info_label(3)
            return

        sender = self.inputs["Sender Email Address"].get()
        sender_password = self.inputs["Sender Password"].get()
        receiver = self.inputs["Receiver Email Address"].get()

        try:
            save_email_settings(sender, sender_password, receiver)
            self.update_info_label(1)
        except Exception as e:
            self.update_info_label(2)
            print(e)

    def update_info_label(self, code: int, **kwargs) -> None:
        """Updates the info label with the text from the
        INFO_LABEL_CODES dictionary.

        Args:
            code (int): The code for the text to be displayed in the
                info label.
            **kwargs: The format keyword arguments for the text to be
                displayed in the info label.

        """
        text = self.INFO_LABEL_CODES[code].format(**kwargs)
        self.info_label.config(text=text)

    def destroy(self) -> None:
        """Destroys the email settings window.

        Returns:

        """
        self.model.reset_settings_window()
        return super().destroy()


if __name__ == "__main__":
    app = EmailSettings()
    app.mainloop()