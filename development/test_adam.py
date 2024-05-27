from pytest import raises
import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch


root = tkinter.Tk()
root.geometry("750x600")
gui = PyMieSimGUI(root)

@patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg.draw')
def test_indexerror(mock):
    detector_widgets = gui.detector_tab.widget_collection.widgets
    std_widget = detector_widgets[3]
    std_widget.tk_radio_button_2.invoke()

    scatterer_widgets = gui.scatterer_tab.widget_collection.widgets

    error_count = 3

    for x_widget in scatterer_widgets:
        x_widget.tk_radio_button_1.invoke()
        gui.calculate_button.invoke()

        ''' try:
            gui.calculate_button.invoke()
        except:
            with raises(IndexError):
                gui.calculate_button.invoke()'''
    
    assert mock.call_count == len(scatterer_widgets)