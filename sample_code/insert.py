import csv
import datetime
import hashlib
import time

import pandas as pd
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import scan
from tqdm.notebook import tqdm

ES_INDEX = "test_000001"
ES_HOST = "0.0.0.0:52200"
ELASTIC_USER = "elastic"
ELASTIC_PASSWORD = "hi1234es"
ES_TIMEOUT = 60 * 10
md5 = lambda x: hashlib.md5(x.encode("utf-8")).hexdigest()


class es_connect:
    def __init__(self):
        self.es_client = None
        self.connect()

    def connect(self):
        http_auth = (ELASTIC_USER, ELASTIC_PASSWORD)
        es = Elasticsearch([ES_HOST], http_auth=http_auth)
        self.es_client = es


def insert_data(data, index):
    ss_bulk = time.time()
    ES_CLIENT = Elasticsearch(
        [ES_HOST],
        timeout=ES_TIMEOUT,
        http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    )
    state_response = helpers.bulk(ES_CLIENT, data)
    cost = round(time.time() - ss_bulk, 4)
    print(f"{index},{state_response},time:{cost}")


def rec_to_actions(df):
    for record in df.to_dict(orient="records"):

        es_uuid = f"{record['id']}_{record['title']}_{record['page_url']}_{record['post_time']}"
        _id = md5(es_uuid)
        res = {"_op_type": "index", "_index": ES_INDEX, "_id": _id, "_source": record}
        yield res


if __name__ == "__main__":

    es = es_connect()
    ss = time.time()
    df = pd.read_csv("sample_data.csv")
    df.post_time = df.post_time.astype("datetime64[ns]")
    df["post_time"] = df["post_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["id"] = [x for x in range(len(df))]
    old_i = 0
    pace = 50000
    length = len(df)

    if length < pace:

        ss_bulk = time.time()
        helpers.bulk(es.es_client, rec_to_actions(df))
        print(round(time.time() - ss_bulk, 4))

    for i in range(pace, length, pace):
        print(old_i, i)
        ss_bulk = time.time()
        helpers.bulk(
            es.es_client,
            rec_to_actions(
                df.loc[
                    old_i:i,
                ]
            ),
        )
        print(round(time.time() - ss_bulk, 4))
        old_i = i + 1
        if length // pace == i // pace:
            print(old_i, length)
            helpers.bulk(
                es.es_client,
                rec_to_actions(
                    df.loc[
                        old_i:i,
                    ]
                ),
            )
    cost = round(time.time() - ss, 4)
    print(cost)
