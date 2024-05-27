from pytest import raises
import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch


root = tkinter.Tk()
root.geometry("750x600")
gui = PyMieSimGUI(root)






@patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg.draw')
def test_calculate_button(mock):
    scatterer_widgets = gui.scatterer_tab.widget_collection.widgets
    detector_widgets = gui.detector_tab.widget_collection.widgets
    widgets = [*scatterer_widgets, *detector_widgets]

    for x_widget in detector_widgets:
        
        x_widget.tk_radio_button_1.invoke()
        #gui.calculate_button.invoke()
       
        with raises(ValueError):
                x_widget.tk_radio_button_2.invoke()
                gui.calculate_button.invoke()

    assert mock.call_count == len(detector_widgets)

test_calculate_button()

"""
We need to also mock the data from the experiment module: There are combinations of buttons that raise errors together
"""