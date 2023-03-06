import pandas as pd
import os
import numpy as np
from sqlite3 import connect
import xlsxwriter


conn = connect("Metro_Data.db")

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


#####
banner("Crime Data")
#####
# reading in Louisville Metro report crime 2023 csv file
crime_df = pd.read_csv(os.path.join(
    'DataSource', 'Louisville_Metro_KY_-_Crime_Data_2022.csv'), sep=",", low_memory=False)

#####
banner("Zip Code Data")
#####
# reading in US Zip Codes to locate the latitude and longitude coordinates to zip codes
zips_df = pd.read_csv(os.path.join(
    'DataSource', 'US Zip Codes from 2013 Government Data.csv'), sep=",")


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

# remove fields that have character /
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


# cleaning up Crime datasource by removing fields where PREMISE_TYPE is null
crime_df = crime_df[crime_df['PREMISE_TYPE'].notna()]

# filtering Crime dataset to premise types that could impact cyclists
premise_filter = ['HIGHWAY / ROAD / ALLEY', 'PARKING LOT / GARAGE',
                  'SERVICE / GAS STATION', 'OTHER / UNKNOWN', 'AIR / BUS / TRAIN TERMINAL',
                  'ATTACHED RESIDENTIAL GARAGE', 'PARK / PLAYGROUND', 'SCHOOL - COLLEGE / UNIVERSITY',
                  'ATM SEPARATE FROM BANK']
# dropping all rows not in the filter array
crime_df = crime_df[crime_df['PREMISE_TYPE'].isin(premise_filter)]
print(crime_df)

# rows are pivoted and made to columns
bike_pivoted = bike_df.pivot(
    index='ROADNAME', columns='MAP_TYPE', values='MAP_TYPE').reset_index()
bike_pivoted.columns.name = None


# """
# Creating database table for the csv files that are used for analysis
# Statments can only be executed once to create the table. Comment out the statements
# after the tables are created to prevent errors going forward.
# """
# bike_df.to_sql("Bike_Path_Data", conn)
# crime_df.to_sql("Reported_Crime_Data", conn)
# zips_df.to_sql("Zipcode_Locations", conn)

# #####
# banner("Database Tabe: Bike_Path_Data")
# #####

# print(pd.read_sql("select * from Bike_Path_Data", conn))


# #####
# banner("Database Tabe: Reported_Crime_Data")
# #####

# print(pd.read_sql("select * from Reported_Crime_Data limit 5", conn))


# #####
# banner("Database Tabe: Zipcode_Locations")
# #####


# print(pd.read_sql("select * from Zipcode_Locations limit 5", conn))

# # merging tables
# # merging crime data with US Zip Code dataframe
# Lou_Crime_Reports = crime_df.merge(zips_df, how="left", on='ZIP_CODE')

# """
# Once the statement to create the Lou_Crime_Reports is executed, comment out the
# statement to prevents errors when the program runs.
# """
# Lou_Crime_Reports.to_sql("Lou_Crime_Reports", conn)

# #####
# banner("Database Tabe: Lou_Crime_Reports")
# #####

# print(pd.read_sql("select * from Lou_Crime_Reports limit 5", conn))

# # merging Crime Data with Bike Paths
# Crime_Bike_Paths = Lou_Crime_Reports.merge(
#     bike_pivoted, how="inner", on='ROADNAME')

# """
# Once the statement to create the Crime_Bike_Paths is executed, comment out the
# statement to prevents errors when the program runs.
# """
# Crime_Bike_Paths.to_sql("Crime_Bike_Paths", conn)

# #####
# banner("Database Tabe: Crime_Bike_Paths")
# #####

# print(pd.read_sql("select * from Crime_Bike_Paths limit 5", conn))


# writer = pd.ExcelWriter('Metro_Data.xlsx', engine='xlsxwriter')
# Crime_Bike_Paths.to_excel(writer, sheet_name='Crime_Bike_Paths', index=False)
# Lou_Crime_Reports.to_excel(writer, sheet_name='Lou_Crime_Reports', index=False)
# bike_df.to_excel(writer, sheet_name='Bike_Data_Original', index=False)
# bike_pivoted.to_excel(writer, sheet_name='Bike_Data', index=False)
# writer.close()
