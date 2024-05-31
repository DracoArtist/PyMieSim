from pytest import raises
import tkinter
from PyMieSim.gui.main_window import PyMieSimGUI
from unittest.mock import patch


root = tkinter.Tk()
root.geometry("750x600")
gui = PyMieSimGUI(root)



@patch('numpy.savetxt')
@patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg.draw')
def test(mock_save, mock_draw):
    widget = gui.source_tab.widget_collection.widgets[0]
    widget.tk_radio_button_1.invoke()
    gui.calculate_button.invoke()
    gui.save_button.invoke()
    assert mock_save.call_count == 1

