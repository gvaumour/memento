import json 


def is_stdin_ready():
    read, _, _ = select.select([sys.stdin.fileno()], [], [], 0.0)
    return bool(read)


def check_command(_):
    global total
    if not is_stdin_ready():
        return

    command = sys.stdin.readline().strip()
    parse_json_request(command)


def handle_request_error(dct):
	logging.error("JSON Request is not formated properly")
	logging.error(dct)


def parse_json(request):

	global ROOM_ID
	global game_state_running
	dct = json.loads(request)

	# Expecting event/value keys in the request
	if "event" not in dct or "value" not in dct:
		handle_request_error()

	# Request is not for me, drop it
	if dct["value"] != ROOM_ID:
		return

	if dct["event"] == "roomStarted":
		process_game_start()
	elif dct["event"] == "roomStopped":
		process_game_stop()
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
    global ROOM_ID
	request = dict()
	request["event"] = "setScore"
	request["value"] = { "idRoom" : ROOM_ID, "score" : score}

	print(json.dumps(request))
