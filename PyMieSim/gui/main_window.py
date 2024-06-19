#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import NoReturn
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt

from PyMieSim.gui.setup import SetUp
from PyMieSim.gui.singleton import datashelf


class PyMieSimGUI:
    """
    Graphical User Interface for computing and visualizing the B1 scattering coefficient
    for cylindrical scatterers using PyMieSim.

    Attributes:
        master (tk.Tk): The main tkinter window.
    """

    def __init__(self, master: tk.Tk):
        """
        Initializes the GUI, setting up variables, plot frame, notebook, and controls.

        Parameters:
            master (tk.Tk): The root window of the application.
        """
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.title("PyMieSim Graphic Interface")
        self.link_radio_button = "link"
        self.customize_notebook_style()
        self.tab_setup()
        self.setup_controls()

    def tab_setup(self):
        self.tab_setup = SetUp(master=self.master)

    def on_close(self) -> NoReturn:
        """
        Handles the GUI close event.
        """
        plt.close('all')  # Close all matplotlib figures
        self.master.destroy()  # Close the Tkinter window

    # The following section of the class will setup the notebooks and their content
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
            command=self.tab_setup.calculate_plot
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

    def update_plot(self) -> NoReturn:
        """
        Will generate and update the plots made by PyMieSima.
        Starts off by calculating all the data needed to create the plot,
        then it generates the figure
        """
        # Deleting any remaining data and figure from datashelf, before calculating new ones
        try:
            del datashelf.figure
            del datashelf.data
        except AttributeError:
            pass

        self.tab_setup.calculate_plot()

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

# -
