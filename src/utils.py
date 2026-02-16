import pygame
import engine

# idle0 = pygame.image.load('images/vita/vita_00.png')
# idle1 = pygame.image.load('images/vita/vita_01.png')
# idle2 = pygame.image.load('images/vita/vita_02.png')
# idle3 = pygame.image.load('images/vita/vita_03.png')

idle0 = pygame.image.load('images/prince/prince_idle_0.png')
idle1 = pygame.image.load('images/prince/prince_idle_1.png')
idle2 = pygame.image.load('images/prince/prince_idle_2.png')
idle3 = pygame.image.load('images/prince/prince_idle_3.png')

walking0 = pygame.image.load('images/prince/prince_walk_0.png')
walking1 = pygame.image.load('images/prince/prince_walk_1.png')
walking2 = pygame.image.load('images/prince/prince_walk_2.png')
walking3 = pygame.image.load('images/prince/prince_walk_3.png')
walking4 = pygame.image.load('images/prince/prince_walk_4.png')
walking5 = pygame.image.load('images/prince/prince_walk_5.png')

jumping0 = pygame.image.load('images/prince/prince_jump_0.png')

ffalling0 = pygame.image.load('images/prince/prince_ffall_0.png')

jab0 = pygame.image.load('images/prince/prince_jab_0.png')
jab1 = pygame.image.load('images/prince/prince_jab_1.png')
jab2 = pygame.image.load('images/prince/prince_jab_2.png')

nair0 = pygame.image.load('images/prince/prince_nair_0.png')

def makePlayer(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,32,72)
    entityIdleAnimation = engine.Animation([idle0, idle1, idle2, idle3])
    entityWalkingAnimation = engine.Animation([walking0, walking1, walking2, walking3, walking4, walking5])
    entityJumpingAnimation = engine.Animation([jumping0])
    entityFastFallingAnimation = engine.Animation([ffalling0])
    entityJabAnimation = engine.Animation([jab0, jab1, jab2], 15.0)  # Faster animation for attack
    entityNairAnimation = engine.Animation([nair0], 15.0)  # Single frame for now
    entity.animations.add('idle', entityIdleAnimation)
    entity.animations.add('walking', entityWalkingAnimation)
    entity.animations.add('jumping', entityJumpingAnimation)
    entity.animations.add('fastfalling', entityFastFallingAnimation)
    entity.animations.add('jab', entityJabAnimation)
    entity.animations.add('nair', entityNairAnimation)
    entity.type = 'player'
    entity.intention = engine.Intention()
    return entity

def makeDummy(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,32,72)
    entityIdleAnimation = engine.Animation([idle0, idle1, idle2, idle3])
    entity.animations.add('idle', entityIdleAnimation)
    entity.type = 'dummy'
    return entity