#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import tkinter
import itertools as it

from PyMieSim.gui.main_window import PyMieSimGUI
from PyMieSim.gui.singleton import datashelf
from PyMieSim.experiment.measure import __sphere__
from PyMieSim.gui.widget_dictonary import widget_dock
from PyMieSim.experiment.measure import __sphere__
from PyMieSim.gui.widget_dictonary import widget_dock
from unittest.mock import patch

from unittest.mock import patch


def reset_std_button(widget, gui):
    '''
    This is the function that will assert whether the reset_std_button works properly
    '''
    gui.reset_std_button.invoke()
    assert datashelf.STD_axis_label_widget.get() == 'None', f"reset button did not worlkfor {widget.tk_radio_button_2['value']} widget"



measures = ['Qsca', 'coupling']

@patch('tkinter.messagebox.showerror')
@patch('PyMieSim.gui.setup_tabs.SetUp.generate_figure')
def calculate_and_reset_button(mock_plot, mock_message_box, gui, possible_widgets):
    """
    This function ensures that the calculate button generates a graph for
    all possible x-axis values, along with some combination of random std-axis values.
    It does not test for all possible combinations of x and std axis due to computational time constraints.
    """
    for (x_widget, std_widget) in it.combinations(possible_widgets, 2):
        mock_plot.reset_mock()

        if x_widget.tk_radio_button_1['value'] == 'mode_number':
            continue

        x_widget.tk_radio_button_1.invoke()
        gui.calculate_button.invoke()

        assert mock_plot.call_count == 1, f"calculate_button with x-axis selection '{x_widget.tk_radio_button_1['value']}' did not call the draw"

        std_widget.tk_radio_button_2.invoke()
        gui.calculate_button.invoke()

        reset_std_button(widget=std_widget, gui=gui)




@pytest.mark.parametrize('y_axis_str', measures, ids=measures)
def test_in_all_combination_of_widgets(y_axis_str):
    """
    This function is meant to cycle through all combinations of tabs and generate the corresponding battery of
    widgets with which the tests should be run. It will then execute the tests for all tab combinations.
    """
    root = tkinter.Tk()
    root.geometry("750x600")
    gui = PyMieSimGUI(root)

    gui.tab_setup.axis_tab.widget_collection.widgets[0].tk_widget.set(y_axis_str)

    # The following nested for loops will create all possible widget combinations
    source_widgets = gui.tab_setup.source_tab.widget_collection

    scatt_det_combinations = it.product(widget_dock['scatterer_tab'].keys(), widget_dock['detector_tab'].keys())

    for scatterer_str, detector_str in scatt_det_combinations:
        # Set up the tabs
        gui.tab_setup.scatterer_tab.type_widget.set(scatterer_str)
        gui.tab_setup.scatterer_tab.on_type_change()

        gui.tab_setup.detector_tab.type_widget.set(detector_str)
        gui.tab_setup.detector_tab.on_type_change()

        # The widgets
        scatterer_widgets = gui.tab_setup.scatterer_tab.widget_collection
        detector_widgets = gui.tab_setup.detector_tab.widget_collection

        possible_widgets = [
            source_widgets['wavelength'],
            scatterer_widgets['medium_index'],
            detector_widgets['NA']
        ]

        calculate_and_reset_button(gui=gui, possible_widgets=possible_widgets)


    root.destroy()


test_in_all_combination_of_widgets(1)

# -
