from shuttlecock import Shuttlecock

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
        player1.frame = (player1.frame + FRAMES_PER_TIME * game_framework.frame_time) % 5
        delay(0.01)
        player1.x += player1.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player1):
        player1.image.clip_draw(int(player1.frame) * 50, player1.action * 50, 50, 50, player1.x, player1.y, 250, 250)


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
        # print("Serve state")  # 디버깅용 출력
        pass

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player1):
        player1.frame = (player1.frame + 1) % 5
        delay(0.1)
        # print("Serve state")  # 디버깅용 출력
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
        delay(0.1)
        player1.frame = (player1.frame + 1) % 5

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
                   down_down: Recieve, up_down: Serve},
            Walk: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,
                   down_down: Recieve, up_down: Serve},
            Recieve: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle},
            Serve: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle},
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
        # 한 프레임이 끝났을 때 Idle 상태로 전환
        if self.cur_state == Serve or self.cur_state == Recieve:
            if self.player1.frame == 4:
                self.cur_state.exit(self.player1, ('NONE', 0))
                self.cur_state = Idle
                self.cur_state.enter(self.player1, ('NONE', 0))


    def draw(self):
        self.cur_state.draw(self.player1)

class Player1:
    def __init__(self):
        self.x, self.y = 200, 200
        self.frame = 0
        self.image = load_image('character.png')
        self.action = 0  # 'action' 속성 추가
        self.score = 0  # 점수 추가
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        # state 추가
        self.state = 'Idle'
        # Shuttlecock 객체 생성
        self.shuttlecock = Shuttlecock()
        # 라켓의 충돌 체크 박스 (self.x로 값 설정 못함??)
        self.racket_x1, self.racket_x2, self.racket_y1, self.racket_y2 = 0, 0, 0, 0


    def update(self):
        self.state_machine.update()
        # 플레이어의 x 좌표 범위 제한
        self.x = clamp(100 - 10, self.x, 400 - 50)

        # Serve 상태일 때 라켓 업데이트
        if self.state_machine.cur_state == Serve:
            # print('서브!!!!')
            self.racket_x1, self.racket_x2 = self.x + 30, self.x + 60
            self.racket_y1, self.racket_y2 = self.y - 20, self.y + 10
        elif self.state_machine.cur_state == Recieve:
            print('리시브!!!!')

        # Shuttlecock 움직임 업데이트
        self.shuttlecock.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        # Shuttlecock 이벤트 처리
        self.shuttlecock.handle_event(event)

    def draw(self):
        self.state_machine.draw()
        # Shuttlecock 그리기
        self.shuttlecock.draw()
        # 충돌 체크 박스
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        #if self.state == 'Idle':
        if self.state_machine.cur_state == Idle:
            # print('아이들')
            return self.x + 40, self.y + 10, self.x + 70, self.y + 40
        if self.state_machine.cur_state == Serve:
            print('서브 겟비비')
            self.racket_x1, self.racket_y1 = self.x + 30, self.y - 20
            self.racket_x2, self.racket_y2 = self.x + 60, self.y + 10
            return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2
        else:
            # 다른 상태이거나 상태가 정의되지 않았을 때의 기본값
            return self.x, self.y, self.x, self.y