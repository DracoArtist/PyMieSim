#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, NoReturn
import matplotlib.pyplot as plt
import tkinter
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from PyMieSim.gui import SourceTab, ScattererTab, DetectorTab, AxisTab
from PyMieSim.experiment import Setup
from PyMieSim.gui.singleton import datashelf


class SetUp:
    """
    This class is doing the setup of the notebook and tabs of the gui.

    Attributes:
        master (tk.Tk): the root of the gui
    """

    def __init__(self, master: tkinter.Tk):
        self.master = master
        datashelf.x_axis_label_widget = tkinter.StringVar(value='phi_offset')
        datashelf.STD_axis_label_widget = tkinter.StringVar(value=None)
        datashelf.STD_axis_label_widget.set(None)
        datashelf.scatterer_tab_name = tkinter.StringVar(value='Sphere')
        self.setup_notebook()

    def setup_notebook(self) -> NoReturn:
        """
        Sets up the notebook widget with tabs for Source, Scatterer, and Detector configurations.
        """
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="ewns")

        self.notebook_2 = ttk.Notebook(self.master)
        self.notebook_2.grid(row=2, column=0, sticky="ewns")

        # Create tab instances
        self.axis_tab = AxisTab(
            notebook=self.notebook_2,
            label='Axis Configuration'
        )

        self.source_tab = SourceTab(
            notebook=self.notebook,
            label='Source'
        )

        self.scatterer_tab = ScattererTab(
            notebook=self.notebook,
            label='Scatterer',
            axis_tab=self.axis_tab
        )

        self.detector_tab = DetectorTab(
            notebook=self.notebook,
            label='Detector'
        )

    @property
    def axis_mapping(self) -> Dict[str, str]:
        """
        Combines mappings from all other tabs to provide a comprehensive dictionary of available axis options.

        Returns:
            Dict[str, str]: A dictionary mapping UI labels to internal scatterer parameter names.
        """
        _axis_mapping = {}
        for tab in [self.source_tab, self.detector_tab, self.scatterer_tab]:
            _axis_mapping.update(tab.component.mapping)

        return _axis_mapping

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

    def calculate_plot(self) -> NoReturn:
        # Closing all previous plots
        plt.close('all')

        # Defining the axis'
        self.x_axis = datashelf.x_axis_label_widget.get()
        self.std_axis = datashelf.STD_axis_label_widget.get()
        self.y_axis_selection = self.axis_tab.get_inputs()[0]

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
