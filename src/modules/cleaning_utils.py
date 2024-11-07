from collections import defaultdict

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

def create_table(cursor, table_name, df, primary_key, foreign_keys = {}):
    command = f'CREATE TABLE IF NOT EXISTS {table_name}('
    for i, c in enumerate(df.columns):
        python_ctype = str(df[c].dtype)
        
        # SQLite has limited data types
        # It does not have datetime types, and supports everything as text
        if any([python_ctype == 'object',
                python_ctype == 'datetime64[ns]',
                python_ctype == 'category']):
            sql_ctype = 'TEXT'
        # SQLite does not have boolean types, and stores as integer
        elif any([python_ctype == 'int64',
                  python_ctype == 'bool']):
            sql_ctype = 'INTEGER'
        elif python_ctype == 'float64':
            sql_ctype = 'REAL'
        else:
            print(f'Unable to determine SQLite dtype for column {c}. Table was not created.')
            
            return False

        # If a column name is a number, forcefully turn it into a string
        if c.isnumeric():
            c = f'"{c}"'
            
        command += f'{(c)} {sql_ctype}'
        
        if c == primary_key:
            command += ' PRIMARY KEY'
        
        if i != len(df.columns) - 1:
            command += ', '
        
        
    if len(foreign_keys) != 0:
        command += ', '
        
        for j, k in enumerate(foreign_keys.keys()):       
            command += f'FOREIGN KEY ({k}) REFERENCES {foreign_keys[k][0]}({foreign_keys[k][1]})'
            
            if j != len(foreign_keys.keys()) - 1:
                command += ', '
    
    command += ');'
    
    print(command)
    
    cursor = cursor.execute(command)
    
    print(f'Table {table_name} successfully created.')
    
    return cursor