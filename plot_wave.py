# Loading the complex data
import xarray as xr
from capytaine.io.xarray import merge_complex_values
dataset = merge_complex_values(xr.open_dataset("ds_wave_cpl.nc"))

omegas = dataset['omega']
periods = 1 / omegas
wavelengths = dataset['wavelength']
wavenumbers = dataset['wavenumber']

from matplotlib import pyplot as plt

fig1 = plt.figure()
ax1 = fig1.add_subplot(projection='3d')
sc = ax1.scatter(omegas, periods, wavenumbers, c=wavelengths, cmap='rainbow')
ax1.set(xlabel='w (rad/s)', ylabel='period (s)', zlabel='wavenumber')

cbar = fig1.colorbar(sc, ax=ax1, orientation='horizontal', fraction=0.035)
cbar.ax.set_xlabel('wavelength')
fig1.tight_layout()

plt.show()