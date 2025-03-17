import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


import re
import pygmt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LightSource
from plotdata.helper_functions import parse_polygon
from plotdata.objects.file_handler import FileHandler


class MapRelief():
    def __init__(self, region=None, polygon=None, location_types: dict = {},ax=None, file: FileHandler = None):
        if not ax:
            self.fig = plt.figure(figsize=(8, 8))
            self.ax = self.fig.add_subplot(111)

        else:
            self.ax = ax
            self.fig = ax.get_figure()

        # self.ax.set_title('Elevation Map')
        # self.ax.set_xlabel('Longitude')
        # self.ax.set_ylabel('Latitude')

        if file:
            self.data = file.data
            self.region = file.region

        elif region:
                self.region = region

        elif polygon:
            self.region = parse_polygon(polygon)

        # TODO sure about zero? is it the correct?
        self.zorder = 0
        self.location_types = location_types


    def get_next_zorder(self):
        z = self.zorder
        self.zorder += 1
        return z


    def add_isolines(self, resolution = '01m', color = 'black', linewidth = 0.5, levels = 10, inline = False, zorder = None):
        if not zorder:
            zorder = self.get_next_zorder()

        # Plot isolines
        print("Adding isolines\n")
        lines = pygmt.datasets.load_earth_relief(resolution=resolution, region=self.region)

        grid_np = lines.values

        # Remove negative values
        grid_np[grid_np < 0] = 0

        # Convert the numpy array back to a DataArray
        lines[:] = grid_np

        # Plot the data
        cont = self.ax.contour(lines, levels=levels, colors=color, extent=self.region, linewidths=linewidth, zorder=zorder)

        if inline:
            self.ax.clabel(cont, inline=inline, fontsize=8)


    def add_colormap(self, cmap = 'terrain', resolution = '01m', interpolate=False, shade=True, zorder=None):
        if not zorder:
            zorder = self.get_next_zorder()

        # Plot colormap
        # Load the relief data
        print("Adding colormap\n")
        self.elevation = pygmt.datasets.load_earth_relief(resolution=resolution, region=self.region)

        if interpolate:
            self.interpolate_relief(resolution)

        # Set all negative values to 0
        self.elevation = self.elevation.where(self.elevation >= 0, 0)

        if shade:
            im = self.shade_elevation(zorder=zorder)
        else:
            im = self.ax.imshow(self.elevation, cmap=cmap, extent=self.region, origin='lower',zorder=zorder)

        if False:
            # Add a colorbar
            cbar = self.fig.colorbar(im, ax=self.ax, orientation='vertical', fraction=0.046, pad=0.04)
            cbar.set_label('Elevation (m)')


    def add_location(self, latitude, longitude, label='', type='earthquake', size=10, zorder=None):
        if not zorder:
            zorder = self.get_next_zorder()

        if type == 'earthquake':
            marker = 'o'
            color = 'purple'
            alpha = 0.5

        else:
            marker = '^'
            color = 'red'
            alpha = 1

        self.ax.plot(longitude, latitude, marker, color=color, markersize=size, alpha=alpha, zorder=zorder)
        self.ax.text(longitude, latitude, label, fontsize=7, ha='right', zorder=zorder, color=color)

        # Track location types for legend
        if type not in self.location_types:
            self.location_types[type] = {'marker': marker, 'color': color}


    def add_legend(self):
        handles = []
        for type, props in self.location_types.items():
            handle = plt.Line2D([0], [0], marker=props['marker'], color='w', label=type, markersize=10, markerfacecolor=props['color'])
            handles.append(handle)
        self.ax.legend(handles=handles, loc='upper right')


    def add_section(self, latitude, longitude, color='black', zorder=None):
        if not zorder:
            zorder = self.get_next_zorder()

        self.ax.plot(longitude, latitude, '-', linewidth=2, alpha=0.7, color=color, zorder=zorder)
        # self.ax.text(longitude[0], latitude[0], 'A', fontsize=10, ha='right', color=color)
        # self.ax.text(longitude[1], latitude[1], 'B', fontsize=10, ha='left', color=color)


    def add_file(self, style='pixel', vmin=None, vmax=None, zorder=None):
        if not zorder:
            zorder = self.get_next_zorder()

        # TODO add displacement
        # self.data = self.data * 120/365 
        if style == 'pixel':
            self.imdata = self.ax.imshow(self.data, cmap='jet', extent=self.region, origin='lower', interpolation='none',zorder=zorder, vmin=vmin, vmax=vmax)

        elif style == 'scatter':
            # Assuming self.data is a 2D numpy array
            data = self.data
            nrows, ncols = data.shape
            x = np.linspace(self.region[0], self.region[1], ncols)
            y = np.linspace(self.region[2], self.region[3], nrows)
            X, Y = np.meshgrid(x, y)
            X = X.flatten()
            Y = Y.flatten()
            C = data.flatten()

            self.imdata = self.ax.scatter(X, Y, c=C, cmap='jet', marker='o', zorder=zorder, s=2, vmin=vmin, vmax=vmax)


    def interpolate_relief(self, resolution):
            print("!WARNING: Interpolating the data to a higher resolution grid")
            print("Accuracy may be lost\n")
            # Interpolate the relief data to the new higher resolution grid
            digits = re.findall(r'\d+', resolution)
            letter = re.findall(r'[a-z]', resolution)
            new_grid_spacing = f'{(int(digits[0]) / 10)}{letter[0]}'

            self.elevation = pygmt.grdsample(grid=self.elevation, spacing=new_grid_spacing, region=self.region)


    def shade_elevation(self,zorder=None):
        if not zorder:
            zorder = self.get_next_zorder()

         # Create hillshade
        print("Shading the elevation data...\n")
        ls = LightSource(azdeg=315, altdeg=45)
        hillshade = ls.hillshade(self.elevation, vert_exag=1.5, dx=1, dy=1)

        # Plot the elevation data with hillshading
        im = self.ax.imshow(hillshade, cmap='gray', extent=self.region, origin='lower', alpha=0.5, zorder=zorder, aspect='auto')

        return im


    def plot(self):
        self.add_legend()
        plt.show()