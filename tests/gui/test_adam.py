import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch, MagicMock
from PyMieSim.gui.singleton import singleton


@patch('tkinter.filedialog.asksaveasfilename')
@patch('tkinter.messagebox.showinfo')
def test_export_plot_button(mock_messagebox, mock_filepath):
    """
    This function tests whether the export_plot_button function is working as intended.
    """

    # setting up the environment
    root = tkinter.Tk()
    root.geometry("750x600")
    gui = PyMieSimGUI(root)

    # mocking the necessary variables
    singleton.figure = MagicMock()
    singleton.filepath = MagicMock()

    # invoking the button
    gui.export_button.invoke()

    # the assertion
    assert singleton.figure.savefig.call_count == 1

    root.destroy()
