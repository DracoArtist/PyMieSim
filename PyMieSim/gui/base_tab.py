#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import ttk
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from typing import NoReturn


@dataclass(kw_only=True, config=ConfigDict(arbitrary_types_allowed=True))
class BaseTab:
    """
    Base class for creating tabs within a notebook in a GUI application. This class provides the foundational
    structure and common functionalities needed for different tabs, including initializing the tab's frame
    and setting up basic attributes.

    Each tab is intended to be a distinct section of the GUI, capable of hosting its own set of widgets and controls.
    Subclasses of BaseTab should implement the setup_tab method to define specific layouts and behaviors.

    Attributes:
        label (str): The label of the tab, displayed in the notebook.
        frame (ttk.Frame): The frame serving as the container for the tab's contents.
        main_window: Reference to the main window of the application, if applicable.
    """
    notebook: ttk.Notebook
    label: str
    main_window = None

    def __post_init__(self):
        """
        Initializes a new tab within the provided notebook widget.

        Parameters:
            notebook (ttk.Notebook): The parent notebook widget to which this tab will be added.
            label (str): The text label for the tab.
            main_window: An optional reference to the main application window, allowing access to shared resources or controls.
        """
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text=self.label)

    def setup_tab(self) -> NoReturn:
        """
        Sets up the layout and widgets specific to this tab. This method is intended to be overridden by subclasses
        to create a customized interface for each tab.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method to set up the tab's layout and widgets.")

    def get_inputs(self) -> list:
        """
        Retrieves user inputs from all widgets in the tab.

        This method assumes that the tab contains a collection of widgets from which user inputs can be extracted.
        Subclasses should provide a mechanism to store and manage these widgets, allowing for easy retrieval of their values.

        Returns:
            list: A list of values representing the user inputs from the tab's widgets.
        """
        if hasattr(self, 'widget_collection'):
            return [widget.tk_widget.get() for widget in self.widget_collection.widgets]
        else:
            raise AttributeError("The tab does not have a widget_collection attribute.")

    def update_user_input(self) -> NoReturn:
        """
        Updates or refreshes the user inputs from the tab's widgets. This method is intended to synchronize
        the current widget states with their corresponding attributes or variables.

        This implementation is a placeholder and should be overridden by subclasses to provide specific
        functionality for updating user inputs.
        """
        if hasattr(self, 'widget_collection'):
            for widget in self.widget_collection.widgets:
                widget.update()
        else:
            raise AttributeError("The tab does not have a widget_collection attribute.")

# -
