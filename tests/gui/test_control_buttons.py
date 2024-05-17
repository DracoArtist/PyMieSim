from pytest import raises
import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI


"""
This file contains tests that make sure the control buttons (calculate, save as csv, export plot and reset std-axis) work as intended
"""

root = tkinter.Tk()
root.geometry("750x600")
gui = PyMieSimGUI(root)



def test_graphExists():
    """
    This function will test for all combination of x, y and std axis if there is a graph produced

    Missing: all the button combination
    """
    for tab in gui.scatterer_tab.type_widget['values']:
        gui.scatterer_tab.type_widget.set(tab)
        gui.scatterer_tab.on_type_change()
        widgets = gui.scatterer_tab.widget_collection.widgets

        for widget in widgets:
            widget.tk_radio_button_1.invoke()

            with raises(Exception):
                gui.calculate_button.invoke()


def all_combination_XandStd():
    source_widgets = gui.source_tab.widget_collection.widgets

    for scatter_tab in gui.scatterer_tab.type_widget['values']:
        gui.scatterer_tab.type_widget.set(scatter_tab)
        gui.scatterer_tab.on_type_change()
        scatter_widgets = gui.scatterer_tab.widget_collection.widgets

        for detector_tab in gui.detector_tab.type_widget['values']:
            gui.detector_tab.type_widget.set(detector_tab)
            gui.detector_tab.on_type_change()
            detector_widgets = gui.detector_tab.widget_collection.widgets

            all_widgets = [*source_widgets, *scatter_widgets, *detector_widgets]# The widgets it is possible to choose from for the std and x axis

            possible_widgets = []
            for widget in all_widgets:
                if widget.can_be_axis == True:
                    possible_widgets.append(widget)

    return 1

all_combination_XandStd()

