import pandas as pd
import os
import numpy as np
from sqlite3 import connect

conn = connect("test.db")

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
    'DataSource', 'Jefferson_County_KY_Bikeways.csv'), sep=",", low_memory=False)


#####
banner("Crime Data Header")
#####
crime_df = pd.read_csv(os.path.join(
    'DataSource', 'Louisville_Metro_KY_-_Crime_Data_2022.csv'), sep=",", low_memory=False)


# reading in US Zip Codes to locate the latitude and longitude coordinates to zip codes
zips_df = pd.read_csv(os.path.join(
    'DataSource', 'US Zip Codes from 2013 Government Data.csv'), sep=",")
# renaming column headers in US Zip Codes Dataframe
zips_df.columns = ['ZIP_CODE', 'LATITUDE', 'LONGITUDE']


# Project Feature 2:  Clean Data

# dropping columns that are not necessary for analysis in Bike Data
bike_df.drop(columns=['MPWBIKEID', 'SHAPELEN', 'OBJECTID'], inplace=True)

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


# dropping unnecessary columns from crime dataframe
crime_df.drop(columns=['BADGE_ID', 'UCR_HIERARCHY',
              'ATT_COMP', 'NIBRS_CODE', 'ObjectId', 'LMPD_BEAT', 'DATE_REPORTED', 'LMPD_DIVISION'], inplace=True)


# crime data remove address that leads with @

# remove fields that have /
# separate the address fields


# merging crime data with US Zip Code dataframe
#print(pd.merge(crime_df, zips_df, on='ZIP_CODE'))


# TO DO
# separate crime street data


#bike_df.to_sql("bike_df", conn)

#print(pd.read_sql("select * from bike_df", conn))
