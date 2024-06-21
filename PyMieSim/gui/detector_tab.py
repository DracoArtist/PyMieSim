#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NoReturn
from tkinter import ttk, StringVar

from PyMieSim.experiment.detector import Photodiode, CoherentMode
from PyMieSim.gui.base_tab import BaseTab
from PyMieSim.gui.widget_collection import WidgetCollection

from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


@dataclass(kw_only=True, config=ConfigDict(arbitrary_types_allowed=True))
class DetectorTab(BaseTab):
    """
    A GUI tab for configuring the detector parameters for simulations in PyMieSim.

    Allows for the setup of detector characteristics such as numerical aperture (NA),
    angular offsets (gamma and phi), and polarization filter angle, facilitating
    the detailed configuration of the simulation's detector component.

    Attributes:
        variables (WidgetCollection): A collection of widgets for detector configuration.

    Inherited attributes:
        notebook (ttk.Notebook): The notebook widget this tab is part of.
        label (str): The label for the tab.
        frame (ttk.Frame): The frame serving as the container for the tab's contents.
        main_window: Reference to the main window of the application, if applicable.
    """

    def __post_init__(self) -> None:
        """
        Calls for BaseTab's post initialisation, and initializes the SourceTab with UI components for source configuration
        """
        super().__post_init__()
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
        self.widget_collection.clear_widgets()
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
        self.widget_collection = WidgetCollection(frame=self.frame)

        self.widget_collection.add_widgets(tab='detector_tab', component='Photodiode')

        self.widget_collection.setup_widgets(row_start=1)
        self.setup_photodiode_component()

    def setup_coherentmode_widgets(self) -> None:
        """
        Setup widgets specific to configuring a Coherent Mode detector.
        """
        self.widget_collection = WidgetCollection(frame=self.frame)

        self.widget_collection.add_widgets(tab='detector_tab', component='Coherentmode')

        self.widget_collection.setup_widgets(row_start=1)
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
        kwargs = self.widget_collection.to_component_dict()

        self.component_dict = kwargs

        self.component = Photodiode(**kwargs)

    def setup_coherentmode_component(self) -> NoReturn:
        kwargs = self.widget_collection.to_component_dict()

        self.component_dict = kwargs

        self.component = CoherentMode(**kwargs)

# -
