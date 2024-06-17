from PyMieSim.gui import SourceTab, ScattererTab, DetectorTab, AxisTab
from typing import Dict, NoReturn
import matplotlib.pyplot as plt
import tkinter as tk
from PyMieSim.experiment import Setup
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


@dataclass(kw_only=True, config=ConfigDict(arbitrary_types_allowed=True))
class Config:
    axis_tab: AxisTab
    source_tab: SourceTab
    scatterer_tab: ScattererTab
    detector_tab: DetectorTab
    master: tk.Tk

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

    def calculate_plot(self, x_axis_label_widget: tk.StringVar, STD_axis_label_widget: tk.StringVar) -> NoReturn:
        # Closing all previous plots
        plt.close('all')

        # Defining the axis'
        x_axis = x_axis_label_widget.get()
        std_axis = STD_axis_label_widget.get()
        y_axis_selection = self.axis_tab.get_inputs()[0]

        # Checking if axis selection is valid
        if x_axis == std_axis:
            self.messagebox1 = tk.messagebox.showerror(title="error", message="X-axis cannot be equal to STD-axis.", parent=self.master)
            raise ValueError("Warning: x-axis cannot be equal to STD-axis.")

        if y_axis_selection != "coupling" and std_axis in self.detector_tab.component_dict.keys():
            self.messagebox2 = tk.messagebox.showerror(title="error", message="STD-axis cannot be associated to detector if y-axis is not coupling.", parent=self.master)
            raise ValueError("Warning: STD-axis cannot be associated to detector if y-axis is not coupling.")

        if y_axis_selection != "coupling" and x_axis in self.detector_tab.component_dict.keys():
            self.messagebox3 = tk.messagebox.showerror(title="error", message="x-axis cannot be associated to detector if y-axis is not coupling.", parent=self.master)
            raise ValueError("Warning: x-axis cannot be associated to detector if y-axis is not coupling.")

        # Setting up the data and the components
        y_axis = self.axis_tab.measure_map[y_axis_selection]

        self.setup_experiment()

        self.data = self.experiment.get(y_axis)

        self.x_axis_component = self.axis_mapping[x_axis]

        self.STD_axis_component = None if std_axis == "None" else self.axis_mapping[std_axis]

    def generate_figure(self):
        """
        Generates and displays the simulation results as a plot in a new window.
        """
        if hasattr(self, 'new_window'):
            self.new_window.destroy()

        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Plot Window")

        figure = self.data.plot(x=self.x_axis_component, std=self.STD_axis_component)
        figure.unit_size = (9, 4)
        figure._render_()
        self.figure = figure._mpl_figure

        canvas = FigureCanvasTkAgg(self.figure, master=self.new_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(canvas, self.new_window)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas.draw()
        self.toolbar.update()

# -
