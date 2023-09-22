from RedStakeGUI.main import MainApp


def test_MainApp():
    app = MainApp()
    assert app.notebook_tabs["Close Job Search"].winfo_exists()
    assert app.notebook_tabs["File Entry"].winfo_exists()
    assert app.notebook_tabs["Intake Sheet"].winfo_exists()
    assert app.notebook_tabs["Website Search"].winfo_exists()
    assert app.notebook_tabs["CAD Opener"].winfo_exists()
    assert app.notebook.winfo_exists()
    assert app.winfo_exists()
