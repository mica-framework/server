from flask import json, jsonify, request
from . import routes, __create_response__
from redis_db import attacks
from influx import *


# In here we're getting the meta information on processed attack.
# Those information are logged within a database and will be used
# for mapping the general collected log data, to those meta information.
# With this mapping, we're able to identify the malicious event logs
# ====
# Receiving: JSON
# Format:
# {data: [{
#      'hostname': 'IM-SEC-001', # must
#      'date': "2019-05-20" # must
#      'time': fields[0], # must
#      'protocol': fields[1], # must
#      'from': fields[2], # not a must
#      'to': fields[4], # not a must
#      'message': '' # must
# },...]
# }
@routes.route('log', methods=['POST'])
def log_attack():

    # get the request data
    req = request.get_data(as_text=True)
    req_data = json.loads(str(req))
    data = req_data['data']
    print('Received the following data: {}'.format(data))

    # check if we got an object, if we only have a signle object,
    # then we should put that in an array for further processes
    if isinstance( data, (object) ) and not isinstance( data, (tuple, list)):
        data = [data]

    # now we need to write the infos to influx
    if len(data) > 0:
        batch = []
        for item in data:
            
            # create the tags dictionary
            tags = { 'hostname': item['hostname'], 'date': item['date'], 'timestamp': item['timestamp'] }
            
            # remove the fields from the item, which are used as a tag
            item.pop('hostname', None) 
            item.pop('date', None) 
            item.pop('timestamp', None) 

            # save the point for batch-processing
            batch.append(build_point("container_traffic", data=item, tags=tags))

        if len(batch) > 0:
            print('Storing {} points in influx..'.format(len(batch)))
            write_batch(batch)

        # finished the write
        return __create_response__(200, message='success')
    else:
        return __create_response__(500, message='received an empty data body')



@routes.route('attack/start', methods=['POST'])
def attack_start():
    
    # get the request data
    req = request.get_data(as_text=True)
    data = json.loads(str(req))

    # at first we need the hostname and command which was executed
    hostname = data['hostName']
    command = data['command']
    uuid = data['uuid']
    
    # at first write that into redis
    attacks.job_start(hostname, command, uuid)

    # finished the state update
    return __create_response__(200, message='success')


@routes.route('attack/end', methods=['POST'])
def attack_end():
    
    # get the request data
    req = request.get_data(as_text=True)
    data = json.loads(str(req))

    # at first we need the hostname and command which was executed
    hostname = data['hostName']
    uuid = data['uuid']

    # get the job details first
    job = attacks.get_running_job(hostname, uuid)
    
    # at first write that into redis
    attacks.job_end(hostname, uuid)

    # now write it into influx -> start + end
    write('attack_history', {
        "command": job['command'],
        "started_timestamp": job['started'],
        "ended_timestamp": datetime.now().timestamp()
        }, tags={'hostname': hostname, "uuid": str(uuid) })

    # finished the state update
    return __create_response__(200, message='success')


@routes.route('empty', methods=['POST','GET','PUT','DELETE'])
def empty_endpoint():
    return __create_response__(200, message='Empty endpoint! This endpoint exists only to simulate a successfull HTTP-Request')
