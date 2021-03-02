# import data_processing
import pandas as pd

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
    
    def intervals_number(self, grid_len=500):
        from math import ceil

        length, width = self.lenght_width()
        
        # convert km to m
        len_intervals_number = ceil(length*1000/grid_len)
        wid_intervals_number = ceil(width*1000/grid_len)

        return (len_intervals_number, wid_intervals_number)

    def return_grids(self):

        southwest, southeast, northwest, northeast = self.get_corners()
        # points_lon: how many points between longitudes(length), east - west 
        # points_lat: how many points between latitudes(width), north - south
        points_lon_num, points_lat_num = self.intervals_number()

        lon_interval_val = (southeast[1] - southwest[1])/points_lon_num
        lat_interval_val = (northeast[0] - southeast[0])/points_lat_num

        grids = self.create_grids(southwest[0], southwest[1], points_lon_num, points_lat_num, 
                                    lon_interval_val, lat_interval_val)

        return grids

    def create_grids(self, start_point_lat, start_point_lon, points_lon_num, 
                    points_lat_num, interval_val_lon, interval_val_lat):
        import numpy as np

        grids = []

        point_lon = start_point_lon
        point_lat = start_point_lat

        for x_axis in range(points_lon_num + 1):
            point_lat = start_point_lat
            for y_axis in range(points_lat_num + 1):
                
                grids.append({'Grid{}_{}'.format(x_axis, y_axis): [point_lat, point_lon]})
                point_lat = point_lat + interval_val_lat
            
            point_lon = point_lon + interval_val_lon

        return grids

    def grids_to_data(self, df, func):
        
        grids = self.return_grids()
        df['Geo'] = df[['LATITUDE','LONGITUDE']].values.tolist()

        # for i in range(len(grids)):
        for i in range(200):

            if i == 68:
                grid1_lon = list(grids[i-68].values())[0][1]
                grid1_lat = list(grids[i-1].values())[0][0]
                grid2_lon = list(grids[i].values())[0][1]
                grid2_lat = list(grids[i].values())[0][0]

                name = list(grids[i].keys())[0]

                df['Grid Name'] = df['Geo'].apply(lambda x: name if x[0] >= grid1_lat \
                                                                and x[1] >= grid1_lon \
                                                                and x[0] < grid2_lat \
                                                                and x[1] < grid2_lon else "NaN")
                
        return df


df = pd.read_csv('fire_incidents.csv', encoding="ISO-8859-1")


def func(x, grid1_lon, \
        grid1_lat, grid2_lon, grid2_lat, name):

    if x.LONGITUDE > grid1_lon:
            x.grid_name = name
            # print(x.grid_name)
            return x.grid_name

main = CreateGrids(min_longitude, max_longitude, min_latitude, max_latitude)
val = main.grids_to_data(df, func=None)
# val = main.return_grids()
# print(val)
val.to_csv('output.csv')
# df['Geo'] = df[['LONGITUDE', 'LATITUDE']].values.tolist()
# print(df)

