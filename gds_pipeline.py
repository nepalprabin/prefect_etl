# -*- coding: utf-8 -*-
import datetime
import json
from math import ceil
import re
import time
import unicodedata
from xml.etree.ElementTree import fromstring, ElementTree, tostring
import numpy as np
import requests
from bs4 import BeautifulSoup

# custom
from es import elastic_upload
from helpers import save_to_json
from sql_helpers import sql_connector

es_ = elastic_upload()
mycursor, mydb = sql_connector()


mycursor.execute("CREATE TABLE gds_table(id INT, data TEXT)")
mycursor.execute("CREATE TABLE query_id(id INT)")


def get_data_from_html(response):
    soup = BeautifulSoup(response, "html.parser")
    text = re.sub(r'\t', '', soup.text)
    res = re.sub(r'\n', '', text)
    res = res.strip("1. ")   # remove "1. " present at the beginning of the data
    return res



def fetch_data_from_id(self, id, query):
    print('Here', id)
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&retmode=xml&tool=rex-ncbi&id={}'.format(id))
    if response.status_code == 400:
        raise RuntimeError("Invalid PMID/Search Query ({})".format(query))
    return get_data_from_html(response.content)



class GDS(object):

    def __init__(self, query):
        print('=====', query)
        ids = []
        json_dataset = []
        # query = 'covid'
        query_response = requests.get(
            'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&retmode=json&tool=rex-ncbi&term=%s&retmax=10' % str(query)).json()
        gds_list = query_response['esearchresult']['idlist']
        
    
        ids_json = {}
        # ids_json[query] = {json_ids}
        ids_json[query] = gds_list
        print(ids_json)
        es_.index(index="id-index1", id=1, document=json.dumps(ids_json))
        save_to_json('id_output.json', ids_json)

        if gds_list:
            i = 1
            for x in gds_list:
                print(x, '---', i)
                res = fetch_data_from_id(self, x, query)
                json_data = {}
                json_data['id'] = x
                json_data['data'] = res
                json_dataset.append(json_data)

                sql = "INSERT INTO gds_table (id, data) VALUES (%s, %s)"
                val = (x, res)
                mycursor.execute(sql, val)

                mydb.commit()

                i += 1
            save_to_json('json_output1.json', json_dataset)
        else:
            pass



obj = GDS("covid")