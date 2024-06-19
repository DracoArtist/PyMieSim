from pytest import raises
from unittest.mock import patch
import tkinter
from tkinter.ttk import Notebook
from PyMieSim.gui.main_window import PyMieSimGUI
import PyMieSim


def test():
    root = tkinter.Tk()
    root.geometry("750x600")
    gui = PyMieSimGUI(root)
