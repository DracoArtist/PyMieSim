from PyMieSim.experiment import scatterer


class Singleton:
    """
    This is a class that stores variables latter accesed in another class
    It is used to reduce coupling

    Attributes it will hold during life_time:
    > x_axis_label_widget (tk.StringVar)
    > STD_axis_label_widget (tk.StringVar)
    > scatterer_tab_name (tk.StringVar)
    > measure_map (dict)
    > data (DataVisual.multi_array.Array)
    > figure (matplotlib.figure.Figure)

    """
    def __init__(self) -> None:
        self.measure_map = scatterer.Sphere.available_measure_list  # Default options for y_axis


singleton = Singleton()

# -
