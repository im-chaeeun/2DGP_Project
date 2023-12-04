import game_framework
from competition.shuttlecock_competition import Shuttlecock

PIXEL_PER_METER = (10.0/0.3)    # 10pixel 30cm
RUN_SPEED_KMPH = 25.0   # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0  # 분당 몇 m?
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0    # 초당 몇 m?
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

# 리시브
RECEIVE_SPEED_KMPH = 15.0 # Km / Hour
RECEIVE_SPEED_MPM = (RECEIVE_SPEED_KMPH * 1000.0 / 60.0)
RECEIVE_SPEED_MPS = (RECEIVE_SPEED_MPM / 60.0)
RECEIVE_SPEED_PPS = (RECEIVE_SPEED_MPS * PIXEL_PER_METER)

# 서브
SERVE_SPEED_KMPH = 10.0 # Km / Hour
SERVE_SPEED_MPM = (SERVE_SPEED_KMPH * 1000.0 / 60.0)
SERVE_SPEED_MPS = (SERVE_SPEED_MPM / 60.0)
SERVE_SPEED_PPS = (SERVE_SPEED_MPS * PIXEL_PER_METER)

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, delay, clamp, get_time, draw_rectangle
from sdl2 import SDLK_RIGHT, SDLK_LEFT, SDLK_DOWN, SDLK_UP


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


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


class Walk:
    @staticmethod
    def enter(player2, e):
        if right_down(e) or left_up(e):  # 우측으로 Walk
            player2.dir, player2.action = 1, 2
        elif left_down(e) or right_up(e):  # 좌측으로 Walk
            player2.dir, player2.action = -1, 2

    @staticmethod
    def exit(player2, e):
        pass

    @staticmethod
    def do(player2):
        player2.frame = (player2.frame + FRAMES_PER_TIME * game_framework.frame_time) % 5
        delay(0.01)
        player2.x += player2.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player2):
        player2.image.clip_composite_draw(int(player2.frame) * 50, player2.action * 50, 50, 50, 0, 'h', player2.x, player2.y, 250, 250)

class Idle:
    @staticmethod
    def enter(player2, e):
        if player2.action == 0:
            player2.action = 2
        elif player2.action == 1:
            player2.action = 2
        player2.dir = 1
        player2.frame = 0
        pass

    @staticmethod
    def exit(player2, e):
        pass

    @staticmethod
    def do(player2):
        pass

    @staticmethod
    def draw(player2):
        player2.image.clip_composite_draw(player2.frame * 50, player2.action * 50, 50, 50, 0, 'h', player2.x, player2.y, 250, 250)
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

        # get_bb를 위한 라켓값을 enter할 때 받아서 do에서 수정하도록!
        player1.racket_x1, player1.racket_y1 = player1.x - 75, player1.y - 20
        player1.racket_x2, player1.racket_y2 = player1.x - 45, player1.y + 10


    @staticmethod
    def exit(player2, e):
        pass

    @staticmethod
    def do(player2):
        player2.frame = (player2.frame + 1) % 5
        player2.racket_x1 -= 3
        player2.racket_x2 -= 3
        player2.racket_y1 += 13
        player2.racket_y2 += 13
        delay(0.05)
        # print("Serve state")  # 디버깅용 출력
        player2.stamina_percent -= 30

    @staticmethod
    def draw(player2):
        player2.image.clip_composite_draw(player2.frame * 50, player2.action * 50, 50, 50, 0, 'h', player2.x, player2.y, 250, 250)



class Recieve:
    @staticmethod
    def enter(player2, e):
        if player2.action == 1:
            player2.action = 0
        elif player2.action == 2:
            player2.action = 0
        player2.dir = 0
        player2.frame = 0

        # do에서 수정할 수 있도록 라켓의 위치를 받아옴
        player2.racket_x1, player2.racket_y1 = player2.x + 70, player2.y + 65
        player2.racket_x2, player2.racket_y2 = player2.x + 100, player2.y + 95

    @staticmethod
    def exit(player2, e):
        pass

    @staticmethod
    def do(player2):
        player2.frame = (player2.frame + 1) % 5
        player2.racket_x1 -= 20
        player2.racket_x2 -= 20
        player2.racket_y1 -= 3
        player2.racket_y2 -= 3
        delay(0.05)
        player2.stamina_percent -= 30

    @staticmethod
    def draw(player2):
        player2.image.clip_composite_draw(player2.frame * 50, player2.action * 50, 50, 50, 0, 'h',player2.x, player2.y, 250, 250)
        pass


