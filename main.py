import pygame
from grid import *
from snake import *
from apple import *
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
 
# initialize pygame
pygame.init()
screen_size = (700, 500)
 
# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake")
 
# clock is used to set a max fps
clock = pygame.time.Clock()
 
grid = Grid(50, screen, RED)
snake = Snake(50, screen, WHITE)
apple = Apple(25, 50, screen, GREEN)

pygame.mixer.music.load("./assets/bgm2.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

running = True
paused = False
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.set_direction(Direction.RIGHT)
            elif event.key == pygame.K_UP:
                snake.set_direction(Direction.UP)
            elif event.key == pygame.K_DOWN:
                snake.set_direction(Direction.DOWN)

            # cheat codes
            elif event.key == pygame.K_a:
                apple.reset()
            elif event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                    continue
                else:
                    pygame.mixer.music.play(-1)
            
        if event.type == pygame.QUIT:
            running = False

    # game logic
    if paused:
        continue

    snake.move()
    if snake.out_of_bounds():
        snake.die("Out of bounds!")
    elif snake.eating_self():
        snake.die("Collision with self!")
    elif snake.eating_apple(apple):
        apple.reset()
        snake.eat()
     
    # drawing logic
    screen.fill(BLACK)
    grid.draw()
    snake.draw()
    apple.draw()
    pygame.display.flip()
    
    # how many updates per second
    clock.tick(1)

pygame.quit()