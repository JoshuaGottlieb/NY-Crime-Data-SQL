## Project Description and Repository Usage
A project meant to showcase the ability to clean data, construct and populate a SQL database with tables to contain the data, and execute queries to extract the data in order to create visualizations in Python using the Matplotlib and Seaborn libraries. For this project, four data sets were used from NYC OpenData, three from NYPD data (Historic Arrests, Complaints, and Shooting Data, 2006-2023) and one from the Department of City Planning (New York City Population by Borough, 1950-2040). The raw data sets are too large to store on GitHub directly and can be downloaded from the following links; however, these data sets may be updated over time and may not be identical to those used in the project (retrieved October 14, 2024).

```
Department of City Planning. New york city population by borough, 1950-2040. https://data.cityofnewyork.us/City-Government/New-York-City-Population-by-Borough-1950-2040/xywu-7bv9/about_data
New York Police Department. NYPD arrests data historic. https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u/about_data
New York Police Department. NYPD complaints data historic. https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i/about_data
New York Police Department. NYPD shooting incident data historic. https://data.cityofnewyork.us/Public-Safety/NYPD-Shooting-Incident-Data-Historic-/833y-fsy8/about_data
```

The data cleaning can be found in the [Arrests-](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/src/Arrest-Data-Cleaning.ipynb)/[Complaints-](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/src/Complaints-Data-Cleaning.ipynb)/[Shooting-](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/src/Shooting-Data-Cleaning.ipynb)/[Population-Data-Cleaning.ipynb](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/src/Population-Data-Cleaning.ipynb) notebooks found under src, using utility functions from [src/modules/cleaning_utils.py](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/src/modules/cleaning_utils.py). The cleaned data was small enough to fit into gzipped parquet files and upload to Github, and all of the cleaned data is under [data/cleaned/](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/tree/main/data/cleaned). The data was then further processed and split into tables in [Table-and-Database-Creation.ipynb](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/src/Table-and-Database-Creation.ipynb). This team decided to utilize SQLite as a database solution due to the built-in compatability with the Pandas module to directly execute the results of queries into dataframes, despite the known lack of functionality offered by SQLite.

The resultant database was too large, even when compressed to load onto GitHub. Thus, to regenerate the database, one should download the datasets from the above links and run the cleaning and table creation notebooks. Alternatively, the raw data as used by this project, along with the cleaned parquet.gz files and zipped database can be found at this personal [Google Drive](https://drive.google.com/drive/folders/1dvpSTP7rCZfLwsFYCO6OoKacUBDg9MTV?usp=sharing).

The results of some queries, along with visualizations of those results can be found in the [SQL-Queries-and-Visualizations.ipynb](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/src/SQL-Queries-and-Visualizations.ipynb) notebook, as well as in the presentation available in [presentation/Gottlieb-Correa-Rai-Chunsen-CS673-Midterm-Presentation.pdf](https://github.com/JoshuaGottlieb/Scalable-Databases-Midterm/blob/main/presentation/Gottlieb-Correa-Rai-Chunsen-CS673-Midterm-Presentation.pdf).

## Database Tables
```
# For a more detailed description of column meanings, see the original datasets, listed earlier in this README.

INTERNAL_CODES (detailed offense code and description)      # Extracted from Arrests and Complaints
    PD_CD primary key
    PD_DESC

OFFENSE_CODES (less detailed offense code and description)  # Extracted from Arrests and Complaints
    KY_CD primary key
    OFNS_DESC

ARRESTS    # Arrests Data
    ARREST_KEY primary key
    ARREST_DATE
    KY_CD foreign key into OFFENSE_CODES
    PD_CD foreign key into INTERNAL_CODES
    LAW_CAT_PD
    LAW_CODE
    PRECINCT_CD
    JURISDICTION_CODE
    BORO
    PERP_AGE_GROUP
    PERP_SEX
    PERP_RACE
    LATITUDE
    LONGITUDE

COMPLAINTS    # Complaints Data
    CMPLT_KEY primary key
    CMPLNT_DATE
    CMPLNT_TIME
    RPT_DATE
    KY_CD foreign key into OFFENSE_CODES
    PD_CD foreign key into INTERNAL_CODES
    LAW_CAT_PD
    PRECINCT_CD
    JURISDICTION_CODE
    JURISDICTION_DESC
    BORO
    SUSP_AGE_GROUP
    SUSP_SEX
    SUSP_RACE
    BORO
    VIC_AGE_GROUP
    VIC_SEX
    VIC_RACE
    LATITUDE
    LONGITUDE

SHOOTINGS    # Shooting Incident Data
    INCIDENT_KEY primary key
    OCCUR_DATE
    OCCUR_TIME
    PRECINCT_CD
    JURISDICTION_CODE
    BORO
    STATISTICAL_MURDER_FLAG
    PERP_AGE_GROUP
    PERP_SEX
    PERP_RACE
    VIC_AGE_GROUP
    VIC_SEX
    VIC_RACE
    LATITUDE
    LONGITUDE

# Note: This table is not properly set up in SQL form for query matching.
# It is highly recommended to use it as a lookup table via Pandas as used in src/SQL-Queries-and-Visualizations.ipynb
BOROUGHS     # Borough Population Data
    BORO_CD
    BORO_DESC
    "1950"
    "1960"
    "1970"
    "1980"
    "1990"
    "2000"
    "2010"
    "2020"
    "2030"
    "2040"
```

## Suggested Respository Structure
```
.
|── data/ # Raw and cleaned data, as well as the unzipped SQLite database
|   ├── raw/ # Ending dates may be different for raw files if downloaded directly from source
|   |	├──NYPD_Arrests_Data__Historic__20241014.csv
|   |	├──NYPD_Complaints_Data__Historic__20241014.csv
|   |	├──NYPD_Shooting_Incident_Data__Historic__20241014.csv
|   |	└── New_York_City_Population_by_Borough__1950_-_2040_20241014.csv
|   ├── cleaned/
|   |	├──arrest_data_historic_cleaned_1.parquet.gz
|   |	├──arrest_data_historic_cleaned_2.parquet.gz
|   |	├──complaint_data_historic_cleaned_1.parquet.gz
|   |	├──complaint_data_historic_cleaned_2.parquet.gz
|   |	├──population_data_historic_cleaned.parquet.gz
|   |	└── shooting_data_historic_cleaned_2.parquet.gz
|   └── database/
|   	└── NYC_CRIME_DATABASE.db
|── src/ # Notebooks go here
|   ├── Arrest-Data-Cleaning.ipynb
|   ├── Complaints-Data-Cleaning.ipynb
|   ├── Population-Data-Cleaning.ipynb
|   ├── SQL-Queries-and_Visualizations.ipynb
|   ├── Shooting-Data-Cleaning.ipynb
|   ├── Table-and-Database-Creation.ipynb
|   └── modules/ # Modules used by notebooks go here
|   	├── __init__.py
|   	├── cleaning_utils.py
|   	├── sql_utils.py
|   	└── visualize.py
|   └── visualizations/ # Folder to hold outputs of saved visualizations
```


## Libraries and Versions
```
# Minimal versions of libraries and Python needed
Python 3.8.10
matplotlib==3.7.5
numpy==1.24.4
numpy==1.17.4
pandas==2.0.3
seaborn==0.13.2
```
