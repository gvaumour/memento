import os

################################# 
# GAME PARAMETERS 

ROOM_ID = 15          # ID used to identify the room by the server
ROUND_TIME = 10       # Number of seconds per round 
NB_NOISE_PICTO = 9    # Number of picto displayed on top of the correct one
TOTAL_PICTO = NB_NOISE_PICTO + 1
POINTS_PER_ROUND = 10 # Number of points per good answer

POS_PICTO_X = 0.17    # Ratio for positionning picto X axis 
POS_PICTO_Y = 0.27    # Ratio for positionning picto Y axis 

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# There are 40 buttons, each picto is attached to 4 buttons:4x10
NB_BUTTONS = 10

# Pictos printed on buttons 
PATH_BUTTONS_PICTO = os.path.realpath(os.path.join(DIR_PATH, "./assets/images/picto_button"))

# Picto not printed on buttons, they are called noise pictos
PATH_NOISE_PICTO = os.path.realpath(os.path.join(DIR_PATH, "./assets/images/picto_noise"))

process_game_start = False
process_game_stop = False

color_azur = (33, 163 , 179)
color_lavande = (64, 70 , 153)
color_black = (2, 2 , 2, 255)


## Launching configuration to smooth problems between ssh remote connection / windows non compatibility
# For some reason, playing sound from a remote X11 session on raspberry is tricky 
SOUND_MANAGEMENT = False # Must be True on production

# If flag raised, all Windows-specific stuff is not handled such as buttons press and server management
# It allows to test on windows the game
RUNNING_ON_WINDOW = False # Must be False on production

################################# 
