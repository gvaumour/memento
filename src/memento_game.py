#!/usr/bin/env python

import os
import pyglet
import random

dir_path = os.path.dirname(os.path.realpath(__file__))

# Pictos printed on buttons 
PATH_BUTTONS_PICTO = os.path.realpath(os.path.join(dir_path, "../pictos/picto_button"))

# Picto not printed on buttons, they are called noise pictos
PATH_NOISE_PICTO = os.path.realpath(os.path.join(dir_path, "../pictos/picto_noise"))

def isCorrectPicto(picto_path):
    # To be improved with other criteria 
    if os.path.isfile(picto_path):
        return True

path_buttons_picto = [os.path.join(PATH_BUTTONS_PICTO, f) for f in os.listdir(PATH_BUTTONS_PICTO) if isCorrectPicto(os.path.join(PATH_BUTTONS_PICTO, f))]
path_noise_picto = [os.path.join(PATH_NOISE_PICTO, f) for f in os.listdir(PATH_NOISE_PICTO) if isCorrectPicto(os.path.join(PATH_NOISE_PICTO, f))]


################################# 
# GAME PARAMETERS 

ROUND_TIME = 10       # Number of seconds per round 
NB_NOISE_PICTO = 7    # Number of picto displayed on top of the correct one
POINTS_PER_ROUND = 10 # Number of points per good answer
################################# 


window = pyglet.window.Window(fullscreen=True)

class Board:
    def __init__(self):
        self.started = True
        self.do_next_round()

    def do_next_round(self):
        self.displayed_noise_picto = [random.choice(noise_picto) for i in range(NB_NOISE_PICTO)]
        self.displayed_button_picto = random.choice(buttons_picto)


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
            self.label.text = '%01d' % (self.time)




@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        timer.reset()
        timer.running = True
    elif symbol == pyglet.window.key.ESCAPE:
        window.close()


@window.event
def on_draw():
    window.clear()
    timer.label.draw()
    score.label.draw()

    background.blit(0,0)
    #print(truc)
    # ball = pyglet.sprite.Sprite(board.displayed_button_picto, x=window.width//2, y=window.height//2)
    #ball.draw()
    board.displayed_button_picto.blit(100, 100)

    #ref = 100
    #for img in board.displayed_noise_picto:
    #    img.x, img.y = ref , ref
    #    img.draw()
    #    ref = ref + 100


buttons_picto = [pyglet.image.load(f) for f in path_buttons_picto]
noise_picto = [pyglet.image.load(f) for f in path_noise_picto]


def resize_image(image):
    height, width = 32 , 32
    image.scale =  height / image.height
    print("Greg = " + str(image.scale))

def resize_images():
    for image in buttons_picto:
        resize_image(image)
    for image in noise_picto:
        resize_image(image)

#resize_images()

background = pyglet.image.load(PATH_BUTTONS_PICTO + str("/background.png"), width=window.width, height=window.height)

timer = Timer()
score = Score()
board = Board()
pyglet.clock.schedule_interval(timer.update, 1/30.0)
pyglet.app.run()

