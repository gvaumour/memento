#!/usr/bin/env python

import os
import pyglet
import random
import logging

import server_management
import config 



window = pyglet.window.Window(fullscreen=True)

game_state_running = False
game_score = 0

picto_position = [ [window.width/2, window.height/2 + window.height*config.POS_PICTO_Y], 
                   [window.width/2, window.height/2 - window.height*config.POS_PICTO_Y],
                   [window.width/2 + window.width*config.POS_PICTO_X, window.height/2],
                   [window.width/2 - window.width*config.POS_PICTO_X, window.height/2], 
                   [window.width/2 + window.width*config.POS_PICTO_X, window.height/2 + window.height*config.POS_PICTO_Y],
                   [window.width/2 + window.width*config.POS_PICTO_X, window.height/2 - window.height*config.POS_PICTO_Y],
                   [window.width/2 - window.width*config.POS_PICTO_X, window.height/2 - window.height*config.POS_PICTO_Y],
                   [window.width/2 - window.width*config.POS_PICTO_X, window.height/2 + window.height*config.POS_PICTO_Y],
                   [window.width/2, window.height/2],
                ]

assert(len(picto_position) == config.TOTAL_PICTO)


def check_raspi_buttons():
    buttons_pressed = gpio_management.check_buttons()



def isCorrectPicto(picto_path):
    # To be improved with other criteria 
    if os.path.isfile(picto_path):
        return True

def resize_image(image, array):
    width = 400

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


def check_game_start(_):

    global game_score, game_state_running, timer
    
    if config.process_game_stop:
        if not game_state_running: 
            logging.warning("Attempting to stop a game already stopped ??")
        timer.running = False
        timer.reset()
        server_management.send_request_score(game_score)
        game_state_running = False
        config.process_game_stop = False
    
    if config.process_game_start:
        if game_state_running: 
            logging.warning("Attempting to start a game already started")
        timer.reset()
        timer.running = True
        game_state_running = True
        config.process_game_start = False


class Board:
    def __init__(self):
        self.started = True
        self.do_next_round()

    def do_next_round(self):
        self.displayed_noise_picto = [random.choice(sprite_noise_picto) for i in range(config.NB_NOISE_PICTO)]
        self.displayed_button_picto = random.choice(sprite_buttons_picto)

        list_of_position = random.sample(range(0,config.TOTAL_PICTO), config.TOTAL_PICTO)
        index = 0
        for pos in list_of_position: 
            if index == config.TOTAL_PICTO-1:
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
        self.label = pyglet.text.Label(str(config.ROUND_TIME), font_size=40, 
                                       x=(window.width - window.width*0.1), y=(window.height*0.1),
                                       anchor_x='center', anchor_y='center')
        self.reset()

    def reset(self):
        self.time = config.ROUND_TIME
        self.running = False
        self.label.text = str(config.ROUND_TIME)
        self.label.color = (255, 255, 255, 255)

    def update(self, dt):
        if self.running:
            self.time -= dt
            if (self.time <= 0):
                board.do_next_round()
                self.time = config.ROUND_TIME
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

    arc.draw()


path_buttons_picto = [os.path.join(config.PATH_BUTTONS_PICTO, f) for f in os.listdir(config.PATH_BUTTONS_PICTO) if isCorrectPicto(os.path.join(config.PATH_BUTTONS_PICTO, f))]
path_noise_picto = [os.path.join(config.PATH_NOISE_PICTO, f) for f in os.listdir(config.PATH_NOISE_PICTO) if isCorrectPicto(os.path.join(config.PATH_NOISE_PICTO, f))]


img_buttons_picto = [pyglet.image.load(f) for f in path_buttons_picto]
img_noise_picto = [pyglet.image.load(f) for f in path_noise_picto]

sprite_buttons_picto = []
sprite_noise_picto = []

resize_images()


background = pyglet.image.load( os.path.join(config.DIR_PATH, "./pictos/background.png"))
background.anchor_x = background.width // 2
background.anchor_y = background.height // 2
background_sprite = pyglet.sprite.Sprite(background, x=window.width//2, y = window.height//2)
background_sprite.scale = 2


# Instantiate the game elements
timer = Timer()
score = Score()
board = Board()
arc = pyglet.shapes.Arc(x=window.width//2, y= window.height//2, radius = 500, start_angle=90, color=(255, 0, 0))

waiting_label = pyglet.text.Label('MEMENTO', font_size=100, 
                                   x=window.width//2, y= window.height//2,
                                   anchor_x='center', anchor_y='center')

if __name__ == "__main__":
    pyglet.clock.schedule_interval(server_management.check_server_command, 1 / 30)
    pyglet.clock.schedule_interval(check_game_start, 1 / 30)
    pyglet.clock.schedule_interval(check_raspi_buttons, 1 / 30)
    pyglet.clock.schedule_interval(timer.update, 1/30.0)
    pyglet.app.run()




