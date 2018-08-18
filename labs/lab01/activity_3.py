#!/usr/bin/env python3
from activity_1 import get_dataframe_from_csv
from pymongo import MongoClient
import json
import pandas

def connect_to_mongo(host, port, db):
    client = MongoClient(host, port)
    return client[db]

def store_dataframe_to_mongo(connection, dataframe, collection):
    records = json.loads(dataframe.T.to_json()).values()
    connection[collection].insert_many(records)

def read_mongo_to_dataframe(connection, collection):
    dataframe = pandas.DataFrame(list(connection[collection].find()))
    return dataframe

def main():
    dataframe = get_dataframe_from_csv('dataset.csv')
    collection = 'demographic_statistics'
    connection = connect_to_mongo('localhost', 27017, 'comp9321')
    store_dataframe_to_mongo(connection, dataframe, collection)
    dataframe_from_db = read_mongo_to_dataframe(connection, collection)

if __name__ == "__main__":
    main()
    