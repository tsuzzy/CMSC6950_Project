# I don't know what is my 2nd computational task right now
# So the script below is just testing what I can do

import capytaine as cpt
import capytaine.io.xarray as xarr
from mpl_toolkits.axes_grid1.axes_size import Fraction
import numpy as np


import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t%(message)s")

# Generating the mesh
full_sphere = cpt.Sphere(
    radius=3, center=(0, 0, 0),  # Size and positions
    ntheta=20, nphi=20,          # Fineness of the mesh
)
full_sphere.add_translation_dof(name="Heave")

# Keeping the immersed part of the mesh
sphere = full_sphere.keep_immersed_part(inplace=False)
sphere.add_translation_dof(name="Heave")

omega_list = np.linspace(1.0, 10.0, 30)

# Setting up a diffraction problem
problems = [cpt.DiffractionProblem(
    body=sphere, wave_direction=0.0, omega=om)
    for om in omega_list]

# Solving the diffraction problem
solver = cpt.BEMSolver()
results = [solver.solve(prob) for prob in sorted(problems)]
#here: next, finding 
periods = [r.period for r in results]
wavelengths = [r.wavelength for r in results]
wavenumbers = [r.wavenumber for r in results]
dataset = xarr.assemble_dataset(results, wavelength=True)


# Defining a mesh of free surface
free_surface = cpt.FreeSurface(
    x_range=(-50,50), y_range=(-50,50), nx=150, ny=150)

diffraction_elevation_surface = solver.get_free_surface_elevation(
    results[0], free_surface, keep_details=True)


# Calculating influence matrices
# Generating the second mesh: cylinder
cylinder = cpt.HorizontalCylinder(
    length=10.0, radius=1.0,  # Dimensions
    center=(0, -2, -2),        # Position
    nr=1, nx=8, ntheta=6,     # Fineness of the mesh
)

# Influence matrix between 2 meshes
engine = cpt.BasicMatrixEngine()
green_func = cpt.Delhommeau()
S, K = engine.build_matrices(
    sphere.mesh, cylinder.mesh,
    free_surface=0.0, sea_bottom=-np.infty,
    wavenumber=1.0, green_function=green_func
)




# from matplotlib import pyplot as plt

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# sc = ax.scatter(omega_list, wavenumbers, wavelengths, c=wavelengths, cmap='rainbow')
# ax.set(xlabel='w (rad/s)', ylabel='Wavenumber', zlabel='wavelength (m)')

# cbar = fig.colorbar(sc, ax=ax, orientation='horizontal', fraction=0.035)
# cbar.ax.set_xlabel('wavelength')

# fig.tight_layout()
# plt.show()

# # try sth new
# ax1 = fig.add_subplot(projection='3d')
# X = np.linspace(-50,50,22500)
# Y = np.linspace(-50,50,22500)
# surf = ax1.scatter(X, Y, diffraction_elevation_surface)
# fig.colorbar(surf)


# Plot the absolute value of the matrix S
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2)
im0 = axs[0].imshow(abs(S))
axs[0].set(title="$|S|$")
fig.colorbar(im0, ax=axs[0])
im1 = axs[1].imshow(abs(K))
axs[1].set(title="$|K|$")
fig.colorbar(im1, ax=axs[1])

plt.tight_layout()
plt.show()