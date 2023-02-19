import pandas as pd
import os
import numpy as np
from sqlite3 import connect

conn = connect("test.db")

# function borrowed to print out banners/headers in order to separate different parts of the project for visibility


def banner(message, banner="--------"):

    line = banner * 11
    print(f"\n{line}")
    print(message)
    print(line)


# Project Feature 1: Read in data files
#####
banner("Bike Data")
#####
# reading in Louisville Metro Bike Path csv file
bike_df = pd.read_csv(os.path.join(
    'DataSource', 'Jefferson_County_KY_Bikeways.csv'), sep=",", low_memory=False)
print(bike_df.head())

#####
banner("Crime Data")
#####
# reading in Louisville Metro report crime 2023 csv file
crime_df = pd.read_csv(os.path.join(
    'DataSource', 'Louisville_Metro_KY_-_Crime_Data_2022.csv'), sep=",", low_memory=False)
print(crime_df.head())

#####
banner("Zip Code Data")
#####
# reading in US Zip Codes to locate the latitude and longitude coordinates to zip codes
zips_df = pd.read_csv(os.path.join(
    'DataSource', 'US Zip Codes from 2013 Government Data.csv'), sep=",")
print(zips_df.head())


# Project Feature 2:  Clean Data

# renaming column headers in US Zip Codes Dataframe
zips_df.columns = ['ZIP_CODE', 'LATITUDE', 'LONGITUDE']

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
crime_df = crime_df[~crime_df['BLOCK_ADDRESS'].astype(str).str.startswith('@')]

# remove fields that have /
crime_df = crime_df[crime_df['BLOCK_ADDRESS'].str.contains("/") == False]


# separate the address fields
crime_df['BLOCK_ADDRESS'].replace('.*BLOCK ', '', inplace=True, regex=True)

# To create the tables in the database Louisville Metro Bike Paths Analysis uncomment out the below commands.  This is only needed once and will throw an error when the command is executed again.

#bike_df.to_sql("bike_df", conn)
# crime_df.to_sql("crime_df", conn)
# zips_df.to_sql("zips_df", conn)


#####
banner("Louisville Metro Bike Database Table")
#####

print(pd.read_sql("select * from bike_df", conn))

#####
banner("Louisville Metro Crime Database Table")
#####

print(pd.read_sql("select * from crime_df limit 5", conn))

#####
banner("Zipcode Database Table")
#####
print(pd.read_sql("select * from zips_df limit 5", conn))


# merging tables

pd.read_sql("create table crime_locations as select * from crime")
