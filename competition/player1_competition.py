from competition.shuttlecock_competition import Shuttlecock
from competition import server_competition

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
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, delay, clamp, draw_rectangle, get_time
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
        server_competition.player1_x += player1.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player1):
        player1.image.clip_draw(int(player1.frame) * 50, player1.action * 50, 50, 50, server_competition.player1_x, player1.y, 250, 250)


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
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, server_competition.player1_x, player1.y, 250, 250)
        pass


class Serve:
    global racket
    @staticmethod
    def enter(player1, e):
        if player1.action == 0:
            player1.action = 1
        elif player1.action == 2:
            player1.action = 1
        player1.dir = 0
        player1.frame = 0
        # print("Serve state")  # 디버깅용 출력

        # get_bb를 위한 라켓값을 enter할 때 받아서 do에서 수정하도록!
        player1.racket_x1, player1.racket_y1 = server_competition.player1_x + 45, player1.y - 20
        player1.racket_x2, player1.racket_y2 = server_competition.player1_x + 75, player1.y + 10


    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player1):
        player1.frame = (player1.frame + 1) % 5
        player1.racket_x1 += 3
        player1.racket_x2 += 3
        player1.racket_y1 += 13
        player1.racket_y2 += 13
        delay(0.05)
        # print("Serve state")  # 디버깅용 출력
        player1.stamina_percent -= 30


    @staticmethod
    def draw(player1):
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, server_competition.player1_x, player1.y, 250, 250)
        pass


    @staticmethod
    def draw(player1):
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, server_competition.player1_x, player1.y, 250, 250)
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

        # do에서 수정할 수 있도록 라켓의 위치를 받아옴
        player1.racket_x1, player1.racket_y1 = server_competition.player1_x - 100, player1.y + 65
        player1.racket_x2, player1.racket_y2 = server_competition.player1_x - 40, player1.y + 95
        pass

    @staticmethod
    def exit(player1, e):
        pass

    @staticmethod
    def do(player1):
        player1.frame = (player1.frame + 1) % 5
        player1.racket_x1 += 20
        player1.racket_x2 += 20
        player1.racket_y1 -= 3
        player1.racket_y2 -= 3
        delay(0.05)
        player1.stamina_percent -= 30

    @staticmethod
    def draw(player1):
        player1.image.clip_draw(player1.frame * 50, player1.action * 50, 50, 50, server_competition.player1_x, player1.y, 250, 250)
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

        if self.player1.stamina_percent < 30:
            self.cur_state.exit(self.player1, ('NONE', 0))
            self.cur_state = Idle
            self.cur_state.enter(self.player1, ('NONE', 0))

    def draw(self):
        self.cur_state.draw(self.player1)

class Player1:

    def __init__(self):
        self.y = 200
        self.frame, self.frame_num = 0, 0
        self.image = load_image('resource/character.png')
        self.action = 0  # 'action' 속성 추가

        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.player_turn = True

        # state 추가
        self.state = 'Idle'

        # Shuttlecock 객체 생성
        self.shuttlecock = Shuttlecock()

        # 라켓의 충돌 체크 박스 (self.x로 값 설정 못함??)
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
        # powergage
        self.powergage_percent = 0
        self.powergage_image = load_image('resource/powergage.png')

    def update(self):
        self.state_machine.update()
        # 플레이어의 x 좌표 범위 제한
        server_competition.player1_x = clamp(50, server_competition.player1_x, 400 - 50)
        # Shuttlecock 움직임 업데이트
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
        #draw_rectangle(*self.get_bb())
        # 화살표 박스 그리기
        self.draw_arrow_box()
        # stamina
        self.draw_stamina()
        # power gage
        self.draw_powergage()



    def get_bb(self):
        if self.state_machine.cur_state == Idle:
            return server_competition.player1_x + 40, int(self.y) + 10, server_competition.player1_x + 70, int(self.y) + 40
        elif self.state_machine.cur_state == Walk:
            return server_competition.player1_x + 40, int(self.y) + 10, server_competition.player1_x + 70, int(self.y) + 40
        elif self.state_machine.cur_state == Serve:
            #print('서브 겟비비')
            return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2
        elif self.state_machine.cur_state == Recieve:
            #print('리시브 겟비비')
            return self.racket_x1, self.racket_y1, self.racket_x2, self.racket_y2

    def draw_arrow_box(self):
        self.image_left.draw(40, 28)
        self.image_right.draw(130, 28)
        self.image_serve.draw(220, 28)
        self.image_recieve.draw(310, 28)
        if self.state_machine.cur_state == Walk:
            if self.dir == - 1:
                self.image_left_press.draw(40, 28)
            elif self.dir == 1:
                self.image_right_press.draw(130, 28)
        elif self.state_machine.cur_state == Serve:
          self.image_serve_press.draw(220, 28)
        elif self.state_machine.cur_state == Recieve:
           self.image_recieve_press.draw(310, 28)

    def draw_stamina(self):
        self.stamina_image.clip_draw(0, 0, 333, 10, 0, 590, self.stamina_percent, 10)

    def draw_powergage(self):
        self.powergage_image.clip_draw(0, 0, 333, 10, 0, 575, self.powergage_percent, 10)


    def handle_collision(self, group, other):
        pass