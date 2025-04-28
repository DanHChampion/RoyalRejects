import pygame

class Character():
    def __init__(self):
        self.power = 10
        self.defense = 10
        self.speed = 5
        self.jump_height = 10
        self.mass = 10
        self.hitbox = pygame.Rect(0, 0, 50, 50)

    def update(self, entity):
        jump_height = self.jump_height

        force_applied = 0.0

        if entity.intention.move_left:
            if entity.dashed == True and entity.direction == 1:
                entity.dashed = False
            entity.direction = -1
            force_applied = -1 if entity.dashed == False else -2
            if entity.on_ground:
                entity.state = 'walking'
                if entity.intention.dodge:
                    entity.dashed = True
                    force_applied = -8
        elif entity.intention.move_right:
            if entity.dashed == True and entity.direction == -1:
                entity.dashed = False
            entity.direction = 1
            force_applied = 1 if entity.dashed == False else 2
            if entity.on_ground:
                entity.state = 'walking'
                if entity.intention.dodge:
                    entity.dashed = True
                    force_applied = 8
        if not entity.intention.move_left and not entity.intention.move_right:
            entity.state = 'idle'
            entity.dashed = False
        if entity.intention.jump and entity.on_ground:
            entity.y_speed = -jump_height
            entity.on_ground = False
        if not entity.on_ground and entity.y_speed != 0:
            entity.state = 'jumping'
            if entity.intention.move_down:
                entity.state = 'fastfalling'
                entity.y_acceleration = 2
            else:
                entity.y_acceleration = 0.4
        if not entity.on_ground and entity.double_jump == False and entity.intention.jump:
            # double jump allowed once after 0.1 seconds
            if entity.y_speed > (jump_height*-0.5):
                entity.double_jump = True
                entity.y_speed = -jump_height
        if entity.on_ground and entity.double_jump == True:
            entity.double_jump = False
        
        physics = {
            'character': self,
            'x_force': force_applied,
            'y_force':0,
        }
        return physics
        

