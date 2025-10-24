score = 0
missed_import pygame
import random

pygame.init()
pygame.mixer.init()

screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("nu pogodi")

font_size = 30
font = pygame.font.Font(None, font_size)

start_x_range = [0, screen_width] 
start_y_range = [50, screen_height - 50] 

egg_speed = 3  
player_radius = 30
max_missed_eggs = 3
font_color = (255, 255, 255)

eggs = 0
game_over = False

background_volk = pygame.image.load("cartinka.png")
background_volk = pygame.transform.scale(background_volk, (screen_width, screen_height))
background = background_volk
korzinka_image = pygame.image.load("corzina.jpg").convert_alpha()
korzinka_image = pygame.transform.scale(korzinka_image, (player_radius * 2, player_radius * 2))
korzinka_image.set_colorkey((255, 255, 255))
egg_image = pygame.image.load("egg.png").convert_alpha()
egg_width = 30
egg_height = 30
egg_image = pygame.transform.scale(egg_image, (egg_width, egg_height))
egg_image.set_colorkey((255, 255, 255))
key_sound = pygame.mixer.Sound("funky-pulse_93559.wav")
key_sound.play(-1)
player_x = screen_width // 2
player_y = screen_height - 50
running = True
clock = pygame.time.Clock()
eggs = []
spawn_interval = 2000  
last_spawn_time = 0
def display_text(text, x, y, color):
    """Отображает текст на экране."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.MOUSEMOTION:
                player_x, player_y = event.pos
                player_x = max(player_radius, min(player_x, screen_width - player_radius))
                player_y = max(player_radius, min(player_y, screen_height - player_radius))

    if game_over:
        key_sound.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0, 0))
        display_text(f"Счет: {score}", screen_width // 2, screen_height // 2 - 30, font_color)
        display_text(f"Пропущено: {missed_eggs}", screen_width // 2, screen_height // 2, font_color)
        display_text("Игра окончена!", screen_width // 2, screen_height // 2 + 30, font_color)
        pygame.display.flip()
        clock.tick(60)
        continue
    if current_time - last_spawn_time > spawn_interval:
        start_x = random.choice([0, screen_width])
        start_y = random.randint(start_y_range[0], start_y_range[1])
        x_direction = 1 if start_x == 0 else -1
        y_direction = random.uniform(-0.5, 0.5) 
        eggs.append([start_x, start_y, x_direction, y_direction]) 
        last_spawn_time = current_time
    eggs_on_screen = []
    for egg_x, egg_y, x_direction, y_direction in eggs:
        egg_x += egg_speed * x_direction
        egg_y += egg_speed * y_direction
       
        egg_rect = pygame.Rect(0, 0, egg_width, egg_height)
        egg_rect.center = (int(egg_x), int(egg_y))
        korzinka_rect = pygame.Rect(0, 0, player_radius * 2, player_radius * 2)
        korzinka_rect.center = (int(player_x), int(player_y))
       
        if korzinka_rect.colliderect(egg_rect):
            score += 1
           
        elif egg_x > 0 and egg_x < screen_width and egg_y > 0 and egg_y < screen_height:
                eggs_on_screen.append([egg_x, egg_y, x_direction, y_direction])
        
        else:
            
            missed_eggs += 1
            if missed_eggs >= max_missed_eggs:
                game_over = True
 eggs = eggs_on_screen
    screen.blit(background, (0, 0))
    for egg_x, egg_y,_,_ in eggs:
        egg_rect = pygame.Rect(0, 0, egg_width, egg_height)
        egg_rect.center = (int(egg_x), int(egg_y))
        screen.blit(egg_image, egg_rect)
    korzinka_rect = pygame.Rect(0, 0, player_radius * 2, player_radius * 2)
    korzinka_rect.center = (int(player_x), int(player_y))
    screen.blit(korzinka_image, korzinka_rect)
    display_text(f"Счет: {score}", 50, 30, font_color)
    display_text(f"Пропущено: {missed_eggs}", 190, 30, font_color)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()