from pytest import raises
import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch


root = tkinter.Tk()
root.geometry("750x600")
gui = PyMieSimGUI(root)



@patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg.draw')
def x_axis_possible_calculate(mock, widgets : list):
    error_button_values = ['polarization_value', 'polarization_label'] #this is a list of the values of all the buttons that for which the calculate button does not work
        
    for x_widget in widgets:
        x_widget.tk_radio_button_1.invoke()
        if gui.x_axis_label_widget.get() not in error_button_values:
            mock.reset_mock()
            gui.calculate_button.invoke()
            assert mock.call_count == 1, f"{x_widget.tk_radio_button_1['value']} button did not call the mock"


@patch('numpy.savetxt')
def export_as_csv_button(mock, widgets : list):
    error_button_values = ['polarization_value', 'polarization_label'] #this is a list of the values of all the buttons that for which the calculate button does not work
        
    for x_widget in widgets:
        x_widget.tk_radio_button_1.invoke()
        if gui.x_axis_label_widget.get() not in error_button_values:
            mock.reset_mock()
            gui.save_button.invoke()
            assert mock.call_count == 1, f"{x_widget.tk_radio_button_1['value']} button did not call the mock"

def test_in_all_tab_combination():
    """
    This function is ment to cycle trough all combinations of tabs and generate a list of widgets with which the tests should be ran
    It will then pass the tests for all tab combination
    """

    # This combination of for loops will create all the possible widget combinations (this is slow. Check if it is best to separate the function in multiple fonctions without the loops)
    source_widgets = gui.source_tab.widget_collection.widgets[0:2]

    for scatter_tab in gui.scatterer_tab.type_widget['values']:
        gui.scatterer_tab.type_widget.set(scatter_tab)
        gui.scatterer_tab.on_type_change()
        scatter_widgets = gui.scatterer_tab.widget_collection.widgets

        for detector_tab in gui.detector_tab.type_widget['values'][:-1]:
            gui.detector_tab.type_widget.set(detector_tab)
            gui.detector_tab.on_type_change()
            all_detector_widgets = gui.detector_tab.widget_collection.widgets
            detector_widgets =[widget for widget in all_detector_widgets if widget.component_label != "mean_coupling"]

            possible_widgets = [*source_widgets, *scatter_widgets, *detector_widgets] # The widgets it is possible to choose from for the std and x axis
            
            # Run the tests
            #x_axis_possible_calculate(widgets=possible_widgets)
            export_as_csv_button(widgets=possible_widgets)