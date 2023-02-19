import pandas as pd
import os
import numpy as np
from sqlite3 import connect

conn = connect("Metro_Data.db")

# function borrowed to print out banners/headers in order to separate different parts of the project for visibility


def banner(message, banner="--------"):

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

# renaming column for merge later
crime_df.rename(columns={'BLOCK_ADDRESS': 'ROADNAME'}, inplace=True)

# converting datatype in crime DataFrame zips to match
m = crime_df.dtypes == 'float64'
crime_df.loc[:, m] = crime_df.loc[:, m].astype(int)


# dropping unnecessary columns from crime dataframe
crime_df.drop(columns=['BADGE_ID', 'UCR_HIERARCHY',
              'ATT_COMP', 'NIBRS_CODE', 'ObjectId', 'LMPD_BEAT', 'DATE_REPORTED', 'LMPD_DIVISION'], inplace=True)


# crime data remove address that leads with @
crime_df = crime_df[~crime_df['ROADNAME'].astype(str).str.startswith('@')]

# remove fields that have /
crime_df = crime_df[crime_df['ROADNAME'].str.contains("/") == False]


# separate the address fields
crime_df['ROADNAME'].replace('.*BLOCK ', '', inplace=True, regex=True)


# trimming out extra whitespace
crime_df = crime_df.apply(lambda x: x.str.strip()
                          if x.dtype == "object" else x)
bike_df = bike_df.apply(lambda x: x.str.strip()
                        if x.dtype == "object" else x)
zips_df = zips_df.apply(lambda x: x.str.strip()
                        if x.dtype == "object" else x)


bike_pivoted = bike_df.pivot(
    index='ROADNAME', columns='MAP_TYPE', values='MAP_TYPE').reset_index()
bike_pivoted.columns.name = None


bike_df.to_sql("bike_df", conn)
crime_df.to_sql("crime_df", conn)
zips_df.to_sql("zips_df", conn)

#print(pd.read_sql("select * from bike_df", conn))

# print(pd.read_sql("select * from crime_df limit 5", conn))
# print(pd.read_sql("select * from zips_df limit 5", conn))


# merging tables
# merging crime data with US Zip Code dataframe
Lou_Crime_Reports = crime_df.merge(zips_df, how="left", on='ZIP_CODE')

Lou_Crime_Reports.to_sql("Lou_Crime_Reports", conn)

# merging Crime Data with Bike Paths
Crime_Bike_Paths = Lou_Crime_Reports.merge(
    bike_pivoted, how="left", on='ROADNAME')
Crime_Bike_Paths.to_sql("Crime_Bike_Paths", conn)

# print(Crime_Bike_Paths.columns)
