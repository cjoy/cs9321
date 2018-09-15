#!/usr/bin/env python3
from flask import Flask, request
from flask_restplus import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests, datetime, re

#------------- CONFIG CONSTANTS -------------#

MAX_PAGE_LIMIT = 2
COLLECTION = 'indicators'
DB_CONFIG = {
  'dbuser': 'z5113243',
  'dbpassword': 'badpassword01',
  'mlab_inst': 'ds239071',
  'dbname': 'cs9321_ass2' 
}

app = Flask(__name__)
api = Api(app)
db = None

#------------- HELPER FUNCTIONS -------------#

def mlab_client(dbuser, dbpassword, mlab_inst, dbname):
  return MongoClient(
    f'mongodb://{dbuser}:{dbpassword}@{mlab_inst}.mlab.com:39071/{dbname}'
  )[dbname]

def api_url(indicator, date='2012:2017', format='json', page=1):
  return 'http://api.worldbank.org/v2/countries/all/indicators/' \
          f'{indicator}?date={date}&format={format}&page={page}'

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
def format_indicator_entry(indicator_data):
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
  except:
     return slice(arr_size)

#------------- QUESTION ROUTES -------------#

@api.route(f'/{COLLECTION}')
class CollectionIndex(Resource):
  # Q1 - Import a collection from the data service
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
    # From now onwards we need to get data from the Worldbank API
    indicator_data = get_indicator_data(indicator=body['indicator_id'])
    # Valid indicator hasn't been specified (400)
    if indicator_data == 'Invalid indicator':
      return { 'message': 'Please specify a valid indicator.' }, 400
    # Create and retrieve indicator from Worldbank API (201)
    indicator = {
      'indicator': indicator_data[0]['indicator']['id'],
      'indicator_value': indicator_data[0]['indicator']['value'],
      'creation_time': datetime.datetime.utcnow(),
      'entries': [format_indicator_entry(entry) for entry in indicator_data],
    }
    created_collection = db[COLLECTION].insert_one(indicator)
    return {
      'location': f'/{COLLECTION}/{str(created_collection.inserted_id)}',
      'collection_id': str(created_collection.inserted_id),
      'creation_time': str(indicator['creation_time']),
      'indicator': indicator['indicator'],
    }, 201

  # Q3 - Retrieve the list of available collections
  def get(self):
    return [{
      'location': f'/{COLLECTION}/{str(doc["_id"])}',
      'collection_id': str(doc['_id']),
      'creation_time': str(doc['creation_time']),
      'indicator': doc['indicator'],
    } for doc in db[COLLECTION].find()], 200

@api.route(f'/{COLLECTION}/<collection_id>')
class CollectionsById(Resource):
  # Q2 - Deleting a collection with the data service
  def delete(self, collection_id):
    # Check if collection exists
    if not db[COLLECTION].find_one({'_id': ObjectId(collection_id)}):
      return { 'message': 'Unable to delete indicator.' }, 400
    # Remove collection from db
    db[COLLECTION].delete_one({'_id': ObjectId(collection_id)})
    return { 'message': f'Collection = {collection_id} is removed from the database!' }, 200

  # Q4 - Retrieve a collection
  def get(self, collection_id):
    if not db[COLLECTION].find_one({'_id': ObjectId(collection_id)}):
      return { 'message': 'Unable to retrieve indicator.' }, 400
    collection = db[COLLECTION].find_one({'_id': ObjectId(collection_id)})
    return {
      'collection_id': str(collection['_id']),
      'indicator': collection['indicator'],
      'indicator_value': collection['indicator_value'],
      'creation_time': str(collection['creation_time']),
      'entries': collection['entries'],
    }, 200

@api.route(f'/{COLLECTION}/<collection_id>/<date>/<country>')
class CollectionByCountryYear(Resource):
  # Q5 - Retrieve economic indicator value for given country and a year
  def get(self, collection_id, date, country):
    collection = db[COLLECTION].find_one({'_id': ObjectId(collection_id)})      
    if not collection:
      return { 'message': 'Unable to retrieve indicator.' }, 400
    # Create a filtered list containing entries that match params
    filtered_entries = [
      entry for entry in collection['entries'] if entry['country'] == country and entry['date'] == date
    ]
    if len(filtered_entries) == 0:
      return { 'message': f'Unable to find specific indicator entry.' }, 400
    return {
      'collection_id': str(collection['_id']),
      'indicator': collection['indicator'],
      **filtered_entries[0],
    }, 200

@api.route(f'/{COLLECTION}/<collection_id>/<date>')
class CollectionByTopBottom(Resource):
  # Q6 - Retrieve top/bottom economic indicator values for a given year
  def get(self, collection_id, date):
    query = request.args.get('q')
    collection = db[COLLECTION].find_one({'_id': ObjectId(collection_id)})      
    if not collection:
      return { 'message': 'Unable to retrieve indicator' }, 400
    if not query:
      return {
        'indicator': collection['indicator'],
        'indicator_value': collection['indicator_value'],
        'entries': collection['entries'],
      }, 200
    return {
      'indicator': collection['indicator'],
      'indicator_value': collection['indicator_value'],
      'entries': sorted(
        collection['entries'], key=lambda k: k['value'],
        reverse=True
      )[query_to_index(query, len(collection['entries']))],
    }, 200

if __name__ == '__main__':
  db = mlab_client(
    dbuser=DB_CONFIG['dbuser'],
    dbpassword=DB_CONFIG['dbpassword'],
    mlab_inst=DB_CONFIG['mlab_inst'],
    dbname=DB_CONFIG['dbname']
  )
  app.run(debug=True)
