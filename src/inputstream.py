import pygame

class Keyboard:
    def __init__(self):
        self.current_key_states = None
        self.previous_key_states = None
    def process_input(self):
        self.previous_key_states = self.current_key_states
        self.current_key_states = pygame.key.get_pressed()
    def is_key_down(self, key_code):
        if self.current_key_states is None or self.previous_key_states is None:
            return False
        return self.current_key_states[key_code] == True
    def is_key_pressed(self, key_code):
        if self.current_key_states is None or self.previous_key_states is None:
            return False
        return self.current_key_states[key_code] == True and self.previous_key_states[key_code] == False
    def is_key_released(self, key_code):
        if self.current_key_states is None or self.previous_key_states is None:
            return False
        return self.current_key_states[key_code] == False and self.previous_key_states[key_code] == True

class InputStream:
    def __init__(self):
        self.keyboard = Keyboard()
    def process_input(self):
        self.keyboard.process_input()