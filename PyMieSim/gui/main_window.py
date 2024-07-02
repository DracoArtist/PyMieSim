#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import NoReturn, Dict
import tkinter
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from PyMieSim.experiment import Setup
from PyMieSim.gui.singleton import datashelf
from PyMieSim.gui import SourceTab, ScattererTab, DetectorTab, AxisTab


class PyMieSimGUI:
    """
    Graphical User Interface for computing and visualizing the B1 scattering coefficient
    for cylindrical scatterers using PyMieSim.

    Attributes:
        master (tkinter.Tk): The main tkinter window.
    """

    def __init__(self, master: tkinter.Tk):
        """
        Initializes the GUI, setting up variables, plot frame, notebook, and controls.

        Parameters:
            master (tk.Tk): The root window of the application.
        """
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.title("PyMieSim Graphic Interface")

        datashelf.x_axis_label_widget = tkinter.StringVar(value='phi_offset')
        datashelf.STD_axis_label_widget = tkinter.StringVar(value=None)
        datashelf.STD_axis_label_widget.set(None)

        self.link_radio_button = "link"
        self.customize_notebook_style()
        self.setup_notebook()

        # self.setup_tab = SetUp(master=self.master)
        self.setup_controls()

    # def setup_tab(self):
    #     self.setup_tab = SetUp(master=self.master)

    def on_close(self) -> NoReturn:
        """
        Handles the GUI close event.
        """
        plt.close('all')  # Close all matplotlib figures
        self.master.destroy()  # Close the Tkinter window

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

    # The following section of the class will setup the notebooks and their content
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

    def customize_notebook_style(self) -> NoReturn:
        """
        Customizes the ttk Notebook style for a unique appearance of tabs, making them larger.
        """
        style = ttk.Style()
        style.configure("TNotebook", background="#f0f0f0")

        style.configure(
            "TNotebook.Tab",
            background="#d0d0d0",
            padding=[10, 20, 10, 20],  # Increase padding for larger tabs
            font=('Helvetica', 12)     # Larger font for tabs
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", "#a0a0a0")],
            expand=[("selected", [1, 1, 1, 0])]
        )

        style.configure(
            "Large.TButton",
            font=('Helvetica', 18),
            padding=[20, 20]
        )

    # The following section of the class defines the control buttons and their respective commands
    def setup_controls(self) -> NoReturn:
        """
        Sets up control buttons for calculating results and saving data.
        """
        self.controls_frame = ttk.Frame(self.master)
        self.controls_frame.grid(row=1, column=0, sticky="ew")

        self.calculate_button = ttk.Button(
            self.controls_frame,
            text="Calculate",
            style="Large.TButton",
            command=self.calculate_plot
        )
        self.calculate_button.grid(row=0, column=0, sticky="ew")

        self.save_button = ttk.Button(
            self.controls_frame,
            text="Save as CSV",
            style="Large.TButton",
            command=self.save_data_as_csv
        )
        self.save_button.grid(row=0, column=1, sticky="ew")

        self.export_button = ttk.Button(
            self.controls_frame,
            text="Export Plot",
            style="Large.TButton",
            command=self.export_plot
        )
        self.export_button.grid(row=0, column=2, sticky="ew")

        self.reset_std_button = ttk.Button(
            self.controls_frame,
            text="Reset STD-axis",
            style="Large.TButton",
            command=self.reset_STDaxis_selection
        )
        self.reset_std_button.grid(row=0, column=3, sticky="ew")

    def save_data_as_csv(self) -> NoReturn:
        """
        Triggered by the "Save as CSV" button. Opens a file dialog to save the computed data as a CSV file.
        """

        if hasattr(datashelf, 'data'):
            self.filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if self.filepath:

                # Assuming datashelf.data is a pandas DataFrame or can be converted to one
                np.savetxt(self.filepath, datashelf.data.y.values.squeeze(), delimiter=",")
                print(f"Data saved to {self.filepath}")
        else:
            print("No data to save. Please calculate first.")

    def export_plot(self) -> NoReturn:
        """
        Opens a file dialog for the user to choose where to save the current plot,
        then saves the plot to the specified location.
        """
        # Ensure there's a plot to save
        if hasattr(datashelf, 'figure'):
            # Open file dialog to choose file name and type
            filetypes = [
                ('PNG files', '*.png'),
                ('JPEG files', '*.jpg;*.jpeg'),
                ('PDF files', '*.pdf'),
                ('SVG files', '*.svg'),
                ('All files', '*.*')
            ]

            self.filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=filetypes,
                title="Save plot as..."
            )

            # If a file was selected (i.e., dialog not cancelled)
            if self.filepath:
                # Save the figure using matplotlib's savefig
                datashelf.figure.savefig(self.filepath)
                messagebox.showinfo("Export Successful", f"Plot successfully saved to {self.filepath}")
        else:
            messagebox.showwarning("Export Failed", "No plot available to export.")

    def reset_STDaxis_selection(self):
        """
        Allows the user to unselect the std-axis radiobuttons.
        """
        datashelf.STD_axis_label_widget.set(None)

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
