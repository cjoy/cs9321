#!/usr/local/bin/python3
import pandas

def get_dataframe_from_cse(filename):
    dataframe = pandas.read_csv(filename)
    return dataframe

def get_columns(dataframe):
    columns = list(dataframe)
    return columns

def get_rows(dataframe, columns):
    rows = [list(map(lambda c: row[c], columns)) for index, row in dataframe.iterrows()]
    return rows

def save_dataframe_to_csv(dataframe, filename):
    dataframe.to_csv(filename)

def main():
    dataframe = get_dataframe_from_cse('./dataset.csv')
    columns = get_columns(dataframe)
    rows = get_rows(dataframe, columns)
    print(columns)
    print(rows)
    save_dataframe_to_csv(dataframe, './dataset.2.csv')

if __name__   == "__main__":
    main()