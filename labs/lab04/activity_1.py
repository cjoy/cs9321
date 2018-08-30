#!/usr/bin/env python3
import pandas
from flask import Flask
from flask_restplus import Resource, Api

# Initialise flask
app = Flask(__name__)
api = Api(app)

# clean dataset
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

@api.route('/books/<int:id>')
class Books(Resource):
  def get(self, id):
    if id not in dataframe.index:
      return {'status': 'Book not found.'}, 404
    return dataframe.loc[id].to_dict(), 200

if __name__ == '__main__':
  dataframe = clean(pandas.read_csv('../common/Books.csv'))
  app.run(debug=True)
