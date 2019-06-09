from influxdb import InfluxDBClient
from config import config
from datetime import datetime
from flask import json

# initially get the configuration
HOST = config['database']['influx']['url']
PORT = config['database']['influx']['port']
USER = config['database']['influx']['user']
PASS = config['database']['influx']['password']
TABLE = config['database']['influx']['tablename']

# create a client instance
_influx_client = InfluxDBClient(HOST, PORT, USER, PASS)

# now check if the mica database does exist and create it if not
databases = _influx_client.get_list_database()
database_names = [db['name'] for db in databases]
if TABLE not in database_names:
    _influx_client.create_database(TABLE)

# so the database should exist now, let's swith to the mica-db
_influx_client.switch_database(TABLE)

def build_point(measurement, data, tags={}, time=datetime.now()):

    # create the entry
    return {
        "measurement": measurement,
        "tags": tags,
        "time": time,
        "fields": data
    }


# writing a measurement to the database
def write(measurement, data, tags={}, time=datetime.now()):
    
    # do not write any empty things!
    if measurement is None or data is None:
        return False

    # create the entry
    entry = [build_point(measurement, data, tags, time)]

    # now write the entry
    return write_batch(entry)


# writing a measurement batch to the database
def write_batch(batch=[]):
    
    # do not write any empty things!
    if batch is None or len(batch) <= 0:
        return False

    # now write the entry
    return _influx_client.write_points(batch, protocol='json', batch_size=len(batch))
