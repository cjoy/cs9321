#!/usr/bin/env python3
import pandas
import matplotlib.pyplot as plt

def clean(dataframe):
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
  dataframe = clean(pandas.read_csv('../lab02/dataset.csv'))
  dataframe['Place of Publication'].value_counts().plot.pie()
  plt.show()

if __name__ == '__main__':
  main()