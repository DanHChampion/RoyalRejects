import pygame
from characters.character import Character
from constants import *
import globals

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen=None, input_stream=None):
        for entity in globals.map.entities:
            if self.check(entity):
                self.update_entity(screen, input_stream, entity)
    def update_entity(self, screen, input_stream, entity):
        pass

class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None
    def update_entity(self, screen, input_stream, entity):    
        entity.animations.animation_list[entity.state].update()

class CameraSystem(System):
    def check(self, entity):
        return entity.camera is not None
    def update_entity(self, screen, input_stream, entity):
        # fill camera background

        camera_rect = entity.camera.rect
        clip_rect = pygame.Rect(
            camera_rect.x,
            camera_rect.y,
            camera_rect.w,
            camera_rect.h)
        screen.set_clip(clip_rect)

        # screen.fill(WHITE)

        # render platforms
        for p in globals.map.platforms:
            new_pos_rect = pygame.Rect(
                p.x,
                p.y,
                p.w,
                p.h)
            pygame.draw.rect(screen, GREY, new_pos_rect)

        # render entities
        for e in globals.map.entities:
            s = e.state
            a = e.animations.animation_list[s]
            a.draw(screen, e,
                e.position.rect.x,
                e.position.rect.y,
                e.direction == -1, False)
            
        screen.set_clip(None)

class InputSystem(System):
    def check(self, entity):
        return entity.input is not None and entity.intention is not None
    def update_entity(self, screen, input_stream, entity):
        # up = jump
        if input_stream.keyboard.is_key_pressed(entity.input.jump):
            entity.intention.jump = True
        else:
            entity.intention.jump = False
        # left = move_left
        if input_stream.keyboard.is_key_down(entity.input.left):
            entity.intention.move_left = True
        else:
            entity.intention.move_left = False
        # right = move_right    
        if input_stream.keyboard.is_key_down(entity.input.right):
            entity.intention.move_right = True
        else:
            entity.intention.move_right = False
        # down = move_down
        if input_stream.keyboard.is_key_down(entity.input.down):
            entity.intention.move_down = True
        else:
            entity.intention.move_down = False
        if input_stream.keyboard.is_key_pressed(entity.input.dodge):
            entity.intention.dodge = True
        else:
            entity.intention.dodge = False

class PhysicsSystem(System): 
    def check(self, entity):
        return entity.position is not None
    def update_entity(self, screen, input_stream, entity):
        new_x = entity.position.rect.x
        new_y = entity.position.rect.y

        ground_max_speed = 4 if entity.dashed == False else 10
        air_max_speed = 2 if entity.dashed == False else 8
        force_applied = 0.0
        if entity.intention is not None:
            physics = entity.character.update(entity)
            force_applied = physics['x_force']
        
        ground_max_speed = 4 if entity.dashed == False else 10
        air_max_speed = 2 if entity.dashed == False else 8

        if entity.intention.move_left or entity.intention.move_right:
            if entity.on_ground:
                if abs(entity.x_speed) < ground_max_speed:
                    entity.x_acceleration = force_applied
                else:
                    entity.x_acceleration = 0.0
            else:
                if abs(entity.x_speed) < air_max_speed:
                    entity.x_acceleration = force_applied
                else:
                    entity.x_acceleration = 0.0
        
        drag_force = 0.0
        drag_coefficient = 0.2
        drag_force = drag_coefficient * entity.x_speed * -1  # Opposite direction

        net_x_acceleration = force_applied + drag_force

        if abs(entity.x_acceleration) < 0.5:
            entity.x_acceleration = 0.0
        if entity.x_speed > -1.0 and entity.x_speed < 0 and not entity.intention.move_left:
            entity.x_speed = 0.0

        entity.x_acceleration = net_x_acceleration
        entity.x_speed += net_x_acceleration

        new_x += entity.x_speed

        # new_x_rect = pygame.Rect(
        #     int(new_x),
        #     int(entity.position.rect.y),
        #     entity.position.rect.width,
        #     entity.position.rect.height)
        
        # x_collision = False

        # #...check against every platform
        # for platform in globals.map.platforms:
        #     if platform.colliderect(new_x_rect):
        #         x_collision = True
        #         entity.x_speed = 0  # Stop horizontal movement on collision
        #         break

        # if not x_collision:
        entity.position.rect.x = new_x
        
        # vertical movement
        entity.y_speed += entity.y_acceleration
        new_y += entity.y_speed

        new_y_rect = pygame.Rect(
            int(entity.position.rect.x),
            int(new_y),
            entity.position.rect.width,
            entity.position.rect.height)
        
        y_collision = False
        entity.on_ground = False

        # collision with platforms
        for platform in globals.map.platforms:
            if platform.colliderect(new_y_rect):
                y_collision = True
                entity.y_speed = 0
                entity.on_ground = True
                if platform[1] >= new_y:
                    entity.position.rect.y = platform[1] - entity.position.rect.height+1
                    # entity.on_ground = True
                break

        if not y_collision:
            entity.position.rect.y = int(new_y)


        pygame.draw.rect(screen, BLUE, (entity.position.rect.x, entity.position.rect.y, entity.position.rect.width, entity.position.rect.height), 2)  # Draw the bounding box
        
        # reset intentions
        if entity.intention is not None:
            entity.intention.move_left = False
            entity.intention.move_right = False
            entity.intention.move_down = False
            entity.intention.jump = False
    
class Camera():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)
 
class Position():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x,y,w,h)

class Animations():
    def __init__(self):
        self.animation_list = {}
        self.alpha = 255
    def add(self, state, animation):
        self.animation_list[state] = animation

class Animation():
    def __init__(self, frames, duration = 30.0):
        self.frames = frames
        self.duration = duration
        self.current_frame = 0
        self.time_per_frame = duration / len(frames)
        self.elapsed_time = 0
        self.scale = 2.0

    def update(self, delta_time = 1):
        self.elapsed_time += delta_time
        if self.elapsed_time >= self.time_per_frame:
            self.elapsed_time -= self.time_per_frame
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

    def draw(self, screen, entity, x, y, flipX, flipY):
        flipped_frame = pygame.transform.flip(self.frames[self.current_frame], flipX, flipY)
        scaled_frame = pygame.transform.scale(flipped_frame, (
            int(self.frames[self.current_frame].get_width() * self.scale),
            int(self.frames[self.current_frame].get_height() * self.scale)
        ))
        offset_x = scaled_frame.get_width() // 2 - entity.position.rect.width // 2
        offset_y = scaled_frame.get_height() - entity.position.rect.height
        screen.blit(scaled_frame, (x - offset_x, y - offset_y))
        pygame.draw.rect(screen, RED, (x - offset_x, y - offset_y, scaled_frame.get_width(), scaled_frame.get_height()), 1)  # Draw the bounding box

class Intention:
    def __init__(self):
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.jump = False
        self.dodge = False

class Input:
    def __init__(self, up, down, left, right, jump, light, heavy, dodge):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.jump = jump
        self.light = light
        self.heavy = heavy
        self.dodge = dodge


class Entity():
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.animations = Animations()
        self.position = None
        self.direction = 1 # 1 for right, -1 for left
        self.camera = None
        self.x_speed = 0
        self.x_acceleration = 0.0
        self.y_speed = 0
        self.y_acceleration = 0.2 # gravity
        self.on_ground = False
        self.input = None
        self.intention = None
        self.character = Character()
        self.double_jump = False
        self.dashed = False
