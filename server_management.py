import json 

def handle_request_error(dct):
	print("Request is not formated properly")
	print(dct)

def parse_json(request, room_id):
	dct = json.loads(request)

	# Expecting event/value keys in the request
	if "event" not in dct or "value" not in dct:
		handle_request_error()

	# Request is not for me, drop it
	if dct["value"] != room_id:
		return

	if dct["event"] == "roomStarted":
		if game_state_running: 
			print("Game is already running ??")
		game_state_running = True

	elif dct["event"] == "roomStopped":
		if not game_state_running: 
			print("Game is already stopped ??")
		game_state_running = Flase
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
def send_request_score(score, room_id):
	request = dict()
	request["event"] = "setScore"
	request["value"] = { "idRoom" : room_id , "score" : score}

	print(json.dumps(request))
