import data_processing

class CreateGrids:

    def __init__(self, df):
        self.df = df

    def get_corners(self):
        df = self.df
        # max_longitude = df['LONGITUDE'].max()
        # min_longitude = df['LONGITUDE'].min()
        # max_latitude = df['LATITUDE'].max()
        # min_latitude = df['LATITUDE'].min()

        # from google map
        min_longitude = -73.949498
        max_longitude = -73.474909
        min_latitude = 45.410686
        max_latitude = 45.706619

        southwest = [min_latitude, min_longitude]
        southeast = [min_latitude, max_longitude]
        northwest = [max_latitude, min_longitude]
        northeast = [max_latitude, max_longitude]

        return (southwest, southeast, northwest, northeast)
    
    def calculate_distance(self):
        from math import sin, cos, sqrt, atan2, radians



    def get_inner_points(self):
        import numpy as np

        southwest, southeast, northwest, northeast = self.get_corners()

        return southwest

main = CreateGrids(data_processing.fire_incidents_df)
print(main.get_inner_points())