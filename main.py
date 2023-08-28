import ttkbootstrap as ttk


class IntakeSheet(ttk.Frame):
    """This class will be used to create a land surveying intake sheet
    for the user to fill out. It will be used to gather information
    about the subject property so a quote can be generated. Inherits
    from ttk.Frame."""

    def __init__(self, master: ttk.Notebook = None):
        super().__init__()
        # self.master = master
        self.pack()
        self.mainloop()


if __name__ == "__main__":
    sheet = IntakeSheet()
