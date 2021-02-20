import data_processing

# from google map
min_longitude = -73.949498
max_longitude = -73.474909
min_latitude = 45.410686
max_latitude = 45.706619

class CreateGrids:

    def __init__(self, min_longi, max_longi, min_lati, max_lati):
        self.min_longi= min_longi
        self.max_longi = max_longi
        self.min_lati = min_lati
        self.max_lati = max_lati

    def get_corners(self):

        min_longitude = self.min_longi
        max_longitude = self.max_longi
        min_latitude = self.min_lati
        max_latitude = self.max_lati

        southwest = [min_latitude, min_longitude]
        southeast = [min_latitude, max_longitude]
        northwest = [max_latitude, min_longitude]
        northeast = [max_latitude, max_longitude]

        return (southwest, southeast, northwest, northeast)
    
    def calculate_distance(self):
        from math import sin, cos, sqrt, atan2, radians

        lat1 = radians(52.2296756)
        lon1 = radians(21.0122287)
        lat2 = radians(52.406374)
        lon2 = radians(16.9251681)


    def get_inner_points(self):
        import numpy as np

        southwest, southeast, northwest, northeast = self.get_corners()

        return southwest

main = CreateGrids(data_processing.fire_incidents_df)
print(main.get_inner_points())