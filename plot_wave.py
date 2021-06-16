# Loading the complex data
import xarray as xr
from capytaine.io.xarray import merge_complex_values
dataset = merge_complex_values(xr.open_dataset("ds_wave_cpl.nc"))

import numpy as np
omegas = dataset['omega']
periods = 2*np.pi / omegas
wavelengths = dataset['wavelength']
wavenumbers = dataset['wavenumber']

from matplotlib import pyplot as plt

# The first plot:
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
sc = ax1.scatter(omegas, periods, wavenumbers, c=wavelengths, cmap='rainbow')
ax1.set(xlabel='w (rad/s)', ylabel='period (s)', zlabel='wavenumber', title='Correlation of wavenumber, w and period')

cbar = fig1.colorbar(sc, ax=ax1, orientation='horizontal', fraction=0.035)
cbar.ax.set_xlabel('wavelength (m)')
fig1.tight_layout()


# The second plot: plotting the waves by different omega in contour
seed = 0.01
# Setting the data
X = Y = np.arange(-2, 2, seed) # defining a flat range and generating a grid mesh
X, Y = np.meshgrid(X, Y)
Z1 = np.sqrt(X**2 + Y**2) # the 'basic' number

fig2, ax2 = plt.subplots(2, 2, figsize=(8,8))

def contour_map(ax, w):
    """
    Setting a contour plot of waves with different omega/period
    :param ax: subplot name
    :param w: omega (rad/s)
    :return: None
    """
    Z = np.sin(w * Z1)
    surf = ax.contour(X, Y, Z, cmap='Blues')
    fig2.colorbar(surf, ax=ax)
    ax.set(title=f'w={w}', xlabel='X', ylabel='Y')

contour_map(ax2[0,0], 1.0)
contour_map(ax2[0,1], 2.0)
contour_map(ax2[1,0], 3.0)
contour_map(ax2[1,1], 4.0)
fig2.suptitle('Shape of waves with different w values')

plt.show()