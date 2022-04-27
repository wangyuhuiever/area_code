# -*- coding: utf-8 -*-
from bson import ObjectId
import json
import datetime
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


class DataToJSON(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime(DATETIME_FORMAT)
        elif isinstance(0, datetime.date):
            return o.strftime(DATE_FORMAT)
        return json.JSONEncoder.default(self, o)


def dumps(data):
    return json.dumps(data, cls=DataToJSON)


def format_pure_json(data):
    d = dumps(data)
    return json.loads(d)
