import pygame
import engine
import utils
import globals
from map import Map
from inputstream import InputStream
from constants import *

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Royal Rejects")
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)


input_stream = InputStream()

cameraSystem = engine.CameraSystem()
animationSystem = engine.AnimationSystem()
physicsSystem = engine.PhysicsSystem()
inputSystem = engine.InputSystem()

globals.map = Map()

player = globals.map.entities[0]
player.camera = engine.Camera(10, 10, SCREEN_WIDTH-20, SCREEN_HEIGHT-20)
player.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE, pygame.K_j, pygame.K_k, pygame.K_l)


running = True
# Game Loop
while running:
    # -------
    # INPUT
    # -------
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    input_stream.process_input()

    # -------
    # UPDATE
    # -------

    # entities
    for entity in globals.map.entities:
        entity.animations.animation_list[entity.state].update()

    # # dummy collision
    # for entity in globals.map.entities:
    #     if entity.type == 'dummy':
    #         if entity.position.rect.colliderect(player.position.rect):
    #             # player.damage += 1
    #             player.position.rect.x = 100
    #             player.position.rect.y = 200
    #             player_speed = 0
    
    # fall off screen
    if player.position.rect.y > SCREEN_HEIGHT or player.position.rect.x < 0 or player.position.rect.x > SCREEN_WIDTH:
        player.position.rect.x = 100
        player.position.rect.y = 200
        player_speed = 0

    screen.fill(BACKGROUND_COLOR)
    inputSystem.update(screen=screen, input_stream=input_stream)
    physicsSystem.update(screen=screen, input_stream=input_stream)
    cameraSystem.update(screen)

    pygame.display.flip()

    # tick
    clock.tick(FPS)

# quit
pygame.quit()