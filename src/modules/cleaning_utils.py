from collections import defaultdict
import pandas as pd

def multiple_descriptions(df, code_col, desc_col):
    '''
    Extracts a dictionary of codes with multiple descriptions for further inspection.
    
    args:
        df: Pandas DataFrame containing data
        code_col: str, column of df containing codes
        desc_col: str, column of df containing descriptions
        
    returns dict of codes with multiple descriptions, where the codes are keys and the
                values are a list of descriptions
    '''
    
    # Extract codes and descriptions
    index = df[[code_col, desc_col]].value_counts().sort_index().index
    
    # Create a default dictionary to store values and populate
    dict_ = defaultdict(list)
    for code, desc in index:
        dict_[code].append(desc)
        
    # Subset along codes with multiple descriptions
    multi_dict = {k: v for k, v in dict_.items() if len(v) > 1}

    return multi_dict

def replace_description(df, code_desc_dict, index_map, code_column, desc_column):
    '''
    Replaces code descriptions in a dataframe based on a specified mapping.
    
    args:
        df: Pandas DataFrame containing data
        code_desc_dict: dict of lists of str, mapping of codes with multiple columns and
            their distinct descriptions, such as those returned by multiple_descriptions()
        index_map: list of int, which indices to use for each list of descriptions in code_desc_dict
        code_column: str, column in df which contains the codes which are keys in code_desc_dict
        desc_column: str, column in df which contains the descriptions which are values in code_desc_dict
    '''
    
    # For each key-value pair in code_desc_dict, replace the subset data of the dataframe
    # with the values in the key-value pair specified by index_map
    for kv, ix in list(zip(list(code_desc_dict.items()), index_map)):
        df.loc[df[code_column] == kv[0], desc_column] = kv[1][ix]
        
    return

def calculate_missing_ratios(df):
    '''
    Calculates the missingness ratio of each column and returns the level of missingness subset
        by severity of missingness (high > 90% missingness, moderate 1-90% missingness, low < 1% missingness)
        
    args:
        df: Pandas DataFrame containing data
        
    returns: Pandas Series representing the highly, moderately, and columns with low missingness
    '''
    missing_ratios = df.isnull().sum() / len(df.index)
    highly_missing = missing_ratios[missing_ratios > 0.9]
    moderately_missing = missing_ratios[(missing_ratios > 0.01) & (missing_ratios < 0.9)]
    low_missing = missing_ratios[(missing_ratios <= 0.01) & (missing_ratios > 0)]
    
    return highly_missing, moderately_missing, low_missing

def validate_age(df, cols):
    '''
    Coerces age columns to contain only values in ['UNKNOWN', '<18', '18-24', '25-44', '45-65', '65+'].
    
    args:
        df: Pandas DataFrame containing data
        cols: list of str, columns to apply validation to
        
    returns df, Pandas DataFrame with modified columns
    '''
    valid_age_ranges = ['UNKNOWN', '<18', '18-24', '25-44', '45-64', '65+']
    
    for c in cols:
        df[c] = df[c].apply(lambda x: 'UNKNOWN' if not any(x == y for y in valid_age_ranges) else x)
        
    return df

def validate_sex(df, cols):
    '''
    Coerces sex columns to contain only values in ['M', 'F', 'U'].
    
    args:
        df: Pandas DataFrame containing data
        cols: list of str, columns to apply validation to
        
    returns df, Pandas DataFrame with modified columns
    '''
    valid_sexes = ['M', 'F', 'U']
    
    for c in cols:
        df[c] = df[c].apply(lambda x: 'U' if not any(x == y for y in valid_sexes) else x)
        
    return df
        
def validate_race(df, cols):
    '''
    Coerces race columns to contain only values in
        ['BLACK', 'WHITE', 'WHITE HISPANIC', 'BLACK HISPANIC',
        'ASIAN / PACIFIC ISLANDER', 'UNKNOWN', 'AMERICAN INDIAN/ALASKAN NATIVE']
    
    args:
        df: Pandas DataFrame containing data
        cols: list of str, columns to apply validation to
        
    returns df, Pandas DataFrame with modified columns
    '''
    valid_races = ['BLACK', 'WHITE', 'WHITE HISPANIC', 'BLACK HISPANIC',
                   'ASIAN / PACIFIC ISLANDER', 'UNKNOWN', 'AMERICAN INDIAN/ALASKAN NATIVE']
    
    for c in cols:
        df[c] = df[c].apply(lambda x: 'UNKNOWN' if not any(x == y for y in valid_races) else x)
        
    return df

def validate_dates_and_times(df, date_cols, time_cols = None):
    '''
    Drops data before start of datasets (2006) and converts date columns to datetime data type.
    Converts time columns to datetime data type and back to string to verify valid formatting.
    
    args:
        df: Pandas DataFrame containing data
        date_cols: list of str, date columns to apply validation to
        time_cols: None or list of str, time columns to apply validation to, optional, default None
        
    returns df, Pandas DataFrame with modified columns
    '''
    for c in date_cols:
        df = df.loc[df[c].apply(lambda x: int(x[-4:])) >= 2006]
        df[c] = pd.to_datetime(df[c])
        
    if time_cols is not None:
        for c in time_cols:
            df[c] = pd.to_datetime(df[c], format = '%H:%M:%S').dt.time
            
    return df

def validate_coordinates(df):
    '''
    Drops data outside of the NYC Latitude and Longitude boundaries.
        Latitude: (40.49, 40.92)
        Longitude: (-74.27, -73.68)
    
    args:
        df: Pandas DataFrame containing data
        
    returns df, subset Pandas DataFrame
    '''
    df = df[(df.Latitude >= 40.49) & (df.Latitude <= 40.92) & (df.Longitude >= -74.27) & (df.Longitude < -73.68)]
    
    return df

def convert_to_categorical(df, number_col, str_col):
    '''
    Converts columns in a dataframe to category data types to save memory.
    
    args:
        df: Pandas DataFrame containing data
        number_col: list of str, columns to be converted to integers before conversion to category type
        str_col: list of str, object-typed columns to be converted to category type
        
    returns df, Pandas DataFrame with converted column types
    '''
    for c in number_col:
        df[c] = df[c].astype(int).astype('category')
    
    for c in str_col:
        df[c] = df[c].astype('category')
        
    return df