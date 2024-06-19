#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import tkinter

from PyMieSim.gui.main_window import PyMieSimGUI
from PyMieSim.gui.singleton import datashelf
from PyMieSim.experiment.measure import __sphere__

from unittest.mock import patch


def reset_std_button(widget, gui):
    '''
    This is the function that will assert whether the reset_std_button works properly
    '''
    gui.reset_std_button.invoke()
    assert datashelf.STD_axis_label_widget.get() == 'None', f"reset button did not worlkfor {widget.tk_radio_button_2['value']} widget"


@patch('DataVisual.multi_array.Array.plot')
@patch('tkinter.messagebox.showerror')
def calculate_and_reset_button(mock_messagebox, mock_plot, gui, y_axis_index, source_widgets, scatterer_widgets, detector_widgets):
    """
    This function ensures that the calculate button generates a graph for
    all possible x-axis values, along with some combination of random std-axis values.
    It does not test for all possible combinations of x and std axis due to computational time constraints.
    """

    # Axis choices from the detector tab only makes sense if the y_axis is coupling
    possible_widgets = [*source_widgets, *scatterer_widgets]
    if y_axis_index == 21:
        possible_widgets.extend(detector_widgets)

    for x_widget in possible_widgets:
        if x_widget.tk_radio_button_1['value'] == 'mode_number':
            continue
        mock_plot.reset_mock()

        x_widget.tk_radio_button_1.invoke()
        gui.calculate_button.invoke()

        assert mock_plot.call_count == 1, f"calculate_button with x-axis selection '{x_widget.tk_radio_button_1['value']}' did not call the draw"

        for position in range(3):  # This will make a test for 3 random std_axis selection (doing them all takes too much computational time)
            mock_plot.reset_mock()

            std_widget = possible_widgets[position]
            std_widget.tk_radio_button_2.invoke()
            gui.calculate_button.invoke()

            if mock_plot.call_count != 1:
                assert x_widget.tk_radio_button_1['value'] == std_widget.tk_radio_button_2['value'], f"calculate_button with x-axis selection '{x_widget.tk_radio_button_1['value']}' and std-axis \
                    selection '{std_widget.tk_radio_button_2['value']}' did not call the draw as intended"

            reset_std_button(widget=std_widget, gui=gui)


@pytest.mark.parametrize('y_axis_index', [index for index in range(len(__sphere__))], ids=__sphere__)
def test_in_all_combination_of_widgets(y_axis_index):
    """
    This function is meant to cycle through all combinations of tabs and generate the corresponding battery of
    widgets with which the tests should be run. It will then execute the tests for all tab combinations.
    """
    root = tkinter.Tk()
    root.geometry("750x600")
    gui = PyMieSimGUI(root)
    tab_setup = gui.tab_setup

    y_axis_widget = tab_setup.axis_tab.widget_collection.widgets[0]
    y_axis_widget.tk_widget.current(y_axis_index)

    # The following nested for loops will create all possible widget combinations

    source_widgets = tab_setup.source_tab.widget_collection.widgets

    for scatterer_str in tab_setup.scatterer_tab.type_widget['values']:
        tab_setup.scatterer_tab.type_widget.set(scatterer_str)
        tab_setup.scatterer_tab.on_type_change()
        scatterer_widgets = tab_setup.scatterer_tab.widget_collection.widgets

        for detector_str in tab_setup.detector_tab.type_widget['values']:
            tab_setup.detector_tab.type_widget.set(detector_str)
            tab_setup.detector_tab.on_type_change()
            all_detector_widgets = tab_setup.detector_tab.widget_collection.widgets
            detector_widgets = [widget for widget in all_detector_widgets if widget.component_label != "mean_coupling"]

            calculate_and_reset_button(
                gui=gui,
                y_axis_index=y_axis_index,
                source_widgets=source_widgets[0:2],  # Only the first two widgets can be choosen as axis.
                scatterer_widgets=scatterer_widgets[0:2],  # Only test necessary widgets to reduce computational time.
                detector_widgets=detector_widgets[0:3]  # Only test necessary widgets to reduce computational time.
            )

    root.destroy()

# -
