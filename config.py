import os

################################# 
# GAME PARAMETERS 

ROOM_ID = 15          # ID used to identify the room by the server
ROUND_TIME = 10       # Number of seconds per round 
NB_NOISE_PICTO = 8    # Number of picto displayed on top of the correct one
TOTAL_PICTO = NB_NOISE_PICTO + 1
POINTS_PER_ROUND = 10 # Number of points per good answer

POS_PICTO_X = 0.17    # Ratio for positionning picto X axis 
POS_PICTO_Y = 0.27    # Ratio for positionning picto Y axis 

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# There are 40 buttons, each picto is attached to 2 buttons
NB_BUTTONS = 20

# Pictos printed on buttons 
PATH_BUTTONS_PICTO = os.path.realpath(os.path.join(DIR_PATH, "./pictos/picto_button"))

# Picto not printed on buttons, they are called noise pictos
PATH_NOISE_PICTO = os.path.realpath(os.path.join(DIR_PATH, "./pictos/picto_noise"))

process_game_start = False
process_game_stop = False

################################# 
