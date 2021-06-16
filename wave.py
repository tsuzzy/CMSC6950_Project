# 2nd computational task:
# 1. Defining a set of diffraction problems and solving them
# 1. Exploring the relationship among wavelength, wave period, wave number and omega
# 3. Adding the 2nd mesh `cylinder`, computing its influence matrices with the 1st mesh `sphere`

import capytaine as cpt
import capytaine.io.xarray as xarr
import numpy as np

import logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s:\t%(message)s")

print("Processing...")

# Generating the mesh
full_sphere = cpt.Sphere(
    radius=3, center=(0, 0, 0),  # Size and positions
    ntheta=20, nphi=20,
)
full_sphere.add_translation_dof(name="Heave")

# Keeping the immersed part of the mesh
sphere = full_sphere.keep_immersed_part(inplace=False)
sphere.add_translation_dof(name="Heave")

omega_list = np.linspace(1.0, 3.5, 30)

# Setting up a diffraction problem
problems = [cpt.DiffractionProblem(
    body=sphere, wave_direction=0.0, omega=om) for om in omega_list]

# Solving the diffraction problem
solver = cpt.BEMSolver(engine=cpt.HierarchicalToeplitzMatrixEngine())
results = [solver.solve(prob) for prob in sorted(problems)]

# Assembling the results into dataset
print("Saving processing results...")
dataset = xarr.assemble_dataset(results, wavelength=True, wavenumber=True)
xarr.separate_complex_values(dataset).to_netcdf('ds_wave_cpl.nc')


# Calculating influence matrices
# Generating the second mesh: cylinder
cylinder = cpt.HorizontalCylinder(
    length=10, radius=1,  # Dimensions
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


# Saving matrices
print("Saving influence matrices...")
import xarray as xr
mat_s = xr.DataArray(S)
mat_k = xr.DataArray(K)

# Resource of the `save_complex` function: 
# https://stackoverflow.com/questions/47162983/how-to-save-xarray-dataarray-with-complex128-data-to-netcdf
def save_complex(data_array, fn):
    ds = xr.Dataset({'real': data_array.real, 'imag': data_array.imag})
    return ds.to_netcdf(fn)

save_complex(mat_s, 'mat_s.nc')
save_complex(mat_k, 'mat_k.nc')

print("Done!")