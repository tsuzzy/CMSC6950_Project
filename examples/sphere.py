from capytaine import *
import logging

logging.basicConfig(level=logging.WARNING)

# Loading a mesh: here is a simple geometry
sphere = Sphere(radius=1.0, center=(0, 0, -2), name="my_sphere")
# sphere.show()

# Defining dof (degree of freedom)
# in the x-direction
sphere.dofs['Surge'] = [(1, 0, 0) for face in sphere.mesh.faces]
sphere.add_translation_dof(name="Heave")

# Defining linear potential flow problem
from numpy import infty
problem = RadiationProblem(body=sphere, radiating_dof="Heave", omega=1.0, sea_bottom=-infty, g=9.81, rho=1000)

# Solving the problem
solver = BEMSolver()
result = solver.solve(problem)

# The other problem
problem2 = RadiationProblem(body=sphere, radiating_dof="Surge", omega=1.0)
result2 = solver.solve(problem2)

# Gathering the results
dataset = assemble_dataset([result, result2])

dataset['added_mass'].sel(radiating_dof=["Surge", "Heave"], influenced_dof=["Surge", "Heave"], omega=1.0)
dataset.to_netcdf("sphere.nc")