import pygame
import math
import random

# 1. ИНИЦИАЛИЗАЦИЯ И НАСТРОЙКИ ЭКРАНА
pygame.init()
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Солнечная система")
cx, cy = WIDTH // 2, HEIGHT // 2
clock = pygame.time.Clock()
FPS = 60

# 2. ОПРЕДЕЛЕНИЕ КЛАССА PLANET 
class Planet:
    def __init__(self, color, x, y, angle, orbit, radius, speed):
        self.color = color
        self.x, self.y = x, y
        self.angle = angle
        self.orbit = orbit
        self.radius = radius
        self.speed = speed

    def update(self, dt):
        self.angle += self.speed * dt
        self.x = cx + self.orbit * math.cos(self.angle)
        self.y = cy + self.orbit * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# 3. СОЗДАНИЕ ВСЕХ ОБЪЕКТОВ С НОВЫМИ ЦВЕТАМИ



sun_color = (255, 100, 0) 
sun_radius = 40


mercury = Planet(color=(0, 100, 80),     x=0, y=0, angle=0, orbit=80,  radius=8,  speed=2.0)    
venus =   Planet(color=(255, 0, 150),   x=0, y=0, angle=0, orbit=130, radius=14, speed=1.5)    
earth =   Planet(color=(50, 220, 50),   x=0, y=0, angle=0, orbit=200, radius=16, speed=1.0)    
mars =    Planet(color=(200, 180, 0),    x=0, y=0, angle=0, orbit=280, radius=10,  speed=0.7)    
jupiter = Planet(color=(180, 150, 255), x=0, y=0, angle=0, orbit=380, radius=35, speed=0.4)    
saturn =  Planet(color=(0, 255, 255),   x=0, y=0, angle=0, orbit=480, radius=30, speed=0.25)   
uranus =  Planet(color=(240, 240, 240), x=0, y=0, angle=0, orbit=570, radius=25, speed=0.15)  
neptune = Planet(color=(130, 0, 0),     x=0, y=0, angle=0, orbit=650, radius=24, speed=0.1)    

# Астероиды
asteroids = []
for _ in range(300):
    angle = random.uniform(0, 2 * math.pi)
    orbit_radius = random.uniform(310, 340)
    asteroids.append([angle, orbit_radius])

# Комета
comet_x = -100
comet_y = random.randint(100, HEIGHT - 100)
comet_speed = 250

# Луна
moon_angle = 0
moon_speed = 1.8
moon_dist = 35

# 4. ОСНОВНОЙ ЦИКЛ 
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление координат всех объектов
    mercury.update(dt)
    venus.update(dt)
    earth.update(dt)
    mars.update(dt)
    jupiter.update(dt)
    saturn.update(dt)
    uranus.update(dt)
    neptune.update(dt)
    
    comet_x += comet_speed * dt
    if comet_x > WIDTH + 100:
        comet_x = -100
        comet_y = random.randint(100, HEIGHT - 100)

   
    screen.fill((20, 0, 30)) 

    pygame.draw.circle(screen, sun_color, (cx, cy), sun_radius)

    # Орбиты 
    pygame.draw.circle(screen, (0, 70, 70), (cx, cy), 200, 1) 
    pygame.draw.circle(screen, (0, 70, 70), (cx, cy), 380, 1) 

    # Астероиды 
    for ast in asteroids:
        ast[0] += 0.3 * dt
        ax = cx + ast[1] * math.cos(ast[0])
        ay = cy + ast[1] * math.sin(ast[0])
        pygame.draw.circle(screen, (150, 75, 0), (int(ax), int(ay)), 1) 

    
    pygame.draw.ellipse(screen, (150, 255, 150), (int(comet_x), int(comet_y), 30, 15))

    mercury.draw()
    venus.draw()
    earth.draw()
    mars.draw()
    jupiter.draw()
    saturn.draw()
    uranus.draw()
    neptune.draw()

    
    moon_angle += moon_speed * dt
    mx = earth.x + moon_dist * math.cos(moon_angle)
    my = earth.y + moon_dist * math.sin(moon_angle)
    pygame.draw.circle(screen, (255, 255, 255), (int(mx), int(my)), 5)

    pygame.display.flip()

pygame.quit()