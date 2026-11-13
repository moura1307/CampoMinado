import pygame

class Button(object):
    def __init__(self, position, size, filename, font, text , iconFile):
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect(topleft=position)

        self.text = text
        self.font = pygame.font.Font(font, size[1]//2)
        self.text_surface = self.font.render(self.text, True, "black")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        self.icon = None
        if iconFile != None:
            self.icon = pygame.image.load(iconFile)

            orig_w = self.icon.get_width()
            orig_h = self.icon.get_height()

            aspect_ratio = orig_w / orig_h

            target_h = size[1]*0.7
            target_w = int(target_h * aspect_ratio)

            self.icon = pygame.transform.scale(self.icon, (target_w, target_h))

    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
        if self.icon == None:
            surface.blit(self.text_surface, self.text_rect)
        else:
            total_width = self.icon.get_width() + self.text_surface.get_width() + 10
            
            start_x = self.rect.centerx - (total_width / 2)
            self.icon_rect = self.icon.get_rect(midleft=(start_x, self.rect.centery-2))
            
            text_start_x = start_x + self.icon.get_width() + 10
            self.text_rect = self.text_surface.get_rect(midleft=(text_start_x, self.rect.centery+2))
            
            surface.blit(self.icon, self.icon_rect)
            surface.blit(self.text_surface, self.text_rect)
     
    def check_press(self,position):
        if self.rect.collidepoint(*position):
            return True
        return False