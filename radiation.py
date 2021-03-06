# My 1st computational task: solving radiation problems for different set of variables, and 
# plotting added mass and radiation damping for each variable group

# 1. Defining sequences of variables (water depth, liquid density, frequency, accleration of gravity)
# 2. Generating a geometry
# 3. Defining a set of radiation problems for each variable sequence
# 4. Calculating added mass and radiation damping for each problem set
# 5. Plotting the result in seperate subplots

import capytaine as cpt
import capytaine.io.xarray as xarr

import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t%(message)s")


import math
import numpy as np
# Profile of the axisymmetric body (referred from examples/asym.py)
def shape(z):
    return 0.1*(-math.pow((z+1), 2) + 16)

# Generating the mesh and display it with VTK.
geometry = cpt.FloatingBody(
    cpt.AxialSymmetricMesh.from_profile(shape, z_range=np.linspace(-5, 0, 30), nphi=40)
)

# Adding degree of freedom (DOF)
geometry.add_translation_dof(name="Heave")


# Setting up the problems
# Problem set#1: RadiationProblem related to water depth
bottoms = np.linspace(-5,-50,50)
problems_seabottom = [cpt.RadiationProblem(body=geometry, radiating_dof='Heave', sea_bottom=bottom)
            for bottom in bottoms]

# Problem set#2: RadiationProblem related to liquid density
rhos = np.linspace(500, 2000, 50)
problems_density = [cpt.RadiationProblem(body=geometry, radiating_dof='Heave', rho=r)
            for r in rhos]

# Problem set#3: RadiationProblem related to frequency omega
omegas = np.linspace(0.1, 5.0, 50)
problems_freq = [cpt.RadiationProblem(body=geometry, radiating_dof='Heave', omega=om)
            for om in omegas]

# Problem set#4: RadiationProblem related to acceleration of gravity
gravities = np.linspace(1, 20, 50)
problems_grav = [cpt.RadiationProblem(body=geometry, radiating_dof='Heave', g=grav)
            for grav in gravities]

# Solving the problems with the axial symmetry
solver = cpt.BEMSolver(engine=cpt.HierarchicalToeplitzMatrixEngine())

results_seabottom = [solver.solve(problem) for problem in sorted(problems_seabottom)]
dataset1 = xarr.assemble_dataset(results_seabottom, wavelength=True)

results_density = [solver.solve(problem) for problem in sorted(problems_density)]
dataset2 = xarr.assemble_dataset(results_density, wavelength=True)

results_freq = [solver.solve(problem) for problem in sorted(problems_freq)]
dataset3 = xarr.assemble_dataset(results_freq, wavelength=True)

results_grav = [solver.solve(problem) for problem in sorted(problems_grav)]
dataset4 = xarr.assemble_dataset(results_grav, wavelength=True)

dataset1.to_netcdf('ds_waterdepth.nc')
dataset2.to_netcdf('ds_density.nc')
dataset3.to_netcdf('ds_freq.nc')
dataset4.to_netcdf('ds_gravity.nc')