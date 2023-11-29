import arrow_practice_mode
import play_mode_practice
from shuttlecock_practice import Shuttlecock_Practice
from arrow_practice_mode import Arrow
# from stamina_bar import Stamina

PIXEL_PER_METER = (10.0/0.3)    # 10pixel 30cm
RUN_SPEED_KMPH = 25.0   # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0  # 분당 몇 m?
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0    # 초당 몇 m?
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

import game_framework
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, delay, clamp, draw_rectangle
from sdl2 import SDLK_d, SDLK_a, SDLK_s, SDLK_w

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

class Walk:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):  # 우측으로 Walk
            player.dir, player.action = 1, 2
        elif left_down(e) or right_up(e):  # 좌측으로 Walk
            player.dir, player.action = -1, 2

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 5
        delay(0.01)
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 50, player.action * 50, 50, 50, player.x, player.y, 250, 250)


class Idle:
    @staticmethod
    def enter(player, e):
        if player.action == 0:
            player.action = 2
        elif player.action == 1:
            player.action = 2
        player.dir = 1
        player.frame = 0
        pass

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 50, player.action * 50, 50, 50, player.x, player.y, 250, 250)
        pass


class Serve:
    global racket
    @staticmethod
    def enter(player, e):
        if player.action == 0:
            player.action = 1
        elif player.action == 2:
            player.action = 1
        player.dir = 0
        player.frame = 0
        # print("Serve state")  # 디버깅용 출력

        # get_bb를 위한 라켓값을 enter할 때 받아서 do에서 수정하도록!
        player.racket_x1, player.racket_y1 = player.x + 45, player.y - 20
        player.racket_x2, player.racket_y2 = player.x + 75, player.y + 10


    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 5
        player.racket_x1 += 3
        player.racket_x2 += 3
        player.racket_y1 += 13
        player.racket_y2 += 13
        delay(0.1)
        # print("Serve state")  # 디버깅용 출력


    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 50, player.action * 50, 50, 50, player.x, player.y, 250, 250)


class Recieve:
    @staticmethod
    def enter(player, e):
        if player.action == 1:
            player.action = 0
        elif player.action == 2:
            player.action = 0
        player.dir = 0
        player.frame = 0

        # do에서 수정할 수 있도록 라켓의 위치를 받아옴
        player.racket_x1, player.racket_y1 = player.x - 120, player.y + 65
        player.racket_x2, player.racket_y2 = player.x - 90, player.y + 95
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 5
        player.racket_x1 += 20
        player.racket_x2 += 20
        player.racket_y1 -= 3
        player.racket_y2 -= 3
        delay(0.1)

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 50, player.action * 50, 50, 50, player.x, player.y, 250, 250)
        pass


class StateMachine:
    def __init__(self, player):
        self.cur_state = Idle
        self.player = player
        self.transitions = {
            Idle: {right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk,
                   down_down: Recieve, up_down: Serve},
            Walk: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,
                   down_down: Recieve, up_down: Serve},
            Recieve: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle},
            Serve: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)
        # 한 프레임이 끝났을 때 Idle 상태로 전환
        if self.cur_state == Serve or self.cur_state == Recieve:
            if self.player.frame == 4:
                self.cur_state.exit(self.player, ('NONE', 0))
                self.cur_state = Idle
                self.cur_state.enter(self.player, ('NONE', 0))


    def draw(self):
        self.cur_state.draw(self.player)

class Player:
    def __init__(self):
        self.x, self.y = 200, 200
        self.frame = 0
        self.image = load_image('character.png')
        self.action = 0  # 'action' 속성 추가
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        # state 추가
        self.state = 'Idle'
        # Shuttlecock 객체 생성
        self.shuttlecock_practice = Shuttlecock_Practice()
        # 라켓의 충돌 체크 박스
        self.racket_x1, self.racket_x2, self.racket_y1, self.racket_y2 = 0, 0, 0, 0
        # 화살표 박스 그리기 변수
        # self.select_press = 0


    def update(self):
        self.state_machine.update()
        # 플레이어의 x 좌표 범위 제한
        self.x = clamp(100 - 10, self.x, 400 - 50)

        # Shuttlecock 움직임 업데이트
        self.shuttlecock_practice.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        # Shuttlecock 이벤트 처리
        self.shuttlecock_practice.handle_event(event)


    def draw(self):
        self.state_machine.draw()
        # Shuttlecock 그리기
        self.shuttlecock_practice.draw()
        # 충돌 체크 박스
        draw_rectangle(*self.get_bb())
        # Stamina 바 그리기
        #self.stamina.draw()


    def get_bb(self):
        if self.state_machine.cur_state == Idle:
            return self.x + 40, self.y + 10, self.x + 70, self.y + 40
        elif self.state_machine.cur_state == Walk:
            return self.x + 40, self.y + 10, self.x + 70, self.y + 40
        elif self.state_machine.cur_state == Serve:
            print('서브 겟비비')
            return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2
        elif self.state_machine.cur_state == Recieve:
            print('리시브 겟비비')
            return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2

    # def check_press_arrow(self):
    #     if self.state_machine.cur_state == Idle:
    #         self.select_press = 0
    #     elif self.state_machine.cur_state == Walk:
    #         self.select_press = 1
    #     return self.select_press
    # elif self.state_machine.cur_state == Serve:
    #     print('서브 겟비비')
    #     return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2
    # elif self.state_machine.cur_state == Recieve:
    #     print('리시브 겟비비')
    #     return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2

