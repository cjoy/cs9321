#!/usr/local/bin/python3
import pandas

def main():
    # Load the dataset into a dataframe
    dataframe = pandas.read_csv('./dataset.csv')
    # Replace the cell value of "Place of Publication" with
    # "London" if it contains "London", and replace all '-' characters with space
    

if __name__ == '__main__':
    main()