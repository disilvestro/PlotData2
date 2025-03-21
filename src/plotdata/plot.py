import os
import math
import pygmt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from plotdata.objects.section import Section
from plotdata.objects.create_map import Mapper, Isolines, Relief

def run_plot(plot_info, inps):
    vmin = inps.vlim[0] if inps.vlim else None
    vmax = inps.vlim[1] if inps.vlim else None

    fig = plt.figure()

    if inps.plot_type == 'horzvert':
        for file in plot_info['vertical']:
            inps.add_plot.insert(0, 'vertical')
        for file in plot_info['horizontal']:
            inps.add_plot.insert(0, 'horizontal')
    if inps.plot_type == 'velocity':
        for file in plot_info['ascending']:
            inps.add_plot.insert(0, 'ascending')
        for file in plot_info['descending']:
            inps.add_plot.insert(0, 'descending')


    rows = math.ceil(math.sqrt(len(inps.add_plot)))
    columns = math.ceil(len(inps.add_plot) / rows)

    main_gs = gridspec.GridSpec(rows, columns, figure=fig) #rows, columns
    axes = []

    for i in range(len(inps.add_plot)):
        row = i // columns
        col = i % columns
        ax = fig.add_subplot(main_gs[row, col])
        axes.append(ax)

    for i, plot in enumerate(inps.add_plot):
        if plot == 'ascending':
            file = plot_info['ascending'][0]
            plot_info['ascending'].remove(file)
            asc_map = processing_maps(ax=axes[i], file=file, no_dem=inps.no_dem, resolution=inps.resolution, interpolate=inps.interpolate, no_shade=inps.no_shade, style=inps.style, vmin=vmin, vmax=vmax, isolines=inps.isolines, iso_color=inps.iso_color, linewidth=inps.linewidth, inline=inps.inline, movement=inps.movement)

        if plot == 'descending':
            file = plot_info['descending'][0]
            plot_info['descending'].remove(file)
            desc_map = processing_maps(ax=axes[i], file=file, no_dem=inps.no_dem, resolution=inps.resolution, interpolate=inps.interpolate, no_shade=inps.no_shade, style=inps.style, vmin=vmin, vmax=vmax, isolines=inps.isolines, iso_color=inps.iso_color, linewidth=inps.linewidth, inline=inps.inline, movement=inps.movement)

        if plot == 'horizontal':
            file = plot_info['horizontal'][0]
            plot_info['horizontal'].remove(file)
            horz_map = processing_maps(ax=axes[i], file=file, no_dem=inps.no_dem, resolution=inps.resolution, interpolate=inps.interpolate, no_shade=inps.no_shade, style=inps.style, vmin=vmin, vmax=vmax, isolines=inps.isolines, iso_color=inps.iso_color, linewidth=inps.linewidth, inline=inps.inline, movement=inps.movement)

        if plot == 'vertical':
            file = plot_info['vertical'][0]
            plot_info['vertical'].remove(file)
            vert_map = processing_maps(ax=axes[i], file=file, no_dem=inps.no_dem, resolution=inps.resolution, interpolate=inps.interpolate, no_shade=inps.no_shade, style=inps.style, vmin=vmin, vmax=vmax, isolines=inps.isolines, iso_color=inps.iso_color, linewidth=inps.linewidth, inline=inps.inline, movement=inps.movement)

        if plot == 'shaded_relief':
            rel_map = Mapper(ax=axes[i], region=inps.region)
            Relief(map=rel_map, resolution = inps.resolution, interpolate=inps.interpolate, no_shade=inps.no_shade, zorder=None)

        if plot == 'vectors':
            if 'hz' in file:
                horz_section = Section(file)

            if 'up' in file:
                vert_section = Section(file)

    print('Plot order ', inps.add_plot)
    plt.tight_layout()
    plt.show()


def processing_maps(ax, file, no_dem, resolution, interpolate, no_shade, style, vmin, vmax, isolines, iso_color, linewidth, inline, movement=None):
    map = Mapper(ax=ax, file=file)

    if not no_dem:
        Relief(map=map, resolution = resolution, cmap = 'terrain', interpolate=interpolate, no_shade=no_shade, zorder=None)

    map.add_file(style=style, vmin=vmin, vmax=vmax, zorder=None, movement=movement)

    if isolines != 0:
        Isolines(map=map, resolution = resolution, color = iso_color, linewidth = linewidth, levels = isolines, inline = inline, zorder = None) # TODO add zorder

    return map



def point_on_globe(latitude, longitude, size='1'):
    fig = pygmt.Figure()

    # Set up orthographic projection centered on your point
    fig.basemap(
        region="d",  # Global domain
        projection=f"G{np.mean(longitude)}/{np.mean(latitude)}/15c",  # Centered on your coordinates
        frame="g"  # Show gridlines only
    )

    # Add continent borders with black lines
    fig.coast(
        shorelines="1/1p,black",  # Continent borders
        land="white",  # Land color
        water="white"  # Water color
    )

    # Plot your central point
    fig.plot(
        x=longitude,
        y=latitude,
        style=f"t{size}c",  # Triangle marker
        fill="red",  # Marker color
        pen="1p,black"  # Outline pen
    )