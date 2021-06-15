# Loading data from path
import netCDF4 as nc

filename1 = 'ds_waterdepth.nc'
dataset_waterdepth = nc.Dataset(filename1)

filename2 = 'ds_density.nc'
dataset_density = nc.Dataset(filename2)

filename3 = 'ds_freq.nc'
dataset_freq = nc.Dataset(filename3)

filename4 = 'ds_gravity.nc'
dataset_grav = nc.Dataset(filename4)

# Converting datasets from netCDF format to xarray
import xarray as xr

dataset_waterdepth = xr.open_dataset(xr.backends.NetCDF4DataStore(dataset_waterdepth))
dataset_density = xr.open_dataset(xr.backends.NetCDF4DataStore(dataset_density))
dataset_freq = xr.open_dataset(xr.backends.NetCDF4DataStore(dataset_freq))
dataset_grav = xr.open_dataset(xr.backends.NetCDF4DataStore(dataset_grav))

# Reading parameters from datasets
bottoms = dataset_waterdepth['water_depth']
rhos = dataset_density['rho']
omegas = dataset_freq['omega']
gravities = dataset_grav['g']

# Plotting results
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2,2,figsize=(10,10))
fig.suptitle('Added mass and radiation damping vs. Variable groups')

def plot_result(subplot, variable_list, dataset, x_name):
    """
    Setting a subplot of the added mass and radiation damping against a given list of variables
    :param subplot: subplot name
    :param variable_list: a given list of variables
    :param dataset: the dataset to be used as extracting added mass and radiation damping
    :param x_name: name of the subplot x-axe
    :return: None
    """
    subplot.plot(
        variable_list,
        dataset['added_mass'].sel(radiating_dof='Heave',influenced_dof='Heave'),
        label="Added mass")
    subplot.plot(
        variable_list,
        dataset['radiation_damping'].sel(radiating_dof='Heave',influenced_dof='Heave'),
        label="Radiation damping")
    subplot.set(xlabel=x_name, ylabel='F')
    subplot.grid()
    subplot.legend()

plot_result(axs[0,0], bottoms, dataset_waterdepth, 'water depth (m)')
plot_result(axs[0,1], rhos, dataset_density, 'liquid density (kg/m³)')
plot_result(axs[1,0], omegas, dataset_freq, 'frequency (rad/s)')
plot_result(axs[1,1], gravities, dataset_grav, 'acceleration of gravity (m/s²)')

plt.savefig('radiation.png')
plt.show()