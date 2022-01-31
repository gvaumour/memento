#!/usr/bin/env python

import os
import pyglet
import random
import logging

import server_management

dir_path = os.path.dirname(os.path.realpath(__file__))

# Pictos printed on buttons 
PATH_BUTTONS_PICTO = os.path.realpath(os.path.join(dir_path, "./pictos/picto_button"))

# Picto not printed on buttons, they are called noise pictos
PATH_NOISE_PICTO = os.path.realpath(os.path.join(dir_path, "./pictos/picto_noise"))


################################# 
# GAME PARAMETERS 

ID_ROOM = 15          # ID used to identify the room by the server
ROUND_TIME = 10       # Number of seconds per round 
NB_NOISE_PICTO = 8    # Number of picto displayed on top of the correct one
TOTAL_PICTO = NB_NOISE_PICTO + 1
POINTS_PER_ROUND = 10 # Number of points per good answer

POS_PICTO_X = 0.17    # Ratio for positionning picto X axis 
POS_PICTO_Y = 0.27    # Ratio for positionning picto Y axis 

################################# 


window = pyglet.window.Window(fullscreen=True)

game_state_running = False

picto_position = [ [window.width/2, window.height/2 + window.height*POS_PICTO_Y], 
                   [window.width/2, window.height/2 - window.height*POS_PICTO_Y],
                   [window.width/2 + window.width*POS_PICTO_X, window.height/2],
                   [window.width/2 - window.width*POS_PICTO_X, window.height/2], 
                   [window.width/2 + window.width*POS_PICTO_X, window.height/2 + window.height*POS_PICTO_Y],
                   [window.width/2 + window.width*POS_PICTO_X, window.height/2 - window.height*POS_PICTO_Y],
                   [window.width/2 - window.width*POS_PICTO_X, window.height/2 - window.height*POS_PICTO_Y],
                   [window.width/2 - window.width*POS_PICTO_X, window.height/2 + window.height*POS_PICTO_Y],
                   [window.width/2, window.height/2],
                ]

assert(len(picto_position) == TOTAL_PICTO)


def isCorrectPicto(picto_path):
    # To be improved with other criteria 
    if os.path.isfile(picto_path):
        return True

def resize_image(image, array):
    width = 512

    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    image_sprite = pyglet.sprite.Sprite(image, x=window.width//2, y = window.height//2)
    image_sprite.scale = width / window.width
    array.append(image_sprite)

def resize_images():
    for image in img_buttons_picto:
        resize_image(image, sprite_buttons_picto)
    for image in img_noise_picto:
        resize_image(image, sprite_noise_picto)


def process_game_stop():
    if not game_state_running: 
        logging.warning("Attempting to stop a game already stopped ??")
    
    game_state_running = False
    timer.running = False
    timer.reset()

def process_game_start():
	if game_state_running: 
	    logging.warning("Attempting to start a game already started")
    game_state_running = True
    timer.reset()
    timer.running = True
    game_state_running = True


class Board:
    def __init__(self):
        self.started = True
        self.do_next_round()

    def do_next_round(self):
        self.displayed_noise_picto = [random.choice(sprite_noise_picto) for i in range(NB_NOISE_PICTO)]
        self.displayed_button_picto = random.choice(sprite_buttons_picto)

        list_of_position = random.sample(range(0,TOTAL_PICTO), TOTAL_PICTO)
        index = 0
        for pos in list_of_position: 
            if index == TOTAL_PICTO-1:
                self.displayed_button_picto.x = picto_position[pos][0]
                self.displayed_button_picto.y = picto_position[pos][1]
            else :
                self.displayed_noise_picto[index].x = picto_position[pos][0]
                self.displayed_noise_picto[index].y = picto_position[pos][1]
                index = index + 1


class Score:
    def __init__(self):
        self.label = pyglet.text.Label('Score: 000', font_size=40, 
                                       x=(window.width - window.width*0.1), y=(window.height - window.height*0.1),
                                       anchor_x='center', anchor_y='center')
        self.reset()

    def reset(self):
        self.score = 0
        self.label.text = 'Score: 000'
        self.label.color = (255, 255, 255, 255)

    def update(self, dt):
        self.score = self.score + POINTS_PER_ROUND
        self.label.text = 'Score: %03d' % (self.score)


class Timer:
    def __init__(self):
        self.label = pyglet.text.Label(str(ROUND_TIME), font_size=40, 
                                       x=(window.width - window.width*0.1), y=(window.height*0.1),
                                       anchor_x='center', anchor_y='center')
        self.reset()

    def reset(self):
        self.time = ROUND_TIME
        self.running = False
        self.label.text = str(ROUND_TIME)
        self.label.color = (255, 255, 255, 255)

    def update(self, dt):
        if self.running:
            self.time -= dt
            if (self.time <= 0):
                board.do_next_round()
                self.time = ROUND_TIME
            self.label.text = '%01d' % (round(self.time))




@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        window.close()


@window.event
def on_draw():
    window.clear()

    background_sprite.draw()

    if game_state_running == True: 
        timer.label.draw()
        score.label.draw()

        board.displayed_button_picto.draw()
        for sprites in board.displayed_noise_picto:
            sprites.draw()

    else: 
        waiting_label.draw()


path_buttons_picto = [os.path.join(PATH_BUTTONS_PICTO, f) for f in os.listdir(PATH_BUTTONS_PICTO) if isCorrectPicto(os.path.join(PATH_BUTTONS_PICTO, f))]
path_noise_picto = [os.path.join(PATH_NOISE_PICTO, f) for f in os.listdir(PATH_NOISE_PICTO) if isCorrectPicto(os.path.join(PATH_NOISE_PICTO, f))]


img_buttons_picto = [pyglet.image.load(f) for f in path_buttons_picto]
img_noise_picto = [pyglet.image.load(f) for f in path_noise_picto]

sprite_buttons_picto = []
sprite_noise_picto = []

resize_images()


background = pyglet.image.load( os.path.join(dir_path, "./pictos/background.png"))
background.anchor_x = background.width // 2
background.anchor_y = background.height // 2
background_sprite = pyglet.sprite.Sprite(background, x=window.width//2, y = window.height//2)
background_sprite.scale = 2



if __name__ == "__main__":
    
    # Instantiate the game elements
    timer = Timer()
    score = Score()
    board = Board()

    waiting_label = pyglet.text.Label('Waiting for game to start', font_size=100, 
                                       x=window.width//2, y= window.height//2,
                                       anchor_x='center', anchor_y='center')


    server_management.send_request_score(100, ID_ROOM)

    pyglet.clock.schedule_interval(check_server_command, 1 / 30)

    pyglet.clock.schedule_interval(timer.update, 1/30.0)
    pyglet.app.run()




