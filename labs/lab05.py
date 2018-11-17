#!/usr/bin/env python3
import pandas
from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse, inputs
from common.Books import clean

# Initialise flask
app = Flask(__name__)
api = Api(app)

Book = api.model('Resource', {
  'Identifier': fields.Integer,
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

parser = reqparse.RequestParser()
parser.add_argument('order_by', choices=list(column for column in Book.keys()))
parser.add_argument('ascending', type=inputs.boolean)

@api.route('/books')
class BooksList(Resource):
  @api.response(200, 'Successful')
  @api.doc(description="Get all books")
  @api.expect(parser, validate=True)
  def get(self):
    args = parser.parse_args()
    order_by = args.get('order_by')
    ascending = args.get('ascending', True)
    if order_by:
      dataframe.sort_values(by=order_by, inplace=True, ascending=ascending)
    return dataframe.to_dict(orient='index'), 200

  @api.response(200, 'Successful')
  @api.response(400, 'Book creation error')
  @api.doc(description="Add a book")
  def post(self):
    req = request.json
    if 'Identifier' not in req:
      return {'status': 'Specify a valid Identifier.'}, 400
    id = req['Identifier']
    if id in dataframe.index:
      return {'status': 'Identifier already taken.'}, 400
    # build dataframe
    for key in req:
      if key not in Book.keys():
        return {'status': f'Unexpect key \'{key}\' in body'}, 400
      dataframe.loc[id, key] = req[key]
    dataframe.append(req, ignore_index=True)
    return dataframe.loc[id].to_dict(), 200

@api.route('/books/<int:id>')
class Books(Resource):
  @api.expect(Book)
  @api.response(200, 'Successful')
  @api.response(400, 'Can\'t process req')
  @api.response(404, 'Can\'t find book')
  @api.doc(description="Get a book")
  def get(self, id):
    if id not in dataframe.index:
      return {'status': 'Book not found.'}, 404
    return dataframe.loc[id].to_dict(), 200

  @api.response(200, 'Successful')
  @api.response(404, 'Can\'t find book')
  @api.doc(description="Delete a book")
  def delete(self, id):
    if id not in dataframe.index:
      return {'status': 'Book not found.'}, 404
    dataframe.drop(id, inplace=True)
    return {'status': f'Book {id} removed'}, 200

  @api.response(200, 'Successful')
  @api.response(404, 'Can\'t find book')
  @api.response(400, 'Can\'t update book')
  def put(self, id):
    if id not in dataframe.index:
      return {'status': 'Book not found.'}, 404
    req = request.json
    if 'Identifier' in req and id != req['Identifier']:
      return {'status': 'Identifier can\'t be changed.'}, 400
    for key in req:
      if key not in Book.keys():
        return {'status': f'Unexpect key \'{key}\' in body'}, 400
      dataframe.loc[id, key] = req[key]
    return dataframe.loc[id].to_dict(), 200

if __name__ == '__main__':
  dataframe = clean(pandas.read_csv('./common/Books.csv'))
  app.run(debug=True)
