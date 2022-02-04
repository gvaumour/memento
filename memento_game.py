#!/usr/bin/env python

import os
import pyglet
import random
import logging

import gpio_management
import server_management
import config 



window = pyglet.window.Window(fullscreen=True)

game_state_running = True
game_score = 0

picto_position = [ [window.width/2+25, window.height/2 + window.height*config.POS_PICTO_Y+35], 
                   [window.width/2-40, window.height/2 - window.height*config.POS_PICTO_Y-50],
                   [window.width/2 + window.width*config.POS_PICTO_X-32, window.height/2-19],
                   [window.width/2 - window.width*config.POS_PICTO_X+48, window.height/2+30], 
                   [window.width/2 + window.width*config.POS_PICTO_X-50, window.height/2 + window.height*config.POS_PICTO_Y-44],
                   [window.width/2 + window.width*config.POS_PICTO_X+34, window.height/2 - window.height*config.POS_PICTO_Y-25],
                   [window.width/2 - window.width*config.POS_PICTO_X+58, window.height/2 - window.height*config.POS_PICTO_Y+12],
                   [window.width/2 - window.width*config.POS_PICTO_X + 45, window.height/2 + window.height*config.POS_PICTO_Y-32],
                   [window.width/2+66, window.height/2-100],
                   [window.width/2-45, window.height/2+70],
                ]

assert(len(picto_position) == config.TOTAL_PICTO)


def check_raspi_buttons(dt):
    return
    #buttons_pressed = gpio_management.check_buttons(dt)


def isCorrectPicto(picto_path):
    # To be improved with other criteria 
    if os.path.isfile(picto_path):
        return True

def resize_image(image, array):
    width = 450

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
        self.displayed_noise_picto = random.sample(sprite_noise_picto, k = config.NB_NOISE_PICTO)
        self.displayed_button_picto = random.sample(sprite_buttons_picto, k = 1)[0]

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
        self.label = pyglet.text.Label('Score: 000', font_size=40, font_name="Gobold_Light",
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
        self.pi = 3.14159
        self.label = pyglet.text.Label(str(config.ROUND_TIME), font_size=40, font_name="Gobold_Light",
                                       x=(window.width - window.width*0.1), y=(window.height*0.1),
                                       anchor_x='center', anchor_y='center')
                                       
        self.label.color = config.color_black                                       
        self.background_circle = pyglet.shapes.Circle( x=(window.width - window.width*0.1), y=(window.height*0.1), radius = 40, color = config.color_azur)
        self.front_circle = pyglet.shapes.Sector( x=(window.width - window.width*0.1), y=(window.height*0.1),
                                        radius = 41, color =config.color_lavande, start_angle = self.pi / 2, angle = 0)
        self.reset()

    def reset(self):
        self.time = config.ROUND_TIME
        self.running = False
        self.label.text = str(config.ROUND_TIME)


    def generate_front_circle(self):
        my_angle  = 2 * self.pi - (2 * self.pi * (10-self.time) / config.ROUND_TIME)
        self.front_circle = pyglet.shapes.Sector( x=(window.width - window.width*0.1), y=(window.height*0.1),
                                        radius = 41, color = config.color_lavande, start_angle = self.pi / 2, angle = my_angle)

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
        timer.background_circle.draw()
        timer.generate_front_circle()
        timer.front_circle.draw()
        timer.label.draw()

        score.label.draw()
        board.displayed_button_picto.draw()
        for sprites in board.displayed_noise_picto:
            sprites.draw()

    else: 
        waiting_label.draw()


path_buttons_picto = [os.path.join(config.PATH_BUTTONS_PICTO, f) for f in os.listdir(config.PATH_BUTTONS_PICTO) if isCorrectPicto(os.path.join(config.PATH_BUTTONS_PICTO, f))]
path_noise_picto = [os.path.join(config.PATH_NOISE_PICTO, f) for f in os.listdir(config.PATH_NOISE_PICTO) if isCorrectPicto(os.path.join(config.PATH_NOISE_PICTO, f))]

img_buttons_picto = [pyglet.image.load(f) for f in path_buttons_picto]
img_noise_picto = [pyglet.image.load(f) for f in path_noise_picto]

sprite_buttons_picto = []
sprite_noise_picto = []

resize_images()


background = pyglet.image.load( os.path.join(config.DIR_PATH, "./assets/images/background.png"))
background.anchor_x = background.width // 2
background.anchor_y = background.height // 2
background_sprite = pyglet.sprite.Sprite(background, x=window.width//2, y = window.height//2)
background_sprite.scale = 2

pyglet.font.add_file(os.path.join(config.DIR_PATH, "./assets/fonts/Gobold_Light.ttf"))
gobold_light = pyglet.font.load("Gobold_Light.ttf")

# Instantiate the game elements
timer = Timer()
score = Score()
board = Board()
timer.running =  True

waiting_label = pyglet.text.Label('MEMENTO', font_size=100, 
                                   x=window.width//2, y= window.height//2,
                                   anchor_x='center', anchor_y='center')

if __name__ == "__main__":
    pyglet.clock.schedule_interval(server_management.check_server_command, 1 / 30)
    pyglet.clock.schedule_interval(check_game_start, 1 / 30)
    pyglet.clock.schedule_interval(check_raspi_buttons, 1 / 30)
    pyglet.clock.schedule_interval(timer.update, 1/30.0)
    pyglet.app.run()




