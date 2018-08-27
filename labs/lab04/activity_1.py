#!/usr/bin/env python3
import pandas
from flask import Flask
from flask_restplus import Resource, Api
from ...common.Books import load_dataframe

# Initialise flask
app = Flask(__name__)
api = Api(app)

# Initialise global dataframe
dataframe = load_dataframe()

@api.route('/hello')
class HelloWorld(Resource):
  def get(self):
    return {'hello': 'world'}

if __name__ == '__main__':
  app.run(debug=True)
