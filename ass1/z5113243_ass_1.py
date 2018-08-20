#!/usr/bin/env python3
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
import re

'''
'' QUESTION FUNCTIONS
'''

def question_1(df_1, df_2):
  # Rename duplicate columns
  dup_cols = ['Number of Games the country participated in', 'Gold', 'Silver', 'Bronze', 'Total']
  dup_cols_dict = lambda season: dict((key, f'{key} ({season})') for key in dup_cols)
  df_1.rename(columns=dup_cols_dict('summer'), inplace=True)
  df_2.rename(columns=dup_cols_dict('winter'), inplace=True)
  # Merge both datasets using pandas.join
  df_merged = df_1.join(df_2, how='outer')
  # Transform default index to column (in order to demonstrate q2)
  df_merged.index.name = 'Team'
  df_merged.reset_index(drop=False, inplace=True)
  return df_merged

def question_2(df):
  df.set_index('Team', inplace=True)
  return df

def question_3(df):
  df = df.drop(columns=['Rubish'])
  return df

def question_4(df):
  df = df.dropna()
  return df

def question_5(df):
  max_gold = df['Gold (summer)'].max()
  country = df[df['Gold (summer)'] == max_gold].index[0]
  return f'{country} has won {max_gold} gold medals during the summer olympics.'

def question_6(df):
  gold_diff = lambda row: abs(int(row['Gold (summer)']) - int(row['Gold (winter)']))
  df['Gold (difference)'] = df.apply(gold_diff, axis=1)
  max_difference = df['Gold (difference)'].max()
  country = df[df['Gold (difference)'] == max_difference].index[0]
  return f'{country} has the max difference between their summer and winter gold medals by {max_difference}.'

def question_7(df):
  return df.sort_values(by='Total.1', ascending=False)

def question_8(df):
  return df[['Total (winter)', 'Total (summer)']].plot(kind='barh', stacked=True, title='Medals for Winter and Summer Games')

def question_9(df):
  countries = ['United States', 'Australia', 'Great Britain', 'Japan', 'New Zealand']
  columns = ['Gold (winter)', 'Silver (winter)', 'Bronze (winter)']
  return df.loc[df.index.isin(countries)][columns].plot(kind='bar', stacked=False, rot=0, title='Winter Games')

'''
'' HELPERS AND MAIN FUNCTION
'''

# Helper function to clean columns
def clean(df):
  # Drop last row
  df.drop(df.tail(1).index, inplace=True)
  # Transform string to integers
  columns = df.columns[1:]
  df[columns] = df[columns].replace({'\$': '', ',': ''}, regex=True)
  df[columns] = df[columns].astype(int)
  # Clean up country names (ie. remove symols and extra spaces)
  df.index = df.index.map(lambda t: re.sub('\s\(.*$', '', t))
  df.index = df.index.map(lambda t: re.sub('^\s', '', t))
  return df

# Helper function to pretty print all questions
def print_question(number, description, output):
  line = f' {"-"*(14+len(description))}'
  output = f'Columns: {list(output.columns)}\nRows:\n{tabulate(output, tablefmt="grid")}' if isinstance(output, pd.DataFrame) else output
  print(f'{line}\n| Question {number}: {description} |\n{line}\n{output}\n')

if __name__ == '__main__':
  df_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
  df_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
  df_result = question_1(df_1, df_2) 
  print_question(1, 'Merge both datasets and print first five rows.', df_result.head(5)) 
  df_result = question_2(df_result)
  print_question(2, 'Set index as the country name and print the first row.', df_result.head(1))
  df_result = question_3(df_result)
  print_question(3, 'Remove "Rubish" column and print first five rows.', df_result.head(5))
  df_result = question_4(df_result)
  print_question(4, 'Drop rows with with NaN fields and display last 10 rows.', df_result.tail(10))
  df_result = clean(df_result) # Clean data (needed for further questions)
  print_question(5, 'Which country has won the most gold medals in summer games?', question_5(df_result))
  print_question(6, 'Which country has the biggest difference between their summer and winter gold medals?', question_6(df_result))  
  df_result = question_7(df_result)
  print_question(7, 'First and last five rows of countries sorted in descending order?', df_result.head(5).append(df_result.tail(5)))
  print_question(8, 'Plot top ten results from question 7 as stacked horizontal bar graph.', question_8(df_result.head(10)))  
  print_question(9, 'Plot winter medals for United States, Australia, Great Britain, Japan and New Zealand.', question_9(df_result))  
  plt.show()
  # DEBUG: Write resulting dataframe into final_dataset.csv after all transformations
  df_result.to_csv('./final_dataset.csv')