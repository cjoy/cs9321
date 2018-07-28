#!/usr/local/bin/python3
from activity_1 import get_dataframe_from_csv
import pandas
import sqlite3

def connect_to_db(filename):
    connection = sqlite3.connect(filename)
    return connection

def store_dataframe_to_sqlite3(connection, dataframe, name):
    dataframe.to_sql(name, connection, if_exists='replace')

def read_sqlite3_to_dataframe(connection, name):
    dataframe = pandas.read_sql_query(f'SELECT * FROM {name}', connection)
    return dataframe

def main():
    dataframe = get_dataframe_from_csv('./dataset.csv')
    db_name = 'demographic_statistics'
    connection = connect_to_db(f'{db_name}.db')
    store_dataframe_to_sqlite3(connection, dataframe, db_name)
    dataframe_2 = read_sqlite3_to_dataframe(connection, db_name)

if __name__   == "__main__":
    main()