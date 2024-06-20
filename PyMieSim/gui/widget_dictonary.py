from PyMieSim.gui.widgets import InputWidget, RadioButtonWidget

widget_dock = {
    'source_tab': {
        'gaussian': [
            InputWidget(default_value='1310', label='Wavelength [nm]', component_label='wavelength', multiplicative_factor=1e-9, dtype=float),
            InputWidget(default_value='0', label='Polarization angle [degree]', component_label='polarization', dtype=float),
            InputWidget(default_value='1.0', label='Optical Power [mW] [fix]', component_label='optical_power', multiplicative_factor=1e-3, can_be_axis=False, dtype=float),
            InputWidget(default_value='0.2', label='Numerical Aperture (NA) [fix]', component_label='NA', can_be_axis=False, dtype=float),
        ]
    },
    'scatterer_tab': {
        'sphere': [
            InputWidget(default_value='500', label='Diameter [nm]', component_label='diameter', multiplicative_factor=1e-9, dtype=float),
            InputWidget(default_value='1.4', label='Refractive Index', component_label='index', dtype=float),
            InputWidget(default_value='1.0', label='Medium Refractive Index', component_label='medium_index', dtype=float)
        ],
        'cylinder': [
            InputWidget(default_value='1000', label='Diameter [nm]', component_label='diameter', multiplicative_factor=1e-9, dtype=float),
            InputWidget(default_value='1.4', label='Refractive Index', component_label='index', dtype=complex),
            InputWidget(default_value='1.0', label='Medium Refractive Index', component_label='medium_index', dtype=float)
        ],
        'coreshell': [
            InputWidget(default_value='1000', label='Core Diameter [nm]', component_label='core_diameter', multiplicative_factor=1e-9, dtype=float),
            InputWidget(default_value='200', label='Shell Width [nm]', component_label='shell_width', multiplicative_factor=1e-9, dtype=float),
            InputWidget(default_value='1.4', label='Core Refractive Index', component_label='core_index', dtype=complex),
            InputWidget(default_value='1.4', label='Shell Refractive Index', component_label='shell_index', dtype=complex),
            InputWidget(default_value='1.0', label='Medium Refractive Index', component_label='medium_index', dtype=float)
        ]
    },
    'detector': {
        'photodiode': [
            InputWidget(default_value='0.2, 0.3, 0.4', label='Numerical aperture (NA)', component_label='NA', dtype=float),
            InputWidget(default_value='0', label='Gamma [degree]', component_label='gamma_offset', dtype=float),
            InputWidget(default_value='0:360:200', label='Phi [degree]', component_label='phi_offset', dtype=float),
            InputWidget(default_value='None', label='Polarization filter [degree]', component_label='polarization_filter', dtype=float),
            InputWidget(default_value='500', label='Sampling', component_label='sampling', dtype=int)
        ],
        'coherentmode': [
            RadioButtonWidget(option_text=['Point', 'Mean'], options_values=[False, True], component_label='mean_coupling', label='Mean coupling'),
            InputWidget(default_value='0', label='Polarization filter [degree]', component_label='polarization_filter', dtype=float),
            InputWidget(default_value='0', label='Gamma [degree]', component_label='gamma_offset', dtype=float),
            InputWidget(default_value='180:-180:200', label='Phi [degree]', component_label='phi_offset', dtype=float),
            InputWidget(default_value='0.2, 0.3, 0.4', label='Numerical aperture (NA)', component_label='NA', dtype=float),
            InputWidget(default_value='LP01', label='Mode field', component_label='mode_number', dtype=str),
            InputWidget(default_value='0', label='Field rotation [degree]', component_label='rotation', dtype=float),
            InputWidget(default_value='500', label='Sampling', component_label='sampling', dtype=int)
        ]
    }
}
