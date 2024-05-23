from pytest import raises
import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch
import PyMieSim.gui.main_window


"""
This file contains tests that make sure the control buttons (calculate, save as csv, export plot and reset std-axis) work as intended
"""

root = tkinter.Tk()
root.geometry("750x600")
gui = PyMieSimGUI(root)


def in_all_tab_combination(test_function):
    """
    This function is ment to cycle trough all combinations of tabs and generate a list of widgets with which the tests should be ran
    """
    source_widgets = gui.source_tab.widget_collection.widgets[0:2]

    for scatter_tab in gui.scatterer_tab.type_widget['values']:
        gui.scatterer_tab.type_widget.set(scatter_tab)
        gui.scatterer_tab.on_type_change()
        scatter_widgets = gui.scatterer_tab.widget_collection.widgets

        for detector_tab in gui.detector_tab.type_widget['values']:
            gui.detector_tab.type_widget.set(detector_tab)
            gui.detector_tab.on_type_change()
            all_detector_widgets = gui.detector_tab.widget_collection.widgets
            detector_widgets =[widget for widget in all_detector_widgets if widget.component_label != "mean_coupling"]

            possible_widgets = [*source_widgets, *scatter_widgets, *detector_widgets] # The widgets it is possible to choose from for the std and x axis
        
            
            in_all_combinations_XandStd(test_function=test_function, widgets=possible_widgets)


def in_all_combinations_XandStd(test_function, widgets):
    """
    This function is ment to cycle trough all possible combinations of x and std axis selection within a selection of scatterer, detector and source tab, and run a test function for each of these combinations.

    The test function is definied in each individual tests, ands this function is then called.
    """
    for x_axis_widget in widgets:
        for y_axis_widget in widgets:
            test_function(x_axis_widget, y_axis_widget)

    
@patch('PyMieSim.gui.main_window.PyMieSimGUI.update_plot')
def test_calculate_button(mock):
    """
    This function will test for all combination of x, y and std axis if there is a graph produced
    """
    def check_calculate_button(x_axis_widget, y_axis_widget):
            x_axis_widget.tk_radio_button_1.invoke()
            gui.calculate_button.invoke()
            
            mock.assert_called_once()
            

            """
            try:
                y_axis_widget.tk_radio_button_2.invoke()

                with raises(Exception):
                    gui.calculate_button.invoke()
            except:
                with raises(ValueError):
                    gui.calculate_button.invoke()
"""
    in_all_tab_combination(check_calculate_button)


'''def test_save_button():
    """
    This test is designed to make sure the Save as CSV button works. It checks if there is an exception raised when calling it from inside a function

    MISSING: The test does not call the calculate button beforehand, is it a necessary step in order to export something?
    """
    def check_save_button(x_axis_widget, y_axis_widget):
            x_axis_widget.tk_radio_button_1.invoke()

            with raises(Exception):
                gui.save_button.invoke()
            
            try:
                y_axis_widget.tk_radio_button_2.invoke()

                with raises(Exception):
                    gui.save_button.invoke()
            except:
                with raises(ValueError):
                    gui.save_button.invoke()

    in_all_tab_combination(check_save_button)

def test_export_button():
    """
    This test is designed to make sure the Export Plot button works. It checks if there is an exception raised when calling it from inside a function
    """
    def check_export_button(x_axis_widget, y_axis_widget):
            x_axis_widget.tk_radio_button_1.invoke()

            with raises(Exception):
                gui.export_button.invoke()
            
            try:
                y_axis_widget.tk_radio_button_2.invoke()

                with raises(Exception):
                    gui.export_button.invoke()
            except:
                with raises(ValueError):
                    gui.export_button.invoke()

    in_all_tab_combination(check_export_button)

def test_reset_std_button():
    """
    This test is designed to make sure the Reset STD_axis button works. It checks if the STD_axis_label_widget variable of the PyMieSimGUI class gets reset to None unpon invoking the button
    """
    def check_reset_std_button(x_axis_widget, y_axis_widget):
            y_axis_widget.tk_radio_button_2.invoke()
            assert gui.STD_axis_label_widget.get() != None
            gui.reset_std_button.invoke()
            assert gui.STD_axis_label_widget.get() == None

    in_all_tab_combination(check_reset_std_button)'''