import pandas as pd
import os
import numpy as np


# function borrowed to print out banners/headers in order to separate different parts of the project for visibility
def banner(message, banner="-"):

    line = banner * 11
    print(f"\n{line}")
    print(message)
    print(line)


# project feature 1: Read in two data files
#####
banner("Bike Data Header")
#####
bike_df = pd.read_csv(os.path.join(
    'DataSource', 'Jefferson_County_KY_Bikeways.csv'), sep=",")
print(bike_df.head())

#####
banner("Crime Data Header")
#####
crime_df = pd.read_csv(os.path.join(
    'DataSource', 'Louisville_Metro_KY_-_Crime_Data_2022.csv'), sep=",")
print(crime_df.head())
print(crime_df.dtypes)

print(bike_df.dtypes)

# reading in US Zip Codes to locate the latitude and longitude coordinates to zip codes
zips_df = pd.read_csv(os.path.join(
    'DataSource', 'US Zip Codes from 2013 Government Data.csv'), sep=",")
print(zips_df.head())

print(zips_df.dtypes)

# Project Feature 2:  Clean Data
# dropping columns that are not necessary for analysis in Bike Data
bike_df.drop(columns=['MPWBIKEID'], inplace=True)
bike_df.drop(columns=['SHAPELEN'], inplace=True)
bike_df.drop(columns=['OBJECTID'], inplace=True)

# making text in column uniform to remove duplicates
bike_df['ROADNAME'] = bike_df['ROADNAME'].str.upper()

# dropping duplicated rows
bike_df.drop_duplicates(inplace=True)

# dropping NaN values from zip code column
crime_df["ZIP_CODE"] = crime_df["ZIP_CODE"].apply(
    pd.to_numeric, errors='coerce').fillna('')
crime_df['ZIP_CODE'].replace('', np.nan, inplace=True)
crime_df.dropna(subset=['ZIP_CODE'], inplace=True)

# converting datatype in crime DataFrame zips to match
m = crime_df.dtypes == 'float64'
crime_df.loc[:, m] = crime_df.loc[:, m].astype(int)

# renaming column headers in US Zip Codes Dataframe
zips_df.columns = ['ZIP_CODE', 'LATITUDE', 'LONGITUDE']
