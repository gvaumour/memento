import select
import json 
import sys
import os
import logging
import config

def is_stdin_ready():
    read, _, _ = select.select([sys.stdin.fileno()], [], [], 0.0)
    return bool(read)


def check_server_command(_):

    if not is_stdin_ready():
        return

    command = sys.stdin.readline().strip()
    if not command or command == '\n': 
        return 
    #print(command)
    parse_json_request(command)


def handle_request_error(dct):
    logging.error("JSON Request is not formated properly")
    logging.error(dct)

def handle_stop_pc():
    logging.warning("Receive stop request, shutting the PC down")
    os.system("sudo shutdown -h now")

def parse_json_request(request):

    
    dct = dict()
    try:
        dct = json.loads(request)
    except ValueError: 
        logging.error("Request is not properly formated in JSON")
        return

    if dct is None or type(dct) is int: 
        logging.error("Request is not properly formated in JSON")
        return

    # Expecting event/value keys in the request
    if "event" not in dct or "value" not in dct:
        handle_request_error()


    if dct["event"] == "stopAllPC":
        handle_stop_pc()

    # Request is not for me, drop it
    if int(dct["value"]) != config.ROOM_ID:
        return

    if dct["event"] == "roomStarted":
        logging.info("Received a game start event")
        config.process_game_start = True
    elif dct["event"] == "roomStopped":
        logging.info("Received a game stop event")
        config.process_game_stop = True
    elif dct["event"] == "stopPC":
        handle_stop_pc()
    else:
        handle_request_error(dct)

#
#{
#  "event": "setScore",
#  "value": {
#    "idRoom": 7,
#    "score": 10500
#  }
#}
def send_request_score(score):
    request = dict()
    request["event"] = "setScore"
    request["value"] = { "idRoom" : config.ROOM_ID, "score" : score}

    print(json.dumps(request))
