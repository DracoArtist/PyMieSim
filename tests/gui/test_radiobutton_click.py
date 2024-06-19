#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pytest import raises
import tkinter as tk
from PyMieSim.gui.main_window import PyMieSimGUI
from PyMieSim.gui.singleton import datashelf
from unittest.mock import patch


def set_up_gui(foo):
    """
    This is a decorator that will set up the gui, run the function and destroy the gui
    """
    def set_up():
        root = tk.Tk()
        root.geometry("750x600")
        gui = PyMieSimGUI(root)

        foo(tab_setup=gui.tab_setup, gui=gui)

        root.destroy()

    return set_up


@patch('tkinter.messagebox.showerror')
def radio_button_invoke(mock, widgets: list, gui) -> None:
    for widget in widgets:
        if widget.can_be_axis:
            # Defining the radiobuttons
            radio_button_x_axis = widget.tk_radio_button_1
            radio_button_STD_axis = widget.tk_radio_button_2

            # The first part of the loop makes sure the buttons work individually
            # Checks if the x-axis radiobuttons work
            radio_button_x_axis.invoke()
            assert radio_button_x_axis['value'] == datashelf.x_axis_label_widget.get(), f"x-axis selection for the {radio_button_x_axis['value']} radio button did not work"
            datashelf.x_axis_label_widget.set(None)

            # Checks if the std-axis radiobuttons work
            radio_button_STD_axis.invoke()
            assert radio_button_STD_axis['value'] == datashelf.STD_axis_label_widget.get(), f"std-axis selection for the {radio_button_STD_axis['value']} radio button did not work"
            datashelf.x_axis_label_widget.set(None)

            # The second part of the loop checks if the correct ValueError gets raised if both selected axis are the same
            radio_button_x_axis.invoke()
            radio_button_STD_axis.invoke()
            with raises(ValueError):
                gui.update_plot()


"""
The following three tests are checking if pressing the
radio buttons of the GUI is possible and if the variables self.STD_axis_label_widget and self.STD_axis_label_widget of the PyMieSimGUI class are updated upon clicking.
"""


@set_up_gui
def test_source_widgets(tab_setup, gui) -> None:
    widgets = tab_setup.source_tab.widget_collection.widgets
    radio_button_invoke(widgets=widgets, gui=gui)


@set_up_gui
def test_scatterer_widgets(tab_setup, gui) -> None:
    for tab in tab_setup.scatterer_tab.type_widget['values']:
        tab_setup.scatterer_tab.type_widget.set(tab)
        tab_setup.scatterer_tab.on_type_change()
        widgets = tab_setup.scatterer_tab.widget_collection.widgets
        radio_button_invoke(widgets=widgets, gui=gui)


@set_up_gui
def test_detector_widgets(tab_setup, gui) -> None:
    for tab in tab_setup.detector_tab.type_widget['values']:
        tab_setup.detector_tab.type_widget.set(tab)
        tab_setup.detector_tab.on_type_change()
        widgets = tab_setup.detector_tab.widget_collection.widgets
        radio_button_invoke(widgets=widgets, gui=gui)
