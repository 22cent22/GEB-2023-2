import pygame
import random

# Pygame 모듈 초기화
pygame.init()

# 화면 설정
width, height = 800, 700 # 화면 너비와 높이 변수 설정
screen = pygame.display.set_mode((width, height)) # Pygame 화면 초기화
pygame.display.set_caption("Raindrop Physics Simulation") # 윈도우 타이틀 설정

# 색상 정의
BLACK = (7, 7, 7) # 배경색
BLUE = (129, 158, 206) # 빗방울 색
WHITE = (255, 255, 255) # 반사광 색

# 물리 변수 설정
gravity = 0.1  # 빗방울이 떨어질 때 가속될 중력 가속도 값
bounce_factor = 0.6  # 빗방울이 땅에 닿았을 때 튀어오르는 정도를 결정하는 반발력 계수
splash_particles = 5  # 빗방울이 땅에 닿아서 튀어오를 때 생성되는 작은 입자들의 수
min_splash_size = 1   # 이보다 작아지면 더 이상 입자가 그려지지 않는 입자의 최소 크기
max_generations = 3   # 입자가 분할되는 세대의 최대 횟수, 이를 넘으면 더 이상 분할되지 않음
burst_speed_threshold = 0.5  # 입자가 바닥에 닿았을 때 이 속도보다 낮으면 튀지 않고 멈추게 하는 임계값

# 속도와 수 조절 변수
raindrop_speed = 0  # 빗방울의 초기 속도, 0으로 시작
raindrop_count = 1  # 한 번에 생성되는 빗방울의 수, 1로 시작

