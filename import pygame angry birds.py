import pygame
import math
import random

# Класс для подвижных мишеней (свинок) 
class Pig:
    def __init__(self, x, y, speed, min_x, max_x):
        # Используем глобальный pig_image, загруженный один раз
        self.image = pig_image 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        # Направление: 1 = вправо, -1 = влево. Выбираем случайное начальное направление.
        self.direction = random.choice([1, -1]) 
        self.min_x = min_x
        self.max_x = max_x

    def move(self):
        self.rect.x += self.speed * self.direction
        
        # Если свинка достигла левой или правой границы, меняем направление
        if self.rect.left <= self.min_x:
            self.direction = 1 # Двигаться вправо
        elif self.rect.right >= self.max_x:
            self.direction = -1 # Двигаться влево

    def draw(self, surface):
        surface.blit(self.image, self.rect)


#  Инициализация Pygame и настройка окна 
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Birds-Style Game")

# Загрузка ресурсов 
background = pygame.transform.scale(pygame.image.load("backgroung birds.jpg"), (WIDTH, HEIGHT))
bird_image = pygame.transform.scale(pygame.image.load("bird.jpg"), (40, 40))
pig_image = pygame.transform.scale(pygame.image.load("pig.png"), (50, 50))
    
# Звуки
pygame.mixer.music.load("sound-effect-birds-birds-sound-fx.wav")
pygame.mixer.music.play(-1)
launch_sound = pygame.mixer.Sound("music hit.wav")
hit_sound = pygame.mixer.Sound("music hit.wav")

#  Основные игровые переменные 
start_x, start_y = 150, 450
x, y = start_x, start_y
radius = 20
vx, vy = 0, 0

gravity = 0.4
power_multiplier = 0.15

is_aiming = False
is_flying = False
game_over = False
win = False

# Мишени (свинки) 
# Теперь это список объектов класса Pig
def create_targets():
    return [
        Pig(x=550, y=500, speed=1, min_x=550, max_x=700),
        Pig(x=650, y=500, speed=2, min_x=550, max_x=700),
        Pig(x=600, y=440, speed=1.5, min_x=580, max_x=680)
    ]
targets = create_targets()

score = 0
shots_left = 4

font_large = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 36)

# Главный игровой цикл 
running = True
clock = pygame.time.Clock()

while running:
    # Обработка событий 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            x, y = start_x, start_y
            vx, vy = 0, 0
            is_aiming, is_flying, game_over, win = False, False, False, False
            score, shots_left = 0, 4
            targets = create_targets() # Пересоздаем мишени

        if not is_flying and not game_over and not win:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if math.hypot(mouse_x - x, mouse_y - y) < radius * 2:
                    is_aiming = True
            if event.type == pygame.MOUSEMOTION and is_aiming:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and is_aiming:
                is_aiming, is_flying = False, True
                vx, vy = (start_x - x) * power_multiplier, (start_y - y) * power_multiplier
                shots_left -= 1
                launch_sound.play()

    # Игровая физика 
    if is_flying:
        vy += gravity
        x += vx
        y += vy
        if x > WIDTH + radius or y > HEIGHT + radius or x < -radius:
            x, y = start_x, start_y
            is_flying, vx, vy = False, 0, 0
            
    # Двигаем каждую свинку
    for target in targets:
        target.move()

    # Проверка столкновения с мишенями
    ball_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    for target in targets[:]:
        # Проверяем столкновение с прямоугольником свинки
        if ball_rect.colliderect(target.rect):
            hit_sound.play()
            targets.remove(target)
            score += 100
    
    # Проверка условий победы и поражения
    if not targets and not win:
        win = True
    if shots_left == 0 and not is_flying and not win:
        game_over = True

    # Отрисовка
    screen.blit(background, (0, 0))

    if is_aiming:
        pygame.draw.line(screen, (48, 25, 52), (start_x - 10, start_y - 5), (x, y), 5)
        pygame.draw.line(screen, (48, 25, 52), (start_x + 10, start_y - 5), (x, y), 5)

    screen.blit(bird_image, (int(x - radius), int(y - radius)))

    # Рисуем мишени, вызывая их собственный метод draw
    for target in targets:
        target.draw(screen)

    # Отображение текста
    score_text = font_small.render(f"Счёт: {score}", True, (255, 255, 255))
    shots_text = font_small.render(f"Выстрелов осталось: {shots_left}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(shots_text, (10, 40))

    # Сообщения о победе/поражении
    if win:
        win_text = font_large.render("ПОБЕДА!", True, (0, 255, 0))
        restart_text = font_small.render("Нажмите R для перезапуска", True, (255, 255, 255))
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    
    if game_over:
        over_text = font_large.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
        restart_text = font_small.render("Нажмите R для перезапуска", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()