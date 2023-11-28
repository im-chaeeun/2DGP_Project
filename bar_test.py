import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("가로 막대 바 예제")

# 색상 정의
white = (255, 255, 255)
black = (250, 0, 0)

# 막대 바 설정
bar_width, bar_height = 200, 20
bar_x, bar_y = (width - bar_width) // 2, height // 2

# 이동 속도
speed = 5

# 게임 루프
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        bar_x -= speed
    if keys[pygame.K_RIGHT]:
        bar_x += speed

    # 화면 갱신
    screen.fill(white)
    pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height))

    pygame.display.flip()

    # 초당 프레임 설정
    clock.tick(60)