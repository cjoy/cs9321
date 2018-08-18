#!/usr/bin/env python3
import pandas

def main():
    # Load the dataset into a dataframe
    dataframe = pandas.read_csv('./dataset.csv')
    # Calculate and print the number of nan (not a 
    # number) in each column
    nan_cols = dataframe.isnull().sum()
    nan_cols_values = [nan_count for nan_count in nan_cols]
    columns = [col for col in dataframe]
    # Drop the columns of dataframe by the above-
    # mentioned black list
    only_nan_cols = []
    for index, nan_col in enumerate(nan_cols_values):
        if nan_col > 0:
            only_nan_cols.append(columns[index])
    # Print the columns of the dataset to make sure the 
    # dataframe includes only desired columns
    dataframe_without_nan_cols = dataframe.drop(only_nan_cols, axis=1)
    print(dataframe_without_nan_cols)

if __name__ == '__main__':
    main()