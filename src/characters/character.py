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

        # Handle attack logic first
        if entity.attack_cooldown > 0:
            entity.attack_cooldown -= 1
            
        if entity.is_attacking:
            entity.attack_timer -= 1
            if entity.attack_timer <= 0:
                entity.is_attacking = False
                # Return to appropriate state after attack
                if entity.on_ground:
                    if entity.intention.move_left or entity.intention.move_right:
                        entity.state = 'walking'
                    else:
                        entity.state = 'idle'
                else:
                    entity.state = 'jumping'
        
        # Check for attack input (only when not already attacking and cooldown finished)
        if entity.intention.attack and not entity.is_attacking and entity.attack_cooldown <= 0:
            entity.is_attacking = True
            entity.attack_timer = 15  # Attack duration in frames
            entity.attack_cooldown = 3  # Cooldown between attacks in frames
            
            # Determine attack type based on state
            if entity.on_ground:
                entity.state = 'jab'  # Ground attack
            else:
                entity.state = 'nair'  # Neutral air attack
        
        # Only handle movement and state changes if not attacking
        if not entity.is_attacking:
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
        else:
            # During attacks, still allow basic movement input to be processed for force
            if entity.intention.move_left:
                # entity.direction = -1
                force_applied = -0.5  # Reduced movement during attack
            elif entity.intention.move_right:
                # entity.direction = 1
                force_applied = 0.5   # Reduced movement during attack
        if entity.on_ground and entity.double_jump == True:
            entity.double_jump = False
        
        physics = {
            'character': self,
            'x_force': force_applied,
            'y_force':0,
        }
        return physics
        