class StateMachine:
    def __init__(self, player2):
        self.cur_state = Idle
        self.player2 = player2
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
                self.cur_state.exit(self.player2, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player2, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.player2, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player2)

        # 한 프레임이 끝났을 때 Idle 상태로 전환
        if self.cur_state == Serve or self.cur_state == Recieve:
            if self.player2.frame == 4:
                self.cur_state.exit(self.player2, ('NONE', 0))
                self.cur_state = Idle
                self.cur_state.enter(self.player2, ('NONE', 0))

        if self.player2.stamina_percent < 30:
            self.cur_state.exit(self.player2, ('NONE', 0))
            self.cur_state = Idle
            self.cur_state.enter(self.player2, ('NONE', 0))


    def draw(self):
        self.cur_state.draw(self.player2)


class Player2:

    def __init__(self):
        self.x, self.y = 600, 200
        self.frame = 0
        self.image = load_image('resource/character.png')
        self.action = 0  # 'action' 속성 추가
        self.score, self.setscore = 0, 0  # 점수 추가
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.player_turn = False
        # Shuttlecock 객체 생성
        self.shuttlecock = Shuttlecock()
        # 라켓의 충돌 체크 박스
        self.racket_x1, self.racket_x2, self.racket_y1, self.racket_y2 = 0, 0, 0, 0
        # 화살표 그리기 - 따로 클래스 만들면 안 돼서 player에서 그림
        self.image_left = load_image('resource/arrow_left.png')
        self.image_left_press = load_image('resource/arrow_left_press.png')
        self.image_right = load_image('resource/arrow_right.png')
        self.image_right_press = load_image('resource/arrow_right_press.png')
        self.image_serve = load_image('resource/arrow_serve.png')
        self.image_serve_press = load_image('resource/arrow_serve_press.png')
        self.image_recieve = load_image('resource/arrow_recieve.png')
        self.image_recieve_press = load_image('resource/arrow_recieve_press.png')

        # 스테미나
        self.stamina_percent, self.stamina_start_time = 640, 0
        self.stamina_image = load_image('resource/stamina.png')

    def update(self):
        self.state_machine.update()

        # x 좌표 범위 제한
        self.x = clamp(400 + 50, self.x, 750)
        # Shuttlecock 업데이트
        self.shuttlecock.update()
        # 스테미나 채우기
        self.stamina_percent = clamp(0, self.stamina_percent, 640)
        #print(self.stamina_percent)
        if get_time() - self.stamina_start_time > 0.2:
            self.stamina_percent += 10
            self.stamina_start_time = get_time()


    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        # Shuttlecock 이벤트 처리
        self.shuttlecock.handle_event(event)

    def draw(self):
        self.state_machine.draw()
        # 충돌 체크 박스
        draw_rectangle(*self.get_bb())
        # 화살표 박스 그리기
        self.draw_arrow_box()
        # stamina
        self.draw_stamina()

    def get_bb(self):
        if self.state_machine.cur_state == Idle:
            return self.x - 40, self.y + 10, self.x - 70, self.y + 40
        elif self.state_machine.cur_state == Walk:
            return self.x - 40, self.y + 10, self.x - 70, self.y + 40
        elif self.state_machine.cur_state == Serve:
            #print('서브 겟비비')
            return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2
        elif self.state_machine.cur_state == Recieve:
            #print('리시브 겟비비')
            return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2

    def draw_arrow_box(self):
        self.image_left.draw(670, 28)
        self.image_right.draw(760, 28)
        self.image_serve.draw(580, 28)
        self.image_recieve.draw(490, 28)
        if self.state_machine.cur_state == Walk:
            if self.dir == - 1:
                self.image_left_press.draw(670, 28)
            elif self.dir == 1:
                self.image_right_press.draw(760, 28)
        elif self.state_machine.cur_state == Serve:
          self.image_serve_press.draw(580, 28)
        elif self.state_machine.cur_state == Recieve:
           self.image_recieve_press.draw(490, 28)

    def draw_stamina(self):
        self.stamina_image.clip_draw(0, 0, 333, 10, 797, 590, self.stamina_percent, 10)

    def handle_collision(self, group, other):
        pass
