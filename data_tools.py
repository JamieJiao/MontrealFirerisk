import data_processing

# from google map
min_longitude = -73.949498
max_longitude = -73.474909
min_latitude = 45.410686
max_latitude = 45.706619

class CreateGrids:

    def __init__(self, lon_min, lon_max, lat_min, lat_max):
        self.lon_min= lon_min
        self.lon_max = lon_max
        self.lat_min = lat_min
        self.lat_max = lat_max

    def get_corners(self):

        min_longitude = self.lon_min
        max_longitude = self.lon_max
        min_latitude = self.lat_min
        max_latitude = self.lat_max

        southwest = [min_latitude, min_longitude]
        southeast = [min_latitude, max_longitude]
        northwest = [max_latitude, min_longitude]
        northeast = [max_latitude, max_longitude]

        return (southwest, southeast, northwest, northeast)
    
    def calculate_distance(self, lon_west, lon_east, lat_south, lat_north):
        from math import sin, cos, sqrt, atan2, radians

        # approximate radius of earth in km
        R = 6373.0

        lon_west_r = radians(lon_west)
        lon_east_r = radians(lon_east)
        lat_south_r = radians(lat_south)
        lat_north_r = radians(lat_north)

        dlon = lon_east_r - lon_west_r
        dlat = lat_north_r - lat_south_r

        a = sin(dlat / 2)**2 + cos(lat_south_r) * cos(lat_north_r) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    def lenght_width(self):

        southwest, southeast, northwest, northeast = self.get_corners()

        lat_south = southwest[0]
        lat_north = northwest[0]
        lon = southwest[1]

        lon_west = southwest[1]
        lon_east = southeast[1]
        lat = southwest[0]

        length = self.calculate_distance(lon_west, lon_east, lat, lat)
        width = self.calculate_distance(lon, lon, lat_south, lat_north)

        return (length, width)

    def get_inner_points(self):
        import numpy as np

        southwest, southeast, northwest, northeast = self.get_corners()

        return southwest

main = CreateGrids(min_longitude, max_longitude, min_latitude, max_latitude)
print(main.lenght_width())
