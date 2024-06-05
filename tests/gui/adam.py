from pytest import raises
import tkinter
import sys
sys.path.append(r'/Users/lodi/Desktop/git_project/PyMieSim')
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch


@patch('PyMieSim.gui.main_window.PyMieSimGUI.export_plot')
def test_export_plot_button(mock_export):
    # setting up the environment
    root = tkinter.Tk()
    root.geometry("750x600")
    gui = PyMieSimGUI(root)
