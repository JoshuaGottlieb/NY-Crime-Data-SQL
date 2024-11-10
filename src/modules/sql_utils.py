import pandas as pd
import sqlite3 as sql

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

def execute_chunk_query(q, conn, chunksize = 100_000, df = None, verbosity = 1):
    if verbosity == 1 or verbosity == 2:
        print(f'Executing query {q} on database.')
    for i, chunk in enumerate(pd.read_sql_query(q, conn, chunksize = chunksize)):
        if len(chunk.index) == 0:
            break
            
        if verbosity == 2:
            print(chunk.head(3))

        if verbosity == 1 or verbosity == 2:
            print(f'Writing chunk {i + 1}.')
            
        if df is None:
            df = chunk
        else:
            df = pd.concat([df, chunk], copy = False)
            
    if verbosity == 1:
        print('Processing done. Returning dataframe.')
    
    return df
