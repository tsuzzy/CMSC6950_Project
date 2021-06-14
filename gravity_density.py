# My 1st computational task:
# 1. Defining a sequence of gravities in different planets in the solar system
# 2. Giving a list of densities of different liquid involving ideal water
# 3. Defining a radiation problem
# 4. Solving the problem and plotting the result in sets

import capytaine as cpt
import capytaine.io.xarray as xarr

import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t%(message)s")


import math
import numpy as np
# Profile of the axisymmetric body
def shape(z):
    return 0.1*(-math.pow((z+1), 2) + 16)

# Generate the mesh and display it with VTK.
geometry = cpt.FloatingBody(
    cpt.AxialSymmetricMesh.from_profile(shape, z_range=np.linspace(-5, 0, 30), nphi=40)
)

# Adding degree of freedom (DOF)
geometry.add_translation_dof(name="Heave")


# Set up the problems
# Problem set#1: RadiationProblem related to water depth
bottoms = np.linspace(-5,-50,50)
problems_seabottom = [cpt.RadiationProblem(body=geometry, radiating_dof='Heave', sea_bottom=bottom)
            for bottom in bottoms]

# Problem set#2: RadiationProblem related to liquid density
rhos = np.linspace(0.5, 13.5, 52)
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

# Solve the problems using the axial symmetry
solver = cpt.BEMSolver(engine=cpt.HierarchicalToeplitzMatrixEngine())

results_seabottom = [solver.solve(problem) for problem in sorted(problems_seabottom)]
dataset1 = xarr.assemble_dataset(results_seabottom, wavelength=True, wavenumber=True)

results_density = [solver.solve(problem) for problem in sorted(problems_density)]
dataset2 = xarr.assemble_dataset(results_density, wavelength=True)

results_freq = [solver.solve(problem) for problem in sorted(problems_freq)]
dataset3 = xarr.assemble_dataset(results_freq, wavelength=True)

results_grav = [solver.solve(problem) for problem in sorted(problems_grav)]
dataset4 = xarr.assemble_dataset(results_grav, wavelength=True)


# Plot results
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2,2)
fig.suptitle('Variable controls')

def plot_result(subplot, variable_list, dataset, x_name):
    subplot.plot(
        variable_list,
        dataset['added_mass'].sel(radiating_dof='Heave',influenced_dof='Heave'),
        label="Added mass")
    subplot.plot(
        variable_list,
        dataset['radiation_damping'].sel(radiating_dof='Heave',influenced_dof='Heave'),
        label="Radiation damping")
    subplot.set(xlabel=x_name)
    subplot.grid()
    subplot.legend()

plot_result(axs[0,0], bottoms, dataset1, 'water depth (m)')
plot_result(axs[0,1], rhos, dataset2, 'liquid density (kg/m³)')
plot_result(axs[1,0], omegas, dataset3, 'frequency (rad/s)')
plot_result(axs[1,1], gravities, dataset4, 'acceleration of gravity (m/s²)')


plt.show()