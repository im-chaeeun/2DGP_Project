import pygame
import sys

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion")

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 초기 위치 및 속도
x, y = 100, HEIGHT - 100
initial_speed_x = 5
initial_speed_y = -10

# 중력 가속도
gravity = 0.5

# 게임 루프
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 수평 및 수직 속도 업데이트
    x += initial_speed_x
    y += initial_speed_y
    initial_speed_y += gravity

    # 그리기
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (int(x), int(y)), 10)

    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 설정
    clock.tick(60)