## Code Louisville Data 2 Final Project:
This project uses the following CSV files:
Jefferson_County_KY_Bikeways.csv
Louisville_Metro_KY_-_Crime_Data_2022.csv
US Zip Codes from 2013 Government Data.csv

Using the CSV files, the project will read in the csv files and perform a series of clean-up statements on each dataframe.  A database is created and each csv file is used to create a table in the database for review later.  A merge is performed to add the LAT and LONG coordinates on the zip codes to the Report Crimes CSV and a new table is created.  A merge is performed to take the Crime data and merge it to the Bike Paths table.   


### Project requirement 1:
Line 19: Bike Data csv is read into a pandas dataframe
Line 32: Crime Data csv is read into a pandas dataframe
Line 40: Zip Code csv is read into a pandas dataframe

### Project requirement 2: 
* Line 48: Column headers are renamed for uniformity and to merge with dataset later
* Line 51: Columns not needed from the Bike dataframe are dropped
* Line 54: Column in Bike dataframe is renamed for uniformity for later merge
* Line 57: Duplicates are dropped from the Bike data set
* Line 60-63: On the Zip Code column of the Crime dataframe, values are changed to numeric and NaN and null values are dropped from the dataset
* Line 66: Column in Crime dataframe is changed for uniformity for later merge
* Line 69-70: Numeric values on Zipcode were a float and added a decimal to the value.  This is changed here to int to format the value
* Line 74-75: Columns not needed from the Crime dataframe are dropped
* Line 79: Rows in the ROADNAME column start with character.  Values are evaluated and dropped as not needed from the data set.
* Line 82: Rows in the ROADNAME column have a character that splits roadnames.  These rows are dropped from the dataset.
* Line 86: ROADNAME values contain address BLOCKS, this is removed from the dataset
* Line 90-95: Whitespace is trimmed and removed from all dataframes
* Line 99-101: The Bike dataframe contains multiple rows to identify the ROADNAME and the types of paths that can be located in that area.  The rows are pivoted to columns here so that they appear on one row later when merging with the Crime dataframe.
* Line 109-111: Each CSV is added to the database as a separate table.  Once these statements are executed, the lines must be commented out to prevent errors on duplicated tables.



* MERGE DATA SETS

### Project requirement 3: 
* MAKE A TABLEAU DASHBOARD


### Project Requirement 4: 
* Annotate your .py files with well-written comments and a clear README.md
