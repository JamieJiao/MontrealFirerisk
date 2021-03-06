# import data_processing
import pandas as pd

# from google map
min_longitude = -73.949498
max_longitude = -73.474909
min_latitude = 45.410686
max_latitude = 45.706619

southwest = [45.410686, -73.949498]
southeast = [45.410686, -73.474909]
northwest = [45.706619, -73.949498]
northeast = [45.706619, -73.474909]

class CreateGrids:

    def __init__(self, southwest, southeast, northwest, northeast):
        self.southwest= southwest
        self.southeast = southeast
        self.northwest = northwest
        self.northeast = northeast
    
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

        southwest = self.southwest
        northwest = self.northwest
        southeast = self.southeast

        lat_south = southwest[0]
        lat_north = northwest[0]
        lon = southwest[1]

        lon_west = southwest[1]
        lon_east = southeast[1]
        lat = southwest[0]

        # if calculate length, southeast - southwest, lats are the same
        # if calcualte width, northwest - southwest, lons are the same
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
        import numpy as np
        
        southwest = self.southwest
        northwest = self.northwest
        southeast = self.southeast
        northeast = self.northeast
        # x_axis_num: how many points between longitudes(length), east - west 
        # y_axis_num: how many points between latitudes(width), north - south
        x_axis_num, y_axis_num = self.intervals_number()

        # for x axis
        x_axis_interval = (southeast[1] - southwest[1])/x_axis_num
        
        # fot y axis
        y_axis_interval = (northeast[0] - southeast[0])/y_axis_num
        print(y_axis_interval)
        grids = np.zeros([x_axis_num+1, y_axis_num, 2])

        grids = self.fill_grids(grids, x_axis_num, y_axis_num, 
                    x_axis_interval, y_axis_interval)

        return grids, x_axis_interval, y_axis_interval

    def fill_grids(self, grids, x_axis_num, y_axis_num, 
                    x_axis_interval, y_axis_interval):
        start_point = self.southwest

        x_count = 0
        y_count = 0
        x_axis_val = start_point[1]
        grids[0][0] = [start_point[1], start_point[0]]
        
        # when inner loop starts (y), x axis at 0
        # when outer loop starts (x), y axis at 1
        # outer loop has one more loop than inner loop  
        for x in range(x_axis_num+1):
            y_count = 0
            y_axis_val = start_point[0]
             
            for y in range(y_axis_num):
                y_axis_val = y_axis_val + y_axis_interval
                grids[x_count][y_count] = [x_axis_val, y_axis_val]

                y_count = y_count + 1
                
            x_count = x_count + 1        
            x_axis_val = x_axis_val + x_axis_interval

        return grids


    def mapping(self, df):
        from math import ceil, floor
        
        df['Grid Name'] = ''

        grids, x_axis_interval, y_axis_interval = self.return_grids()

        start_point = self.southwest

        # the mapping below, y has one more row than y in the grids array
        # when compare y axis, mapping[x][y] = grids[x][y-1]
        for row_n in range(len(df)):

            longitude = df['LONGITUDE'][row_n]
            latitude = df['LATITUDE'][row_n]

            x_axis = ceil((longitude - start_point[1])/x_axis_interval)
            y_axis = ceil((latitude - start_point[0])/y_axis_interval)

            df['Grid Name'][row_n] = 'Grid_{}_{}'.format(x_axis, y_axis)

        return df
            


df = pd.read_csv('fire_incidents.csv', nrows=500, encoding="ISO-8859-1")


main = CreateGrids(southwest, southeast, northwest, northeast)
grids, a, b = main.return_grids()

mapped_df = main.mapping(df)

print(grids.shape)
print(mapped_df.head())
print(grids[75][65])
print(grids[0][1])
print(grids[0][0])
print("")
print(grids[63][23])
print(grids[63][22])
print(grids[62][23])
print(grids[62][22])


