import pygame

class Label:
    def __init__(self, text, position, font_name=None, font_size=36, color="white", align="topleft"):
        self.font = pygame.font.Font(font_name, font_size)
        self.color = color
        self.text = text
        
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(**{align: position})

    def draw(self, surface):
        surface.blit(self.surface, self.rect)