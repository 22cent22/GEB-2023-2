import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Raindrop Physics Simulation")

# 색상 설정
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# 물리적 속성
gravity = 0.1
bounce_factor = 0.6  # 바닥에 닿은 입자들의 반발력
splash_particles = 5  # 초기 분리될 입자 수
min_splash_size = 1   # 입자의 최소 크기
max_generations = 3   # 세분화 최대 횟수
burst_speed_threshold = 0.5  # 바닥에 닿았을 때 튀어오르지 않고 정지하는 속도 임계값

# 속도 및 빗방울 수 조절을 위한 변수
raindrop_speed = 0
raindrop_count = 1

# 빗방울 클래스 정의
class Raindrop:
    # 생성자에서 x, y 위치를 받도록 수정
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = raindrop_speed  # 여기서 전역 변수의 현재 값을 사용(초기 속도 지정할 수 있는 곳)
        self.size = random.randint(5, 7)
        self.splashed = False

    def move(self):
        self.speed += gravity  # 중력에 의해 속도 증가
        self.y += self.speed   # 속도에 따른 y 위치 업데이트

        # 여기서 전역변수 raindrop_speed를 참조하여 속도 조정
        if self.speed < raindrop_speed:
            self.speed = raindrop_speed
        
        if not self.splashed:
            # 땅에 닿으면 분할 및 튀기는 효과
            if self.y >= height - self.size:
                self.splashed = True
                self.fragment(0)  # 초기 세대는 0

    def draw(self):
        if not self.splashed:
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)

    def fragment(self, generation):
        for _ in range(splash_particles):
            splashes.append(Splash(self.x, height - self.size, self.size // 2, generation + 1))

# 튀는 입자 클래스
class Splash:
    def __init__(self, x, y, size, generation):
        self.x = x
        self.y = y
        self.size = max(size, min_splash_size)
        self.speed = random.uniform(-2, 2), random.uniform(-5, 0)
        self.generation = generation
        self.stopped = False  # 입자가 정지했는지 여부

    def move(self):
        if self.stopped:  # 이미 정지한 입자는 이동하지 않음
            return
        
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.speed = self.speed[0], self.speed[1] + gravity
        
        # 바닥에 닿았을 때의 처리
        if self.y >= height - self.size:
            self.y = height - self.size
            if abs(self.speed[1]) < burst_speed_threshold or self.generation >= max_generations:
                self.stopped = True  # 속도가 기준 이하이면 정지
                self.speed = (0, 0)
            else:
                # 속도가 기준 이상이면 튀어오르고 세분화
                self.speed = (self.speed[0] * bounce_factor, -self.speed[1] * bounce_factor)
                self.fragment()

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)

    def fragment(self):
        # 현재 입자를 더 작은 입자들로 분할
        for _ in range(2):  # 두 개의 더 작은 입자 생성
            new_size = max(self.size // 3, min_splash_size)  # 새 입자 크기를 1/3로 설정
            splashes.append(Splash(self.x, self.y, new_size, self.generation + 1))
        splashes.remove(self)  # 현재 입자는 제거

def create_raindrops(x, y, count):
    spacing = 20  # 물방울 사이 간격을 20으로 설정
    start_x = x - (spacing * (count - 1)) / 2  # 첫 번째 물방울의 x 위치 계산

    for i in range(count):
        raindrop_x = start_x + i * spacing  # 각 물방울의 x 위치
        raindrops.append(Raindrop(raindrop_x, y))

# 빗방울 및 튀는 입자들을 저장할 리스트
raindrops = []  # 빈 리스트로 초기화
splashes = []

# 글자를 화면에 표시하는 함수
def display_text(text, x, y, color=WHITE, font_size=20):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

# 게임 상태 관리를 위한 변수
paused = False
running = True

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_1:
                raindrop_speed += 1  # 빗방울 속도 증가
            elif event.key == pygame.K_2:
                raindrop_speed = max(0, raindrop_speed - 1)  # 빗방울 속도 감소
            if event.key == pygame.K_3:
                raindrop_count = min(15, raindrop_count + 1)  # 물방울 수 증가
            elif event.key == pygame.K_4:
                raindrop_count = max(1, raindrop_count - 1)  # 물방울 수 감소
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            x, y = event.pos # 마우스 클릭 위치에 빗방울 생성
            create_raindrops(x, y, raindrop_count)  # 여러 물방울을 생성하는 함수 호출

    if not paused:
        screen.fill(BLACK)

        # 안내문 표시 (폰트 크기를 20으로 설정하고 좌측 상단에 위치)
        display_text("Raindrop Physics Simulation", 10, 20, font_size=24)
        display_text("raindrops fall from the mouse click position", 10, 45, font_size=18)
        display_text("[P] PAUSE", 10, 70, font_size=18)
        display_text("[Q] QUIT", 10, 95, font_size=18)
        display_text("[1] Increase Speed  [2] Decrease Speed", width//2 - 100, height//2 - 330, font_size=18)
        display_text("[3] Add Raindrop  [4] Subtract Raindrop", width//2 - 100, height//2 - 310, font_size=18)

        for raindrop in raindrops:
            raindrop.move()
            raindrop.draw()

        for splash in splashes[:]:
            splash.move()
            splash.draw()

        pygame.display.flip()
        pygame.time.delay(10)

pygame.quit()
