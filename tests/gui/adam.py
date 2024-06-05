from pytest import raises
import tkinter
import sys
sys.path.append(r'/Users/lodi/Desktop/git_project/PyMieSim')
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch, MagicMock


@patch('PyMieSim.gui.main_window.PyMieSimGUI.figure.savefig')
def test_export_plot_button(mock_export):
    # setting up the environment
    root = tkinter.Tk()
    root.geometry("750x600")
    gui = PyMieSimGUI(root)

    widget = gui.source_tab.widget_collection.widgets[0]
    widget.tk_radio_button_1.invoke()
    gui.figure = MagicMock()
    gui.export_button.invoke()
    assert mock_export.call_count == 1