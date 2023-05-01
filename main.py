import pygame
from grid import *
from snake import *
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
 
# initialize pygame
pygame.init()
screen_size = (700, 500)
 
# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("pygame Test")
 
# clock is used to set a max fps
clock = pygame.time.Clock()
 
grid = Grid(50, screen, RED)
snake = Snake(50, screen, WHITE)

pygame.mixer.music.load("./assets/bgm.mp3")
#pygame.mixer.music.play(-1)

running = True
while running:
    #print("Loop")

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
            
        if event.type == pygame.QUIT:
            running = False

    # game logic
    snake.move()
    if snake.out_of_bounds():
        snake.die()
     
    # drawing logic
    screen.fill(BLACK)
    grid.draw()
    snake.draw()
    pygame.display.flip()
    
    # how many updates per second
    clock.tick(1)

pygame.quit()