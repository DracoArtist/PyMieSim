from pytest import raises
import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch


root = tkinter.Tk()
root.geometry("750x600")
gui = PyMieSimGUI(root)



@patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg.draw')
def x_axis_possible(mock, widgets : list):
    #mock.reset_mock()

    for x_widget in widgets:
        x_widget.tk_radio_button_1.invoke()
        gui.calculate_button.invoke()
        count=mock.call_count
        mock.reset_mock()
        new_count=mock.call_count
        assert count != new_count, f"{x_widget.tk_radio_button_1['value']} button did not call the mock"
    
    #assert mock.call_count == len(widgets)

def test_in_all_tab_combination():
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
            
            x_axis_possible(widgets=possible_widgets)

test_in_all_tab_combination()