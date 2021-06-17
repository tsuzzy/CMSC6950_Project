# Loading the complex data
import xarray as xr
from capytaine.io.xarray import merge_complex_values
dataset = merge_complex_values(xr.open_dataset("ds_wave_cpl.nc"))

import numpy as np
omegas = dataset['omega']
periods = 2*np.pi / omegas
wavelengths = dataset['wavelength']
wavenumbers = dataset['wavenumber']

# Reference of function `read_complex`:
# https://stackoverflow.com/questions/47162983/how-to-save-xarray-dataarray-with-complex128-data-to-netcdf
def read_complex(fn):
    ds = xr.open_dataset(fn)
    return ds['real'] + ds['imag'] * 1j

# Loading matrices S and K
S = read_complex('mat_s.nc')
K = read_complex('mat_k.nc')

from matplotlib import pyplot as plt

# The first plot: plotting correlation of wavenumber, w and period
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

fig2, ax2 = plt.subplots(2, 2, figsize=(10,10))

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

# The third plot: plotting inluence matrices
fig3, ax3 = plt.subplots(1, 2)

im0 = ax3[0].imshow(abs(S), cmap='YlOrRd')
ax3[0].set(title="$|S|$")
fig3.colorbar(im0, ax=ax3[0])

im1 = ax3[1].imshow(abs(K), cmap='YlOrRd')
ax3[1].set(title="$|K|$")
fig3.colorbar(im1, ax=ax3[1])

fig3.suptitle('Influence matrices between two mesh objects')

# Storing the images
from os import path
output_path = './img/'
fig1.savefig(path.join(output_path,"2_1_correlation.png"))
fig2.savefig(path.join(output_path,"2_2_waveshape.png"))
fig3.savefig(path.join(output_path,"2_3_infmatrix.png"))