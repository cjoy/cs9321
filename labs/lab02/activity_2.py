#!/usr/bin/env python3
import pandas

def clean_columns(dataframe):
    # Replace the cell value of "Place of Publication" with
    # "London" if it contains "London", and replace all '-' characters with space    
    dataframe['Place of Publication'] = dataframe['Place of Publication'].apply(
        lambda s: 'London' if 'London' in s else s.replace('-', ' ')
    )
    # Keep the first 4 digit number in "Date of Publication"
    dataframe['Date of Publication'] = dataframe['Date of Publication'].str.extract(r'^(\d{4})')
    # Convert "Date of Publication" cells to numbers
    dataframe['Date of Publication'] = pandas.to_numeric(dataframe['Date of Publication'], downcast='unsigned')
    # Replace NaN with 0 for the cells of "Date of Publication"
    dataframe['Date of Publication'] = dataframe['Date of Publication'].fillna(0)
    return dataframe

def main():
    # Load the dataset into a dataframe
    dataframe = pandas.read_csv('../common/Books.csv')
    # Cleanse dataframe
    dataframe = clean_columns(dataframe)
    # Print the dataframe to see if the changes have been applied properly
    print(dataframe['Date of Publication'])

if __name__ == '__main__':
    main()