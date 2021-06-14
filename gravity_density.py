# My 1st computational task:
# 1. Defining a sequence of gravities in different planets in the solar system
# 2. Giving a list of densities of different liquid involving ideal water
# 3. Defining a radiation problem
# 4. Solving the problem and plotting the result in sets

import capytaine as cpt
import capytaine.io.xarray as xarr
import numpy as np
import math

import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t%(message)s")

# # Loading a mesh: sphere
# sphere = cpt.Sphere(radius=0.5, center=(0, 0, -2), name="MySphere")

# sphere = cpt.FloatingBody.from_file("examples/boat_200.mar", file_format="mar", name="unit")



# Profile of the axisymmetric body
def shape(z):
    return 0.1*(math.pow(-(z+1), 2) + 16)

# Generate the mesh and display it with VTK.
geometry = cpt.FloatingBody(
    cpt.AxialSymmetricMesh.from_profile(shape, z_range=np.linspace(-5, 0, 30), nphi=40)
)

geometry.show()


# Adding degree of freedom (DOF)
geometry.add_translation_dof(name="Heave")

# Set up the problems
bottoms = np.linspace(-5,-100,50)
# planets = ['Earth', 'Moon', 'Mars']
problems_seabottom = [cpt.RadiationProblem(body=geometry, radiating_dof='Heave', sea_bottom=bottom)
            for bottom in bottoms]

# Problems relating to liquid density
rhos = np.linspace(0.5, 13.5, 52)
problems_density = [cpt.RadiationProblem(body=geometry, radiating_dof='Heave', rho=r)
            for r in rhos]

# Solve the problems using the axial symmetry
solver = cpt.BEMSolver(engine=cpt.HierarchicalToeplitzMatrixEngine())

results_seabottom = [solver.solve(problem) for problem in sorted(problems_seabottom)]
dataset1 = xarr.assemble_dataset(results_seabottom, wavelength=True, wavenumber=True)

results_density = [solver.solve(problem) for problem in sorted(problems_density)]
dataset2 = xarr.assemble_dataset(results_density, wavelength=True)


# Plot results
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2)
fig.suptitle('Variable controls')

axs[0].plot(bottoms, dataset1['wavelength'], label="Wavelength")
axs[0].plot(
    bottoms,
    dataset1['added_mass'].sel(radiating_dof='Heave',influenced_dof='Heave'),
    label="Added mass")
axs[0].plot(
    bottoms,
    dataset1['radiation_damping'].sel(radiating_dof='Heave',influenced_dof='Heave'),
    label="Radiation damping")
axs[0].grid()
axs[0].legend()

# axs[1].plot(rhos, dataset2['wavelength'], label="Wavelength")
axs[1].plot(
    rhos,
    dataset2['added_mass'].sel(radiating_dof='Heave',influenced_dof='Heave'),
    label="Added mass")
axs[1].plot(
    rhos,
    dataset2['radiation_damping'].sel(radiating_dof='Heave',influenced_dof='Heave'),
    label="Radiation damping")
axs[1].grid()
axs[1].legend()

plt.show()