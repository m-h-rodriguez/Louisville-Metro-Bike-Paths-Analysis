## Code Louisville Data 2 Final Project:
This project uses the following CSV files:

    * Jefferson_County_KY_Bikeways.csv
    * Louisville_Metro_KY_-_Crime_Data_2022.csv
    * US Zip Codes from 2013 Government Data.csv

Using the CSV files, the project will read in the csv files and perform a series of clean-up statements on each dataframe.  A database is created and each csv file is used to create a table in the database for review later.  A merge is performed to add the LAT and LONG coordinates on the zip codes to the Report Crimes CSV and a new table is created.  A merge is performed to take the Crime data and merge it to the Bike Paths table.   

The requirements.txt contains the necessary modules that need to be installed.  Navigating to the command prompt, 'pip install -r requirements.txt" for each module in the list to ensure the program will sucessfully execute.
Sqlite3 is added to the requirements txt but is not necessarily needed as a pip install.  If the module is already available in the version being used, the install may fail. 
Additionally, the extension SQLite can be added to VS Code to assist in viewing the database created.   
The program is executed from the terminal on main.py.


### Project Requirement 1:
* Line 19: Bike Data csv is read into a pandas dataframe
* Line 32: Crime Data csv is read into a pandas dataframe
* Line 40: Zip Code csv is read into a pandas dataframe

### Project Requirement 2: 
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
* Line 138: Left join is performed on the Crime dataframe and the Zipcode dataframe to create new dataframe Lou_Crime_Reports
* Line 144: The performed merge is added as a new table to the database. Once this statement is executed to create the table, it must be commented out to prevent errors running the program.
* Line 155: The Lou_Crime_Reports dataframe is merged to the Bike_Paths dataframe
* Line 160: A new table is created in the database for the merged data set.  Once this is executed, the statement must be commented out to prevent errors running the program after. 



### Project Requirement 3: 
https://public.tableau.com/views/LouisvilleMetroBikePathandCrimeAnalysis/Story1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link


### Project Requirement 4: 
* Annotate your .py files with well-written comments and a clear README.md
