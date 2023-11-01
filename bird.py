from pico2d import *
import game_framework
import random
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Run:
    @staticmethod
    def enter(bird, e):
        bird.dir, bird.action, bird.face_dir = 1, 2, 1


    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

        if bird.x > 1500:
            bird.dir = -1
            bird.face_dir = -1
        elif bird.x < 100:
            bird.dir = 1
            bird.face_dir = 1

        bird.action = (bird.action + 1) % 3


    @staticmethod
    def draw(bird):
        if bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) % 5 * 182, bird.action * 165, 180, 165, 0, 'h', bird.x, bird.y, 180, 180)
        else:
            bird.image.clip_composite_draw(int(bird.frame) % 5 * 182, bird.action * 165, 180, 165, 0, '', bird.x, bird.y, 180, 180)

class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run
        self.transitions = {
            Run: {},
        }

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def draw(self):
        self.cur_state.draw(self.bird)


class Bird:
    def __init__(self):
        self.x, self.y = random.randint(100, 1500), random.randint(250, 600)
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()
