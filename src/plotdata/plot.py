import matplotlib.pyplot as plt
from matplotlib import gridspec
import pygmt
import numpy as np

def run_plot(plot_info, inps):
    fig = plt.figure(constrained_layout=True)
    main_gs = gridspec.GridSpec(1, len(plot_info['file(s)']), figure=fig) #rows, columns

    if False: #To remebmer the structure
        # Add a subplot to the figure using the GridSpec
        ax = fig.add_subplot(main_gs[0, 0])

        # Plot something
        ax.plot([0, 1, 2], [0, 1, 4])

        # Show the plot
        plt.show()


def othth():
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