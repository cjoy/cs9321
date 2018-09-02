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
    # Load the City dataset into a dataframe
    city_df = pandas.read_csv('./dataset.csv')
    # Merge two datasets based on the name of city
    merged_df = pandas.merge(dataframe, city_df, how='left', left_on=['Place_of_Publication'], right_on=['City'])
    # Group by the resultant dataframe based on the country column 
    groupby_df = merged_df.groupby(by=['Country'], as_index=False)
    # Use count() to calculate the number of publications by country
    count_gb_df = groupby_df['Identifier'].count()
    # Print the dataframe
    print(count_gb_df)

if __name__ == '__main__':
    main()