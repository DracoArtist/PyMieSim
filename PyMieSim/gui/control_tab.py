from tkinter.ttk import Button, Frame
from tkinter import messagebox
import tkinter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from typing import NoReturn

from PyMieSim.gui.singleton import datashelf
from PyMieSim.experiment import Setup


class ControlButton:
    def __init__(self, frame: Frame, text: str, style: str, command: str) -> None:
        self.frame = frame
        self.text = text
        self.style = style
        self.command = command

        self.button = Button(
            self.frame,
            text=self.text,
            style=self.style,
            command=self.setup_command()
        )

    def setup_command(self):
        match self.command:
            case "calculate":
                self.calculate()

            # case "export":
            #     self.export()

            # case "save":
            #     self.save()

            # case "reset":
            #     self.reset()

    def setup_experiment(self) -> NoReturn:
        """
        Compute the B1 scattering data using either a single diameter or a range of diameters.
        """
        self.scatterer_tab.setup_component()
        self.source_tab.setup_component()
        self.detector_tab.setup_component()

        self.experiment = Setup(
            scatterer=self.scatterer_tab.component,
            source=self.source_tab.component,
            detector=self.detector_tab.component
        )

    def validate_axis_choice(self):
        if self.x_axis == self.std_axis:
            return "Warning: x-axis cannot be equal to STD-axis."

        if self.y_axis_selection != "coupling" and self.std_axis in self.detector_tab.component_dict.keys():
            return "Warning: STD-axis cannot be associated to detector if y-axis is not coupling."

        if self.y_axis_selection != "coupling" and self.x_axis in self.detector_tab.component_dict.keys():
            return "Warning: x-axis cannot be associated to detector if y-axis is not coupling."

        return True

    def calculate(self):
        # Closing all previous plots
        plt.close('all')

        # Defining the axis'
        self.x_axis = datashelf.x_axis_label_widget.get()
        self.std_axis = datashelf.STD_axis_label_widget.get()
        self.y_axis_selection = datashelf.y_axis_selection.get()

        # Checking if axis selection is valid
        validation = self.validate_axis_choice()
        if validation is not True:
            self.messagebox = messagebox.showerror(title="error", message=validation, parent=self.master)
            raise ValueError(validation)

        # Setting up the data and the components
        y_axis = datashelf.measure_map[self.y_axis_selection]

        self.setup_experiment()

        datashelf.data = self.experiment.get(y_axis)

        self.x_axis_component = self.axis_mapping[self.x_axis]

        self.STD_axis_component = None if self.std_axis == "None" else self.axis_mapping[self.std_axis]

        try:
            self.generate_figure()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def generate_figure(self):
        """
        Generates and displays the simulation results as a plot in a new window.
        """
        if hasattr(self, 'new_window'):
            self.new_window.destroy()

        # Creates a tk window for the plot
        self.new_window = tkinter.Toplevel(self.master)
        self.new_window.title("Plot Window")

        # Renders the figure
        figure = datashelf.data.plot(x=self.x_axis_component, std=self.STD_axis_component)
        figure.unit_size = (9, 4)
        figure._render_()
        datashelf.figure = figure._mpl_figure

        # Creates the canvas
        canvas = FigureCanvasTkAgg(datashelf.figure, master=self.new_window)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(canvas, self.new_window)
        canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

        # Draws the figure
        canvas.draw()
        self.toolbar.update()

# -
