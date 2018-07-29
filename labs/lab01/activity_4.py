#!/usr/local/bin/python3
import requests
import pandas

def fetch_data(url):
    response = requests.get(url)
    return response.json()

def read_response_to_dataframe(response_object):
    data = response_object['data']
    columns = [column['name'] for column in response_object['meta']['view']['columns']]
    dataframe = pandas.DataFrame(data=data, columns=columns)
    return dataframe

def main():
    url = 'https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json'
    response_object = fetch_data(url)
    dataframe = read_response_to_dataframe(response_object)

if __name__ == "__main__":
    main()