#!/bin/bash 

set -o pipefail

DEFAULT_PORT=12345
DEFAULT_SERVER="ws://minecraft.mrskyzz.fr"


usage() {

	echo "This script launches the 1055/Memento game"
	echo "This script tries to connect every second to the websocket server, then launch the game"
	echo "If the game crashes or gets disconnected, the game restarts" 
	echo "By default, the websocket server address used is ${DEFAULT_SERVER}:${DEFAULT_PORT}"
	echo "Usage: launch_forever.sh --port PORT --server SERVER"
}

PORT=${DEFAULT_PORT}
SERVER=${DEFAULT_SERVER}


while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--port)
      PORT="$2"
      shift # past argument
      shift # past value
      ;;
    -s|--server)
      SERVER="$2"
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      usag
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      usage
      shift # past argument
      ;;
  esac 
done

CURRENT_DIR=$( dirname -- "${BASH_SOURCE[0]}" )
cd $CURRENT_DIR

if [ -p "fifo_memento" ];then 
	rm fifo_memento
	mkfifo fifo_memento
fi

while :
do
	echo "Connecting to the websocket server $SERVER:$PORT ..."
	tail -f fifo_memento | websocat -E $SERVER:$PORT | python ./memento_game.py > fifo_memento
	echo "Memento game has been stopped, attempt to relaunching it"
	sleep 1
done



