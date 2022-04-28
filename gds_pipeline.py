# -*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
from contextlib import closing
import sqlite3
import pandas as pd

# prefect
from prefect import task, Flow, Parameter

# elasticsearch
from elasticsearch import helpers


# custom
from es import elastic_upload
from utils import save_to_json
from sql_helpers import sql_connector

es_ = elastic_upload()
mycursor, mydb = sql_connector()


def get_data_from_html(response):
    soup = BeautifulSoup(response, "html.parser")
    text = re.sub(r'\t', '', soup.text)
    res = re.sub(r'\n', '', text)
    res = res.strip("1. ")   # remove "1. " present at the beginning of the data
    if '(Submitter supplied)' in res:
        result = res.split('(Submitter supplied)') # title is differentiated by (Submitter supplied) term. So, splitting title with content with this term
        if len(result) == 2:
            stripped_res = result[1].strip()
            return result[0], stripped_res
        else:
            return res
    return res



def fetch_data_from_id(id, query):
    print('Here', id)
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&retmode=xml&tool=rex-ncbi&id={}'.format(id))
    if response.status_code == 400:
        raise RuntimeError("Invalid PMID/Search Query ({})".format(query))
    return get_data_from_html(response.content)



def store_json_data(result):
    save_to_json('gds_data.json', result)


def store_id_data(result):
    save_to_json('gds_id_data.json', result)



@task
def fetch_data_from_query(query):
    query_response = requests.get(
            'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&retmode=json&tool=rex-ncbi&term=%s&retmax=1000' % str(query)).json()
    gds_list = query_response['esearchresult']['idlist']     

    all_data = []
    json_dataset = []
    ids_json = {}
    for i in gds_list:
        res = fetch_data_from_id(i, query)
        json_data = {}
        json_data['id'] = i
        json_data['title'] = res[0]
        json_data['data'] = res[1]
        ids_json[query] = gds_list
        json_dataset.append(json_data)
        all_data.append([i, res[0], res[1]])
    es_.index(index="id-index1", id=1, document=json.dumps(ids_json))
    helpers.bulk(es_, json_dataset, index='gds-data',)
    # es_.index(index="gds-data", id=2, document=json.dump(json_dataset))
    store_id_data(ids_json)
    store_json_data(json_dataset)
    return all_data


@task
def store_gds_data(parsed):
    create_script = 'CREATE TABLE IF NOT EXISTS gds_table (id INT, title TEXT, data TEXT)'
    insert_cmd = "INSERT INTO gds_table VALUES (?, ?, ?)"

    with closing(sqlite3.connect("gds_data.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executescript(create_script)
            cursor.executemany(insert_cmd, parsed)
            conn.commit()



with Flow("gds-flow") as f:
    query = Parameter('covid', default='covid')
    parsed = fetch_data_from_query(query)
    store_gds_data(parsed)

f.run()