#!/usr/bin/env python3
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests, datetime, re

#------------- CONFIG CONSTANTS -------------#

DEBUG = True
MAX_PAGE_LIMIT = 2
COLLECTION = 'indicators'
DB_CONFIG = {
  'dbuser': 'z5113243',
  'dbpassword': 'badpassword01',
  'mlab_inst': 'ds239071',
  'dbname': 'cs9321_ass2' 
}

#------------- API INITIALISATION -------------#

db = None # initialised in main
app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
api = Api(
  app,
  title='Assignment 2 - COMP9321 - Chris Joy (z5113243)',
  description='In this assignment, we\'re asked to develop ' \
  'a Flask-Restplus data service that allows a client to ' \
  'read and store some publicly available economic indicator ' \
  'data for countries around the world, and allow the consumers ' \
  'to access the data through a REST API.'
)
indicator_model = api.model(COLLECTION, {
  'indicator_id': fields.String(required=True,
                                title='An Indicator ',
                                description='http://api.worldbank.org/v2/indicators',
                                example='NY.GDP.MKTP.CD'),
})
parser = api.parser()
parser.add_argument('q', help='Query param. Expected format: top<k> / bottom<k>, ' \
                              'where k is between 1 and 100. Eg. top10, bottom40')

#------------- HELPER FUNCTIONS -------------#

def mlab_client(dbuser, dbpassword, mlab_inst, dbname):
  return MongoClient(
    f'mongodb://{dbuser}:{dbpassword}@{mlab_inst}.mlab.com:39071/{dbname}'
  )[dbname]

def api_url(indicator, date='2012:2017', fmt='json', page=1):
  return 'http://api.worldbank.org/v2/countries/all/indicators/' \
          f'{indicator}?date={date}&format={fmt}&page={page}'

# Recursively build an array containing indicator data
def get_indicator_data(indicator, page=1, prevRes=[], max_pages=MAX_PAGE_LIMIT):
  response = requests.get(api_url(indicator=indicator, page=page)).json()
  if not indicator or (len(response) <= 1 and response[0]['message'][0]['key'] == 'Invalid value'):
    return 'Invalid indicator'
  if response[0]['page'] >= max_pages or response[0]['page'] == response[0]['pages']:
    return prevRes+response[1]
  return get_indicator_data(
    indicator=indicator,
    page=response[0]['page']+1,
    prevRes=prevRes+response[1],
    max_pages=max_pages,
  )

# Restructure indicator entry according to spec
def format_collection_entry(indicator_data):
  return {
    'country': indicator_data['country']['value'],
    'date': indicator_data['date'],
    'value': indicator_data['value'],
  }

# Transform to top<k>/bottom<k> queries to array indexes
def query_to_index(query, arr_size):
  try:
    match = re.search(r'^(bottom|top)\d+$', query).group()
    order = re.search(r'^(bottom|top)', match).group()
    length = int(re.search(r'\d+$', match).group())
    if order == 'top':
      return slice(length)
    elif order == 'bottom':
      return slice(arr_size-length, arr_size)
    else:
      return slice(arr_size)
  except:
     return slice(arr_size)

#------------- QUESTION ROUTES -------------#

@api.route(f'/{COLLECTION}', endpoint=COLLECTION)
class CollectionIndex(Resource):
  @api.doc(description='[Q1] Import a collection from the data service.')
  @api.response(200, 'Successfully retrieved collection.')
  @api.response(201, 'Successfully created collection.')
  @api.response(400, 'Unable to create / retrieve collection.')
  @api.expect(indicator_model)
  def post(self):
    body = request.json
    # Indicator hasn't been specified in body (400)
    if not body['indicator_id']:
      return { 'message': 'Please specify an indicator.' }, 400
    # Retrieve indicator from database (200)
    existing_collection = db[COLLECTION].find_one({'indicator': body['indicator_id']})
    if existing_collection:
      return {
        'location': f'/{COLLECTION}/{str(existing_collection["_id"])}',
        'collection_id': str(existing_collection['_id']),
        'creation_time': str(existing_collection['creation_time']),
        'indicator': existing_collection['indicator'],
      }, 200
    # From now onwards we need to obtain data from the Worldbank API
    indicator_data = get_indicator_data(body['indicator_id'])
    # Valid indicator hasn't been specified (400)
    if indicator_data == 'Invalid indicator':
      return { 'message': 'Please specify a valid indicator.' }, 400
    # Create and retrieve indicator from Worldbank API (201)
    collection = {
      'indicator': indicator_data[0]['indicator']['id'],
      'indicator_value': indicator_data[0]['indicator']['value'],
      'creation_time': datetime.datetime.utcnow(),
      'entries': [format_collection_entry(entry) for entry in indicator_data],
    }
    created_collection = db[COLLECTION].insert_one(collection)
    return {
      'location': f'/{COLLECTION}/{str(created_collection.inserted_id)}',
      'collection_id': str(created_collection.inserted_id),
      'creation_time': str(collection['creation_time']),
      'indicator': collection['indicator'],
    }, 201

  @api.doc(description='[Q3] Retrieve the list of available collections.')
  @api.response(200, 'Successfully retreieved collections.')
  @api.response(400, 'Unable to retreive collections.')
  def get(self):
    try:
      collections = db[COLLECTION].find()
    except:
      return { 'message': 'Unable to retrieve collections.' }, 400
    return [{
      'location': f'/{COLLECTION}/{str(doc["_id"])}',
      'collection_id': str(doc['_id']),
      'creation_time': str(doc['creation_time']),
      'indicator': doc['indicator'],
    } for doc in collections], 200

