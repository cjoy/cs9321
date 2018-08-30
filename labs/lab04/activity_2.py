#!/usr/bin/env python3
import pandas
from flask import Flask
from flask_restplus import Resource, Api
from activity_1 import clean

# Initialise flask
app = Flask(__name__)
api = Api(app)

@api.route('/books/<int:id>')
class Books(Resource):
  def get(self, id):
    if id not in dataframe.index:
      return {'error': 'Book not found.'}, 404
    return dataframe.loc[id].to_dict(), 200
  def delete(self, id):
    if id not in dataframe.index:
      return {'error': 'Book not found.'}, 404
    dataframe.drop(id, inplace=True)
    return {'status': f'Book {id} removed'}, 200

if __name__ == '__main__':
  dataframe = clean(pandas.read_csv('../common/Books.csv'))
  app.run(debug=True)
