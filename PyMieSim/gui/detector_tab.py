#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NoReturn
from tkinter import ttk, StringVar
from PyMieSim.experiment.detector import Photodiode, CoherentMode
from PyMieSim.gui.base_tab import BaseTab
from PyMieSim.gui.utils import InputWidget, WidgetCollection, ComBoxWidget


class DetectorTab(BaseTab):
    """
    A GUI tab for configuring the detector parameters for simulations in PyMieSim.

    Allows for the setup of detector characteristics such as numerical aperture (NA),
    angular offsets (gamma and phi), and polarization filter angle, facilitating
    the detailed configuration of the simulation's detector component.

    Attributes:
        variables (WidgetCollection): A collection of widgets for detector configuration.
    """

    def __init__(self, master: ttk.Notebook, label: str) -> None:
        """
        Initialize the DetectorTab with UI components to configure the detector parameters.

        Args:
            master (ttk.Notebook): The notebook widget this tab is a part of.
            label (str): The tab label.
        """
        super().__init__(master, label=label)
        self.type_button = StringVar(value='Photodiode')
        self.setup_type_combobox()
        self.setup_widgets()

    def setup_type_combobox(self) -> None:
        """
        Create and configure a combobox to select the type of detector, binding it to update UI on change.
        """
        self.type_widget = ttk.Combobox(
            self.frame,
            textvariable=self.type_button,
            values=['Photodiode', 'CoherentMode'],
            state="readonly"
        )
        self.type_widget.grid(row=0, column=0)
        self.type_widget.bind("<<ComboboxSelected>>", self.on_type_change)

    def on_type_change(self, event=None) -> NoReturn:
        """
        Handles the event triggered by a change in the selected scatterer type. It updates the UI to match
        the selected scatterer configuration.

        Args:
            event: The event that triggered this method (default is None).
        """
        detector_type = self.type_widget.get().lower()
        setup_method = getattr(self, f"setup_{detector_type}_widgets", None)
        if callable(setup_method):
            setup_method()
        else:
            raise ValueError(f"Unsupported detector type: {detector_type}")

    def setup_widgets(self) -> NoReturn:
        """
        Configures the GUI elements for the Scatterer tab based on the selected scatterer type.
        """
        detector_type = self.type_widget.get()

        match detector_type:
            case 'Photodiode':
                self.setup_photodiode_widgets()
            case 'CoherentMode':
                self.setup_coherentmode_widgets()
            case _:
                raise ValueError(f'Detector type not valid: {detector_type}')

    def setup_photodiode_widgets(self) -> None:
        """
        Setup widgets specific to configuring a Photodiode detector.
        """
        self.widget_collection = WidgetCollection(
            InputWidget(default_value='0.2, 0.3, 0.4', label='Numerical aperture (NA)', component_label='NA', frame=self.frame),
            InputWidget(default_value='0', label='Gamma [degree]', component_label='gamma_offset', frame=self.frame),
            InputWidget(default_value='0:360:200', label='Phi [degree]', component_label='phi_offset', frame=self.frame),
            InputWidget(default_value='None', label='Polarization filter [degree]', component_label='polarization_filter', frame=self.frame),
            InputWidget(default_value='500', label='Sampling', component_label='sampling', to_int=True, frame=self.frame)
        )
        self.widget_collection.row_start = 1
        self.widget_collection.setup_widgets(self.frame)
        self.setup_photodiode_component()

    def setup_coherentmode_widgets(self) -> None:
        """
        Setup widgets specific to configuring a Coherent Mode detector.
        """
        self.widget_collection = WidgetCollection(
            ComBoxWidget(label='Coupling mode', component_label='coupling_mode', options=['point', 'mean'], frame=self.frame, default_options=0),
            InputWidget(default_value='0.', label='Polarization filter [degree]', component_label='polarization_filter', frame=self.frame),
            InputWidget(default_value='0', label='Gamma [degree]', component_label='gamma_offset', frame=self.frame),
            InputWidget(default_value='180:-180:200', label='Phi [degree]', component_label='phi_offset', frame=self.frame),
            InputWidget(default_value='0.2, 0.3, 0.4', label='Numerical aperture (NA)', component_label='NA', frame=self.frame),
            InputWidget(default_value='LP01', label='Mode field', component_label='mode_number', to_float=False, frame=self.frame),
            InputWidget(default_value='500', label='Sampling', component_label='sampling', to_int=True, frame=self.frame)
        )
        self.widget_collection.row_start = 1
        self.widget_collection.setup_widgets(self.frame)
        self.setup_coherentmode_component()

    def setup_component(self, event=None) -> NoReturn:
        """
        Handles the event triggered by a change in the selected scatterer type. It updates the UI to match
        the selected scatterer configuration.

        Args:
            event: The event that triggered this method (default is None).
        """
        detector_type = self.type_button.get().lower()
        self.widget_collection.update()
        setup_method = getattr(self, f"setup_{detector_type}_component", None)
        if callable(setup_method):
            setup_method()
        else:
            raise ValueError(f"Unsupported scatterer type: {detector_type}")

    def setup_photodiode_component(self) -> NoReturn:
        self.component = Photodiode(**self.widget_collection.to_component_dict())

        self.mapping = {
            'NA': self.component.NA,
            'gamma': self.component.gamma_offset,
            'phi': self.component.phi_offset,
            'polarization_filter': self.component.polarization_filter
        }

    def setup_coherentmode_component(self) -> NoReturn:
        self.component = CoherentMode(**self.widget_collection.to_component_dict())

        self.mapping = {
            'NA': self.component.NA,
            'gamma': self.component.gamma_offset,
            'phi': self.component.phi_offset,
            'polarization_filter': self.component.polarization_filter
        }
# -
