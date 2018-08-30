#!/usr/bin/env python3
import pandas
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from activity_1 import clean

# Initialise flask
app = Flask(__name__)
api = Api(app)

Book = api.model('Resource', {
  'name': fields.String,
	'Edition_Statement': fields.String,
	'Place_of_Publication': fields.String,
	'Date_of_Publication': fields.Integer,
	'Publisher': fields.String,
	'Title': fields.String,
	'Author': fields.String,
	'Contributors': fields.String,
	'Corporate_Author': fields.String,
	'Corporate_Contributors': fields.String,
	'Former_owner': fields.String,
	'Engraver': fields.String,
	'Issuance_type': fields.String,
	'Flickr_URL': fields.String,
	'Shelfmarks': fields.String
})

@api.route('/books/<int:id>')
class Books(Resource):
  @api.expect(Book)
  def put(self, id):
    if id not in dataframe.index:
      return {'status': 'Book not found.'}, 404
    req = request.json
    if 'Identifier' in req and id != req['Identifier']:
      return {'status': 'Identifier can\'t be changed.'}, 400
    for key in req:
      if key not in Book.keys():
        return {'status': 'Unexpect value in body'}, 400
      dataframe.loc[id, key] = req[key]
    return dataframe.loc[id].to_dict(), 200

if __name__ == '__main__':
  dataframe = clean(pandas.read_csv('../common/Books.csv'))
  app.run(debug=True)
