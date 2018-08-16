import pandas as pd

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
  df['Gold (difference)'] = df.apply(lambda row: abs(int(row['Gold (summer)']) - int(row['Gold (winter)'])), axis=1)
  max_difference = df['Gold (difference)'].max()
  country = df[df['Gold (difference)'] == max_difference].index[0]
  return f'{country} has the max difference between their summer and winter gold medals by {max_difference}.'

def question_7(df):
  return df.sort_values(by='Total.1', ascending=False)

def question_8():
  # insert code here
  return 

def question_9():
  # insert code here
  return

'''
'' HELPERS AND MAIN FUNCTION
'''

# Helper function to clean columns
def clean_columns(df):
  # Drop last row
  df.drop(df.tail(1).index, inplace=True)
  # Transform string to integers
  columns = df.columns[1:]
  df[columns] = df[columns].replace({'\$': '', ',': ''}, regex=True)
  df[columns] = df[columns].astype(int)
  return df

# Helper function to pretty print all questions
def print_question(number, description, output):
  line = f' {"-"*(14+len(description))}'
  print(f'{line}\n| Question {number}: {description} |\n{line}\n{output}\n')

if __name__ == '__main__':
  df_1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
  df_2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
  df_result = question_1(df_1, df_2) 
  print_question(1, 'Merge both datasets and print first five rows.', df_result.head(5)) 
  df_result = question_2(df_result)
  print_question(2, 'Set index as the country name and print index of first row.', df_result.head(1).index[0])
  df_result = question_3(df_result)
  print_question(3, 'Remove "Rubish" column and print first five rows.', df_result.head(5))
  df_result = question_4(df_result)
  print_question(4, 'Drop rows with with NaN fields and display last 10 rows.', df_result.tail(10))
  df_result = clean_columns(df_result) # Clean columns further for further analysis
  print_question(5, 'Which country has won the most gold medals in summer games?', question_5(df_result))
  print_question(6, 'Which country has the biggest difference between their summer and winter gold medals?', question_6(df_result))  
  df_result = question_7(df_result)
  print_question(7, 'First and last five rows of countries sorted in descending order?', df_result.head(5).append(df_result.tail(5)))
  # DEBUG: Write resulting dataframe into final_dataset.csv after all transformations
  df_result.to_csv('./final_dataset.csv')