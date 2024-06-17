from PyMieSim.gui import SourceTab, ScattererTab, DetectorTab, AxisTab
from typing import Dict, NoReturn
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from PyMieSim.experiment import Setup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PyMieSim.gui.singleton import singleton


class Config:

    def __init__(self, master):
        self.master = master
        singleton.x_axis_label_widget = tk.StringVar(value='phi_offset')
        singleton.STD_axis_label_widget = tk.StringVar(value=None)
        singleton.STD_axis_label_widget.set(None)
        singleton.scatterer_tab_name = tk.StringVar(value='Sphere')
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

    def calculate_plot(self) -> NoReturn:
        # Closing all previous plots
        plt.close('all')

        # Defining the axis'
        x_axis = singleton.x_axis_label_widget.get()
        std_axis = singleton.STD_axis_label_widget.get()
        y_axis_selection = self.axis_tab.get_inputs()[0]

        # Checking if axis selection is valid
        validation = singleton.validate_axis_choice(y_axis_selection=y_axis_selection)
        if validation is not True:
            self.messagebox = messagebox.showerror(title="error", message=validation, parent=self.master)
            raise ValueError(validation)

        # Setting up the data and the components
        y_axis = self.axis_tab.measure_map[y_axis_selection]

        self.setup_experiment()

        singleton.data = self.experiment.get(y_axis)

        self.x_axis_component = self.axis_mapping[x_axis]

        self.STD_axis_component = None if std_axis == "None" else self.axis_mapping[std_axis]

    def generate_figure(self):
        """
        Generates and displays the simulation results as a plot in a new window.
        """
        if hasattr(self, 'new_window'):
            self.new_window.destroy()

        # Creates a tk window for the plot
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Plot Window")

        # Renders the figure
        figure = singleton.data.plot(x=self.x_axis_component, std=self.STD_axis_component)
        figure.unit_size = (9, 4)
        figure._render_()
        singleton.figure = figure._mpl_figure

        # Creates the canvas
        canvas = FigureCanvasTkAgg(singleton.figure, master=self.new_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(canvas, self.new_window)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Draws the figure
        canvas.draw()
        self.toolbar.update()


# -
