from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT
from sdl2 import SDLK_DOWN, SDLK_UP


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


class Walk:
    @staticmethod
    def enter(player1, e):
        if right_down(e) or left_up(e):  # 우측으로 Walk
            player1.dir, player1.action = 1, 2
        elif left_down(e) or right_up(e):  # 좌측으로 Walk
            player1.dir, player1.action = -1, 2

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player1):
        player1.frame = (player1.frame + 1) % 5
        player1.x += player1.dir * 10
        pass

    @staticmethod
    def draw(player1):
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, player1.x, player1.y, 250, 250)


class Idle:
    @staticmethod
    def enter(player1, e):
        if player1.action == 0:
            player1.action = 2
        elif player1.action == 1:
            player1.action = 2
        player1.dir = 1
        player1.frame = 0
        pass

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player1):
        pass

    @staticmethod
    def draw(player1):
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, player1.x, player1.y, 250, 250)
        pass


class Serve:
    @staticmethod
    def enter(player1, e):
        if player1.action == 0:
            player1.action = 1
        elif player1.action == 2:
            player1.action = 1
        player1.dir = 0
        player1.frame = 0
        pass

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player1):
        player1.frame = (player1.frame + 1) % 5

        if player1.frame == 4:  # 프레임이 한 바퀴 돌면
            player1.state_machine.handle_event(('INPUT', SDL_KEYUP, SDLK_UP))  # 강제로 다음 상태로 전환

        pass

    @staticmethod
    def draw(player1):
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, player1.x, player1.y, 250, 250)
        pass


class Recieve:
    @staticmethod
    def enter(player1, e):
        if player1.action == 1:
            player1.action = 0
        elif player1.action == 2:
            player1.action = 0
        player1.dir = 0
        player1.frame = 0
        pass

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player1):
        player1.frame = (player1.frame + 1) % 5

        # if player1.frame == 0:  # 프레임이 한 바퀴 돌면
        #     player1.state_machine.handle_event(('INPUT', SDL_KEYUP, SDLK_DOWN))  # 강제로 다음 상태로 전환

    @staticmethod
    def draw(player1):
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, player1.x, player1.y, 250, 250)
        pass


class StateMachine:
    def __init__(self, player1):
        self.cur_state = Idle
        self.player1 = player1
        self.transitions = {
            Idle: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk,
                   down_down: Recieve, up_down: Serve, down_up: Idle, up_up: Idle},
            Walk: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,  down_down: Recieve,
                   up_down: Serve, down_up: Walk, up_up: Walk},
            Recieve: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,  down_down: Recieve,
                   up_down: Serve, down_up: Walk, up_up: Walk},
            Serve: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,  down_down: Recieve,
                   up_down: Serve, down_up: Walk, up_up: Walk},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player1, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player1, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.player1, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player1)

    def draw(self):
        self.cur_state.draw(self.player1)


class Player1:
    def __init__(self):
        self.x, self.y = 200, 200
        self.frame = 0
        self.image = load_image('character.png')
        self.action = 0  # 'action' 속성 추가
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
