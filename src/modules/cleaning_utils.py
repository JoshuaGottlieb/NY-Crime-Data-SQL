from collections import defaultdict
import pandas as pd

def multiple_descriptions(df, code_col, desc_col):
    index = df[[code_col, desc_col]].value_counts().sort_index().index
    dict_ = defaultdict(list)
    
    for code, desc in index:
        dict_[code].append(desc)
        
    multi_dict = {k: v for k, v in dict_.items() if len(v) > 1}

    return multi_dict

def replace_description(df, code_desc_dict, index_map, code_column, desc_column):
    for kv, ix in list(zip(list(code_desc_dict.items()), index_map)):
        df.loc[df[code_column] == kv[0], desc_column] = kv[1][ix]
        
    return

def calculate_missing_ratios(df):
    missing_ratios = df.isnull().sum() / len(df.index)
    highly_missing = missing_ratios[missing_ratios > 0.9]
    moderately_missing = missing_ratios[(missing_ratios > 0.01) & (missing_ratios < 0.9)]
    low_missing = missing_ratios[(missing_ratios <= 0.01) & (missing_ratios > 0)]
    
    return highly_missing, moderately_missing, low_missing

def convert_to_categorical(df, number_col, str_col):
    for c in number_col:
        df[c] = df[c].astype(int).astype('category')
    
    for c in str_col:
        df[c] = df[c].astype('category')
        
    return df

def validate_age(df, cols):
    valid_age_ranges = ['UNKNOWN', '<18', '18-24', '25-44', '45-64', '65+']
    
    for c in cols:
        df[c] = df[c].apply(lambda x: 'UNKNOWN' if not any(x == y for y in valid_age_ranges) else x)
        
    return df

def validate_sex(df, cols):
    valid_sexes = ['M', 'F', 'U']
    
    for c in cols:
        df[c] = df[c].apply(lambda x: 'U' if not any(x == y for y in valid_sexes) else x)
        
    return df
        
def validate_race(df, cols):
    valid_races = ['BLACK', 'WHITE', 'WHITE HISPANIC', 'BLACK HISPANIC',
                   'ASIAN / PACIFIC ISLANDER', 'UNKNOWN', 'AMERICAN INDIAN/ALASKAN NATIVE']
    
    for c in cols:
        df[c] = df[c].apply(lambda x: 'UNKNOWN' if not any(x == y for y in valid_races) else x)
        
    return df

def validate_dates_and_times(df, date_cols, time_cols = None):
    for c in date_cols:
        df = df.loc[df[c].apply(lambda x: int(x[-4:])) >= 2006]
        df[c] = pd.to_datetime(df[c])
        
    if time_cols is not None:
        for c in time_cols:
            df[c] = pd.to_datetime(df[c], format = '%H:%M:%S').dt.time
            
    return df

def validate_coordinates(df):
    df = df[(df.Latitude >= 40.49) & (df.Latitude <= 40.92) & (df.Longitude >= -74.27) & (df.Longitude < -73.68)]
    
    return df