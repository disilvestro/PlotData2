import os
from plotdata.helper_functions import get_bounding_box
from datetime import datetime
from mintpy.utils import readfile


path = "/Users/giacomo/onedrive/scratch/Unzendake"
file_name = "up.h5"
file_path = os.path.join(path, file_name)


class FileHandler():
    def __init__(self, path) -> None:
        self.path = path
        self.data, self.metadata = readfile.read(path)

        self.start = datetime.strptime(self.metadata['START_DATE'], '%Y%m%d').date()
        self.end = datetime.strptime(self.metadata['END_DATE'], '%Y%m%d').date()

        self.get_region()


    def get_region(self):
        latitude, longitude = get_bounding_box(self.metadata)
        self.region = [longitude[0], longitude[1], latitude[0], latitude[1]]

    # TODO not necessary at the moment
    def xy2lalo(self, x, y):
        """
        Converts x, y coordinates to latitude and longitude.

        Args:
            x (list): List of x-coordinates.
            y (list): List of y-coordinates.

        Returns:
            None

        Side Effects:
            Updates the 'region' attribute of the object.

        """
        lat_out = []
        lon_out = []
        for y_i, x_i in zip(y, x):
            lat_i = None if y_i is None else (y_i + 0.5) * self.lat_step + self.lat0
            lon_i = None if x_i is None else (x_i + 0.5) * self.lon_step + self.lon0
            lat_out.append(lat_i)
            lon_out.append(lon_i)

        self.region = [min(lon_out), max(lon_out), min(lat_out), max(lat_out)]