from PyMieSim.experiment import scatterer


class Singleton:
    """
    This is a class who's utility is to store variables latter accesed in another class
    It is used to reduce coupling

    It also contains a method to validate the axis choices before calculating the plots
    """
    def __init__(self) -> None:
        self.x_axis_label_widget = ''
        self.STD_axis_label_widget = ''
        self.measure_map = scatterer.Sphere.available_measure_list  # Default options for y_axis

    def validate_axis_choice(self, y_axis_selection):
        if self.x_axis_label_widget.get() == self.STD_axis_label_widget.get():
            return "Warning: x-axis cannot be equal to STD-axis."

        if y_axis_selection != "coupling" and self.STD_axis_label_widget.get() in self.detector_tab.component_dict.keys():
            return "Warning: STD-axis cannot be associated to detector if y-axis is not coupling."

        if y_axis_selection != "coupling" and self.x_axis_label_widget.get() in self.detector_tab.component_dict.keys():
            return "Warning: x-axis cannot be associated to detector if y-axis is not coupling."

        return True


singleton = Singleton()

# -
