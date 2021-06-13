from os import name
import capytaine as cpt
from capytaine import *
import logging
import numpy as np
import xarray as xr

logging.basicConfig(level=logging.INFO)

body = cpt.FloatingBody.from_file("boat_200.mar", file_format="mar", name="unit")

test_matrix = xr.Dataset(coords={
    'omega': np.linspace(0.1, 4, 40),
    'wave_direction': [0, np.pi/2],
    'radiating_dof': ['Heave'],
    'water_depth': [np.infty],
})
dataset = cpt.BEMSolver().fill_dataset(test_matrix, body)

print(dataset)