@api.route(f'/{COLLECTION}/<collection_id>', endpoint=f'{COLLECTION}_by_id')
@api.param('collection_id', f'Unique id, used to distinguish {COLLECTION}.')
class CollectionsById(Resource):
  @api.doc(description='[Q2] Deleting a collection with the data service.')
  @api.response(200, 'Successfully removed collection.')
  @api.response(404, 'Unable to find collection.')
  @api.response(400, 'Unable to remove collection.')
  def delete(self, collection_id):
    # Check if collection exists
    if not db[COLLECTION].find_one({'_id': ObjectId(collection_id)}):
      return { 'message': 'Unable to find collection.' }, 404
    # Remove collection from db
    try:
      db[COLLECTION].delete_one({'_id': ObjectId(collection_id)})
    except:
      return { 'message': 'Unable to remove collection.' }, 400
    return { 'message': f'Collection = {collection_id} has been removed from the database!' }, 200

  @api.doc(description='[Q4] Retrieve a collection.')
  @api.response(200, 'Successfully retreived collection.')
  @api.response(404, 'Unable to retreive collection.')
  def get(self, collection_id):
    try:
      collection = db[COLLECTION].find_one({'_id': ObjectId(collection_id)})
    except:
      return { 'message': 'Unable to find collection' }, 404
    return {
      'collection_id': str(collection['_id']),
      'indicator': collection['indicator'],
      'indicator_value': collection['indicator_value'],
      'creation_time': str(collection['creation_time']),
      'entries': collection['entries'],
    }, 200

@api.route(f'/{COLLECTION}/<collection_id>/<year>/<country>', endpoint=f'{COLLECTION}_countrydate')
@api.param('collection_id', f'Unique id, used to distinguish {COLLECTION}.')
@api.param('year', 'Year ranging from 2012 to 2017.')
@api.param('country', 'Country identifier (eg. Arab World)')
class CollectionByCountryYear(Resource):
  @api.doc(description='[Q5] Retrieve economic indicator value for given a country and year.')
  @api.response(200, 'Successfully retrieved economic indicator for given a country and year.')
  @api.response(400, 'Unable to retrieve indicator entry.')
  @api.response(404, 'Unable to find collection.')
  def get(self, collection_id, year, country):
    try:
      collection = db[COLLECTION].find_one({'_id': ObjectId(collection_id)})
    except:
      return { 'message': 'Unable to find collection' }, 404
    # Create a filtered list containing entries that match params
    filtered_entries = [
      entry for entry in collection['entries'] if entry['country'] == country and entry['date'] == year
    ]
    if len(filtered_entries) == 0:
      return {'message': 'Unable to find specific indicator entry ' \
              f'for country=\'{country}\' and year=\'{year}\'.'}, 400
    return {
      'collection_id': str(collection['_id']),
      'indicator': collection['indicator'],
      **filtered_entries[0],
    }, 200

@api.route(f'/{COLLECTION}/<collection_id>/<year>', endpoint=f'{COLLECTION}_by_top_bottom')
@api.param('collection_id', f'Unique id, used to distinguish {COLLECTION}.')
@api.param('year', 'Year ranging from 2012 to 2017.')
class CollectionByTopBottom(Resource):
  @api.doc(description='[Q6] Retrieve top/bottom economic indicator values for a given year.')
  @api.response(200, 'Successfully retreived economic indicator values.')
  @api.response(404, 'Unable to find collection.')
  @api.expect(parser)
  def get(self, collection_id, year):
    query = request.args.get('q')
    try:
      collection = db[COLLECTION].find_one({'_id': ObjectId(collection_id)})
    except:
      return { 'message': 'Unable to find collection' }, 404
    filtered_entries = [
      entry for entry in collection['entries'] if entry['date'] == year
    ]
    if not query:
      return {
        'indicator': collection['indicator'],
        'indicator_value': collection['indicator_value'],
        'entries': filtered_entries,
      }, 200
    return {
      'indicator': collection['indicator'],
      'indicator_value': collection['indicator_value'],
      'entries': sorted(
        filtered_entries,
        key=lambda k: k['value'],
        reverse=True
      )[query_to_index(query, len(filtered_entries))],
    }, 200

if __name__ == '__main__':
  db = mlab_client(
    dbuser=DB_CONFIG['dbuser'],
    dbpassword=DB_CONFIG['dbpassword'],
    mlab_inst=DB_CONFIG['mlab_inst'],
    dbname=DB_CONFIG['dbname']
  )
  app.run(debug=DEBUG)