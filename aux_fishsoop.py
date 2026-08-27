
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from cmocean import cm as cmo
from mpl_toolkits.axes_grid1 import make_axes_locatable





def make_map():
    '''
    roi: 'Aus+WCP', 'WCP', 'SolomonSea', 'Sol.Islands', 'Fiji'
    location: "gadi" or "mac"
    plot_spec: "depth" if you want a pcolor plot of the bathymetry, None if you just want a contour for 1000 m

    It only creats the maps, not other plots, for the ROIs defined.
    
    location: gadi or mac, which will change the path to the file.
    '''

    # Getting extension coordinates
    extent = [139.88709, 154.70308, -47.09012, -35.64416]


    # Set up plots
    fig, ax0 = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)},
                        figsize=(15, 8), dpi=100, facecolor='w', edgecolor='k')

    # plot properties
    ax0.set_extent(extent, crs=ccrs.PlateCarree())
    coast = cfeature.GSHHSFeature(
        scale='h', 
        levels=[1, 6], 
        facecolor='darkgray',  # Fill land so data shows only on water
        edgecolor='black',
        linewidth=0.5,
        zorder=2  # Ensures land sits ON TOP of the pcolormesh
    )
    ax0.add_feature(coast)

    gl = ax0.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                    linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlines = True
    gl.xlocator = mticker.FixedLocator(range(-180, 180, 5))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 15, 'color': 'black'}
    gl.xlabel_style = {'color': 'black'}

    return fig, ax0