import os
import re
import csv
import sys
import jsonlines
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

es = Elasticsearch()

class CsvIndexer:
    def __init__(self, csv_path, es_host='localhost', es_port=9200, es_index='csv_data', es_doc_type='entry'):
        self.csv_path = csv_path
        self.es_host = es_host
        self.es_port = es_port
        self.es_index = es_index
        self.es_doc_type = es_doc_type
        self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        self.create_index()

    def create_index(self):
        if not self.es.indices.exists(self.es_index):
            self.es.indices.create(index=self.es_index, body={
                'mappings': {
                    self.es_doc_type: {
                        'properties': {
                            'reviews': {'type': 'text'},
                            'msc': {'type': 'text'},
                            'id': {'type': 'text'},
                            # add more fields as needed
                        }
                    }
                }
            })

    def index_csv(self):
        with open(self.csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # skip the header row

            for row in reader:
                doc = {}
                doc['field1'] = row[0]
                doc['field2'] = row[1]
                doc['field3'] = row[2]

                self.es.index(index=self.es_index, doc_type=self.es_doc_type, body=doc)
