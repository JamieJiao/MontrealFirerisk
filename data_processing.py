import geopandas as gpd
import pandas as pd

property_assess_dir = '/Users/Jiao/Desktop/Data Science and Machine Learning/Final Project/Data/Property Assessment/uniteevaluationfonciere/'
property_assess_link = property_assess_dir + 'uniteevaluationfonciere.shp'
property_assess_df = gpd.read_file(property_assess_link, rows=1000)

fire_incidents_dir = '/Users/Jiao/Desktop/Data Science and Machine Learning/Final Project/Data/Fire Incidents/interventions-sim/'
fire_incidents_link = fire_incidents_dir + 'interventions-sim.shp'
fire_incidents_df = gpd.read_file(fire_incidents_link, rows=1000)

fire_stations_dir = '/Users/Jiao/Desktop/Data Science and Machine Learning/Final Project/Data/Fire Stations/casernes/'
fire_stations_link = fire_stations_dir + 'casernes.shp'
fire_stations_df = gpd.read_file(fire_stations_link)

crime_dir = '/Users/Jiao/Desktop/Data Science and Machine Learning/Final Project/Data/Crime/'
crime_link = crime_dir + 'interventionscitoyendo.csv'
crime_df = pd.read_csv(crime_link, nrows=1000)


print(fire_stations_df.head())