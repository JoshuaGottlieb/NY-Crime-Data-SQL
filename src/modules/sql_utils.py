import pandas as pd
import sqlite3 as sql

def create_table(cursor, table_name, df, primary_key, foreign_keys = {}):
    '''
    Generates the SQL statement required to create a table based off of a data frame.
    
    args:
        cursor: sqlite3 Cursor object, to use for executing CREATE TABLE statement
        table_name: str, name of the table to create
        df: Pandas DataFrame, containing data to write to table
        primary_key: str, name of column in df to use as primary key
        foreign_keys: dict, where each key is the name of a column in df, and the value is a
            tuple of values (foreign_table_name, foreign_column_name)
            
    returns sqlite3 Cursor object
    '''
    
    # Construct the CREATE TABLE statement
    command = f'CREATE TABLE IF NOT EXISTS {table_name}('
    
    # For each column, append appropriate column name and type to SQL statement
    for i, c in enumerate(df.columns):
        # Determine data type for each column
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
            
        # Add the column name and its SQLite data type to CREATE TABLE statement
        command += f'{(c)} {sql_ctype}'
        
        # Append PRIMARY KEY tag, if applicable
        if c == primary_key:
            command += ' PRIMARY KEY'
        
        # Append comma after each line, except for the last column
        if i != len(df.columns) - 1:
            command += ', '
        
    # If there are foreign keys, add them to the CREATE TABLE statement
    if len(foreign_keys) != 0:
        # Add comma after column definitions
        command += ', '
        
        # Add each foreign key statement, as with adding the column names
        for j, k in enumerate(foreign_keys.keys()):       
            command += f'FOREIGN KEY ({k}) REFERENCES {foreign_keys[k][0]}({foreign_keys[k][1]})'
            
            if j != len(foreign_keys.keys()) - 1:
                command += ', '
    
    # Close CREATE TABLE statement
    command += ');'
    
    # Print constructed string for user verification, in case of error
    print(command)
    
    # Execute command
    cursor = cursor.execute(command)
    
    print(f'Table {table_name} successfully created.')
    
    return cursor

def execute_chunk_query(q, conn, chunksize = 100_000, df = None, verbosity = 1):
    '''
    Executes a SQL query on a SQLite database and writes the result to a Pandas DataFrame in chunks.
    
    args:
        q: str, query to execute
        conn: sqlite3 Connection object to database
        chunksize: int, size of chunk to use for loading the results of the query into the DataFrame
        df: None or Pandas DataFrame, if None, writes to a new dataframe, otherwise concatenates, default None
        verbosity: 0, 1, or 2, if 0, run silently, if 1, give updates on execution and chunk writing, if 2,
            print the first 3 rows of each chunk before writing to dataframe. Default 1.
            
    returns df, containing results of SQL query
    '''
    
    if verbosity == 1 or verbosity == 2:
        print(f'Executing query {q} on database.')
        
    for i, chunk in enumerate(pd.read_sql_query(q, conn, chunksize = chunksize)):
        # If the chunk contains no new data, break
        if len(chunk.index) == 0:
            break
            
        if verbosity == 2:
            print(chunk.head(3))

        if verbosity == 1 or verbosity == 2:
            print(f'Writing chunk {i + 1}.')
        
        # If the dataframe is None, the dataframe becomes the chunk, otherwise, concatenate chunk to dataframe
        if df is None:
            df = chunk
        else:
            df = pd.concat([df, chunk], copy = False)
            
    if verbosity == 1:
        print('Processing done. Returning dataframe.')
    
    return df