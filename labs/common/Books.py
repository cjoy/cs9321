#!/usr/bin/env python3
import pandas

def clean(dataframe):
  dataframe['Place of Publication'] = dataframe['Place of Publication'].apply(
      lambda s: 'London' if 'London' in s else s.replace('-', ' ')
  )
  dataframe['Date of Publication'] = dataframe['Date of Publication'].str.extract(r'^(\d{4})')
  dataframe['Date of Publication'] = pandas.to_numeric(dataframe['Date of Publication'], downcast='unsigned')
  dataframe['Date of Publication'] = dataframe['Date of Publication'].fillna(0)
  dataframe.columns = dataframe.columns.str.replace(' ', '_')
  dataframe.set_index('Identifier', inplace=True)
  return dataframe
