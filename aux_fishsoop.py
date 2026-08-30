# =========================================================================

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binned_statistic_2d
import pandas as pd 

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from cmocean import cm as cmo
from mpl_toolkits.axes_grid1 import make_axes_locatable

# =========================================================================



def make_map(lon_min, lon_max, lat_min, lat_max):
    # Getting extension coordinates
    extent = [lon_min, lon_max, lat_min, lat_max]

    # Set up plots
    fig, ax0 = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)},
                        figsize=(15, 8), dpi=100, facecolor='w', edgecolor='k')

    # # plot properties
    ax0.set_extent(extent, crs=ccrs.PlateCarree())

    ax0.add_feature(cfeature.LAND, facecolor="lightgray", zorder=10)

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




def fishsoop_binning_spatialFields(fishsoop_data: pd.DataFrame, variable: str, grid_resol: float, extent: list):
    """
        Compute gridded spatial field using 2D binning.

        Parameters
        ----------
        fishsoop_data : pd.DataFrame
            Must contain 'LATITUDE', 'LONGITUDE', and the variable column.
        variable : str
            Column name to aggregate (e.g. 'TEMPERATURE', 'DEPTH', 'TEMP_ANOMALY').
        ROI : str
            Standard ROI names. It will be used in a function to get the extent of the selected domain.
        grid_resol : float
            Grid resolution in degrees.
        extent: list
            lon_min, lon_max, lat_min, lat_max

        Returns
        -------
        stat : 2D np.ndarray
            Binned mean field
        lat_edges : np.ndarray
        lon_edges : np.ndarray

        Fernando Sobral 22 Apr 2026
    """

    lon_bins = np.arange(extent[0] - grid_resol, extent[1] + grid_resol, grid_resol)
    lat_bins = np.arange(extent[2] - grid_resol, extent[3] + grid_resol, grid_resol)

    bin_avg, lat_edges, lon_edges, _ = binned_statistic_2d(
        fishsoop_data['LATITUDE'].to_numpy(dtype=float),
        fishsoop_data['LONGITUDE'].to_numpy(dtype=float),
        fishsoop_data[variable].to_numpy(dtype=float),
        statistic='mean',
        bins=[lat_bins, lon_bins]
    )

    return bin_avg, lat_edges, lon_edges