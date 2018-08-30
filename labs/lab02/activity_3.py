#!/usr/bin/env python3
import pandas
from activity_2 import clean_columns

def main():
    # Load the dataset into a dataframe
    dataframe = pandas.read_csv('../common/Books.csv')
    # Apply the cleansing methods discussed in Activity-2
    dataframe = clean_columns(dataframe)
    # Replace the spaces in the column names with the underline character ('_')
    dataframe.columns = [c.replace(' ', '_') for c in dataframe.columns]
    # Filter the rows and only keep books which are published in "London" after 1866.
    query = dataframe.query("Place_of_Publication == 'London' and Date_of_Publication > 1866")
    # Print the dataframe and validate the result
    print(query)

if __name__ == '__main__':
    main()