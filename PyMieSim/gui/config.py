from PyMieSim.gui import SourceTab, ScattererTab, DetectorTab, AxisTab
from typing import Dict, NoReturn
import matplotlib.pyplot as plt
import tkinter as tk
from PyMieSim.experiment import Setup
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


@dataclass(kw_only=True, config=ConfigDict(arbitrary_types_allowed=True))
class Config:
    axis_tab: AxisTab
    source_tab: SourceTab
    scatterer_tab: ScattererTab
    detector_tab: DetectorTab

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

    def update_plot(self, x_axis_label_widget: tk.StringVar, std_axis_label_widget: tk.StringVar) -> NoReturn:
        # Closing all previous plots
        plt.close('all')

        # Defining the axis'
        x_axis = x_axis_label_widget.get()
        std_axis = std_axis_label_widget.get()
        y_axis = self.axis_tab.get_inputs()[0]

        # Checking if axis selection is valid
        if x_axis == std_axis:
            self.messagebox1 = tk.messagebox.showerror(title="error", message="X-axis cannot be equal to STD-axis.", parent=self.master)
            raise ValueError("Warning: x-axis cannot be equal to STD-axis.")

        if y_axis != "coupling" and std_axis in self.detector_tab.component_dict.keys():
            self.messagebox2 = tk.messagebox.showerror(title="error", message="STD-axis cannot be associated to detector if y-axis is not coupling.", parent=self.master)
            raise ValueError("Warning: STD-axis cannot be associated to detector if y-axis is not coupling.")

        if y_axis != "coupling" and x_axis in self.detector_tab.component_dict.keys():
            self.messagebox3 = tk.messagebox.showerror(title="error", message="x-axis cannot be associated to detector if y-axis is not coupling.", parent=self.master)
            raise ValueError("Warning: x-axis cannot be associated to detector if y-axis is not coupling.")

        # Setting up the data and the components
        self.y_axis = self.axis_tab.measure_map[y_axis]

        self.setup_experiment()

        self.data = self.experiment.get(self.y_axis)

        self.x_axis_component = self.axis_mapping[x_axis]

        self.STD_axis_component = None if std_axis == "None" else self.axis_mapping[std_axis]

        try:
            self.generate_figure()

        except ValueError as e:
            tk.messagebox.showerror("Input Error", str(e))

# -
