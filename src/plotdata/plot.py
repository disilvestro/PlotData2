import pygmt
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from plotdata.objects.section import Section
from plotdata.objects.create_map import Mapper, Isolines, Relief

def run_plot(plot_info, inps):
    vmin = inps.vlim[0] if inps.vlim else None
    vmax = inps.vlim[1] if inps.vlim else None

    fig = plt.figure(constrained_layout=True)

    n_plots = len(plot_info['file(s)']) + len(inps.add_plot)
    rows = math.ceil(math.sqrt(n_plots))
    columns = math.ceil(n_plots / rows)

    main_gs = gridspec.GridSpec(rows, columns, figure=fig) #rows, columns
    axes = []

    for i in range(n_plots):
        row = i // columns
        col = i % columns
        ax = fig.add_subplot(main_gs[row, col])
        axes.append(ax)

    for i, file in enumerate(plot_info['file(s)']):
        if inps.plot_type == 'horzvert':
            mapper = Mapper(ax=axes[i], file=file)

            if not inps.no_dem:
                Relief(map=mapper, resolution = inps.resolution, cmap = 'terrain', interpolate=inps.interpolate, no_shade=inps.no_shade, zorder=None)

            mapper.add_file(style=inps.style, vmin=vmin, vmax=vmax, zorder=None)

            if inps.isolines != 0:
                Isolines(map=mapper, resolution = inps.resolution, color = inps.iso_color, linewidth = inps.linewidth, levels = inps.isolines, inline = inps.inline, zorder = None) # TODO add zorder

        if inps.plot_type == 'velocity':
            pass
        if inps.plot_type == 'vectors':
            pass
        if inps.plot_type == 'ifgram':
            mapper = Mapper(ax=axes[i], file=file)

            if not inps.no_dem:
                Relief(map=mapper, resolution = inps.resolution, cmap = 'terrain', interpolate=inps.interpolate, no_shade=inps.no_shade, zorder=None)

            mapper.add_file(style=inps.style, vmin=vmin, vmax=vmax, zorder=None)

            if inps.isolines != 0:
                Isolines(map=mapper, resolution = inps.resolution, color = inps.iso_color, linewidth = inps.linewidth, levels = inps.isolines, inline = inps.inline, zorder = None) # TODO add zorder

        if inps.plot_type == 'shaded_relief':
            Relief(map=mapper, resolution = inps.resolution, interpolate=inps.interpolate, no_shade=inps.no_shade, zorder=None)

    plt.show()

def randomstuff():
    pass


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