# 빗방울 클래스 정의
class Raindrop:
    # 빗방울 인스턴스 생성자
    def __init__(self, x, y):
        self.x = x  # 빗방울의 x 좌표
        self.y = y  # 빗방울의 y 좌표
        self.speed = raindrop_speed  # 빗방울의 현재 낙하 속도
        self.size = random.randint(5, 7)  # 빗방울의 크기를 5에서 7 사이의 난수로 설정
        self.splashed = False  # 빗방울이 땅에 닿았는지 여부를 나타내는 플래그

    # 입자 이동 처리
    def move(self):
        self.speed += gravity  # 입자의 속도에 중력값을 더해서 낙하 속도 증가
        self.y += self.speed   # 입자의 y 좌표를 업데이트하여 실제로 낙하 효과 적용

        # 바닥 충돌 처리
        if not self.splashed and self.y >= height - self.size:
            self.splashed = True  # 만약 입자가 바닥에 도달했다면, 'splashed' 상태를 True로 변경
            self.fragment(0) # 그리고 입자를 분할하는 fragment 함수를 호출

    # 입자 그리기
    def draw(self):
        if not self.splashed: # 만약 입자가 아직 바닥에 닿지 않았다면
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size) # 화면에 파란색 원으로 입자를 그림
           
           # 반사광 그리기
            if self.size >= 4:  # 만약 입자의 크기가 4 이상이라면 반사광을 그림
                highlight_offset = self.size // 3  # 반사광의 위치를 결정하기 위해 입자 크기의 1/3 값을 계산
                highlight_x = int(self.x) + highlight_offset  # 반사광의 x 좌표는 입자의 x 좌표에 offset을 더함
                highlight_y = int(self.y) - highlight_offset  # 반사광의 y 좌표는 입자의 y 좌표에서 offset을 뺌
                highlight_size = max(1, self.size // 3)  # 반사광의 크기는 입자 크기의 1/3으로 설정, 단 최소 크기는 1
                pygame.draw.circle(screen, WHITE, (highlight_x, highlight_y), highlight_size)  # 화면에 흰색 원으로 반사광을 그림

    # 입자 분할 처리
    def fragment(self, generation):
        for _ in range(splash_particles):
            # 현재 빗방울 위치에서 새로운 Splash 입자 생성해서 splashes 리스트에 추가
            splashes.append(Splash(self.x, height - self.size, self.size // 2, generation + 1))

# 튀기는 입자 클래스 정의
class Splash:
    def __init__(self, x, y, size, generation):
        self.x = x # 입자의 x 좌표
        self.y = y # 입자의 y 좌표
        self.size = max(size, min_splash_size)  # 입자의 크기, 최소 크기보다 작지 않게 설정
        self.speed = random.uniform(-2, 2), random.uniform(-5, 0)  # 초기 속도 랜덤 결정
        self.generation = generation  # 입자의 세대, 분할될 때마다 증가
        self.stopped = False  # 입자가 정지했는지의 여부

    # 입자 이동 처리
    def move(self):
        if not self.stopped:
            self.x += self.speed[0] # x축 속도에 따라 x 좌표 업데이트
            self.y += self.speed[1] # y축 속도에 따라 y 좌표 업데이트
            self.speed = (self.speed[0], self.speed[1] + gravity) # y축 속도에 중력 효과 적용
            
            # 바닥 충돌 처리
            if self.y >= height - self.size: # 입자가 바닥에 도달했는지 검사
                if abs(self.speed[1]) < burst_speed_threshold or self.generation >= max_generations:
                    self.stopped = True # 속도 임계값 또는 최대 세대에 도달하면 정지
                else:
                    # 반발력을 적용하여 y축 속도 방향 반전 및 감속
                    self.speed = (self.speed[0] * bounce_factor, -self.speed[1] * bounce_factor)
                    self.fragment() # 더 작은 입자로 분할

    # 입자 그리기
    def draw(self):
        if not self.stopped:  # 정지하지 않은 입자만 화면에 그림
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)  # 입자를 파란색 원으로 그림
            # 반사광 그리기
            if self.size >= 4:  # 입자 크기가 충분히 클 때만 반사광을 그림
                highlight_offset = self.size // 3  # 반사광 위치 계산
                highlight_x = int(self.x) + highlight_offset  # 반사광 x 좌표
                highlight_y = int(self.y) - highlight_offset  # 반사광 y 좌표
                highlight_size = max(1, self.size // 3)  # 반사광 크기 계산, 최소 1
                pygame.draw.circle(screen, WHITE, (highlight_x, highlight_y), highlight_size)  # 반사광을 흰색 원으로 그림

    # 입자 분할 처리
    def fragment(self):
        if self.generation < max_generations:  # 최대 세대에 도달하지 않았을 때만 분할
            for _ in range(2):  # 두 개의 새로운 입자 생성
                new_size = max(self.size // 3, min_splash_size)  # 새 입자 크기 계산
                splashes.append(Splash(self.x, self.y, new_size, self.generation + 1))  # 새 입자 splashes 리스트에 추가
            splashes.remove(self)  # 현재 입자는 리스트에서 제거

# 빗방울 생성 함수
def create_raindrops(x, y, count):
    spacing = 20  # 빗방울 간 간격 설정
    start_x = x - (spacing * (count - 1)) / 2  # 첫 빗방울의 x 좌표 계산

    for i in range(count):  # 지정된 수만큼 빗방울 생성
        raindrop_x = start_x + i * spacing  # 각 빗방울의 x 좌표 계산
        raindrops.append(Raindrop(raindrop_x, y))  # 빗방울 리스트에 추가

# 빗방울과 튀기는 입자 리스트 초기화
raindrops = []  # 빗방울 리스트
splashes = []  # 튀기는 입자 리스트

# 텍스트 표시 함수
def display_text(text, x, y, color=WHITE, font_size=20):
    font = pygame.font.SysFont(None, font_size)  # 폰트 설정
    text = font.render(text, True, color)  # 텍스트 렌더링
    screen.blit(text, (x, y))  # 화면에 텍스트 표시

# 게임 실행 상태 변수
paused = False  # 일시정지 상태
running = True  # 게임 실행 중

# 게임 메인 루프
while running:
    for event in pygame.event.get():  # 이벤트 처리
        if event.type == pygame.QUIT:  # 종료 이벤트가 발생하면
            running = False  # 게임 종료
        # 키보드 이벤트 처리
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # P 키를 누르면 일시정지 토글
            elif event.key == pygame.K_q:
                running = False  # Q 키를 누르면 게임 종료
            elif event.key == pygame.K_1:
                raindrop_speed += 1  # 속도 증가
            elif event.key == pygame.K_2:
                raindrop_speed = max(0, raindrop_speed - 1)  # 속도 감소
            if event.key == pygame.K_3:
                raindrop_count += 1  # 빗방울 수 증가
            elif event.key == pygame.K_4:
                raindrop_count = max(1, raindrop_count - 1)  # 빗방울 수 감소
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트 처리
            x, y = event.pos  # 클릭 위치
            create_raindrops(x, y, raindrop_count)  # 클릭 위치에 빗방울 생성

    if not paused:  # 게임이 일시정지 상태가 아니라면
        screen.fill(BLACK)  # 화면을 검은색으로 채움
        
        # 화면에 텍스트 표시
        display_text("Raindrop Physics Simulation", 10, 20, font_size=24)
        display_text("raindrops fall from the mouse click position", 10, 45, font_size=18)
        display_text("[P] PAUSE", 10, 70, font_size=18)
        display_text("[Q] QUIT", 10, 95, font_size=18)
        display_text("[1] Increase Speed  [2] Decrease Speed", width//2 - 100, height//2 - 330, font_size=18)
        display_text("[3] Add Raindrop  [4] Subtract Raindrop", width//2 - 100, height//2 - 310, font_size=18)

        # 모든 빗방울 및 입자 이동 및 그리기 처리
        for raindrop in raindrops:
            raindrop.move()  # 빗방울 이동
            raindrop.draw()  # 빗방울 그리기

        for splash in splashes[:]:  # 리스트를 복사하여 순회하면서
            splash.move()  # 입자 이동
            splash.draw()  # 입자 그리기

        pygame.display.flip()  # 화면 전체를 업데이트
        pygame.time.delay(10)  # 10밀리초 동안 대기하여 프레임 속도 조절

# Pygame 종료 처리
pygame.quit()  # Pygame 종료
