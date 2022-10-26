import pandas as pd
import psycopg2
import config as config


def gen_df(rows, cols):
    if isinstance(cols, list):
        return pd.DataFrame(data=rows, columns=cols)
    else:
        temp = []
        x = cols.split(",")
        for i in x:
            temp.append(i.split()[-1])
        return pd.DataFrame(data=rows, columns=temp)


def get(table_name, cols='*', where=None, modifier=None, wantrows=False):
    q = df = None
    dbconfig = config.get_config(config, "DATABASE")

    try:
        connection = psycopg2.connect(
            host=dbconfig.get("HOST"),  # host on which the database is running
            database=dbconfig.get("DATABASE"),  # name of the database to connect to
            user=dbconfig.get("USER"),  # username to connect with
            password=dbconfig.get("PASSWORD")  # insert your password here
        )
    except:
        print('Connection failed...')
        pass

    else:
        cursor = connection.cursor()
        if where == None and modifier == None:
            q = f'SELECT {cols} FROM {table_name};'
        elif where != None and modifier == None:
            q = f'SELECT {cols} FROM {table_name} where {where};'
        elif where == None and modifier != None:
            q = f'SELECT {cols} FROM {table_name} {modifier};'
        else:
            q = f'SELECT {cols} FROM {table_name} WHERE {where} {modifier};'

        # print(f'Firing ...{q}')
        cursor.execute(q)
        rows = cursor.fetchall()
        df = gen_df(rows, cols)
        connection.close()
        if wantrows:
            return df, len(rows)  # can take out length to get all data in tuples
        else:
            return df


def get_q(query, cols, table_name, wantrows=False):
    q = df = None
    q = query
    dbconfig = config.get_config(config, "DATABASE")

    try:
        connection = psycopg2.connect(
            host=dbconfig.get("HOST"),  # host on which the database is running
            database=dbconfig.get("DATABASE"),  # name of the database to connect to
            user=dbconfig.get("USER"),  # username to connect with
            password=dbconfig.get("PASSWORD")  # insert your password here
        )
    except:
        print('Connection failed...')
        pass

    else:
        cursor = connection.cursor()
        # print(f'Firing ...{q}')
        cursor.execute(q)
        rows = cursor.fetchall()
        df = gen_df(rows, cols)
        connection.close()
        if wantrows:
            return df, len(rows)  # can take out length to get all data in tuples
        else:
            return df
