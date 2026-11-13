import pygame

class Cell:
    def __init__(self, row, col, screenSize):
        self.tile_width = screenSize[0] // 10
        self.tile_height = screenSize[1] // 10
        
        # cell
        self.image = pygame.image.load("Python/Campo Minado/assets/pixil-layer-Background.png")
        self.image = pygame.transform.scale(self.image, (self.tile_width, self.tile_height))

        # bomb
        self.bomb_image = pygame.image.load("Python/Campo Minado/assets/bomb_cell.png")
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.tile_width, self.tile_height))
        
        self.row = row
        self.col = col
        
        self.x = col * self.tile_width
        self.y = row * self.tile_height
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.is_bomb = False
        self.clicked = False
        self.flagged = False
        

    def draw(self, surface):
        if self.clicked and self.is_bomb:
            surface.blit(self.bomb_image, self.rect)
        elif self.clicked and not self.is_bomb:
            surface.blit(self.number_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

    def calculate_adjacent_bombs(self, grid):
            self.adjacent_bombs = 0 
            
            for r_offset in [-1, 0, 1]:
                for c_offset in [-1, 0, 1]:
                    if r_offset == 0 and c_offset == 0:
                        continue
                    
                    neighbor_row = self.row + r_offset
                    neighbor_col = self.col + c_offset
                    
                    if 0 <= neighbor_row < 10 and 0 <= neighbor_col < 10:
                        neighbor_cell = grid[neighbor_row][neighbor_col]
                        
                        if neighbor_cell.is_bomb:
                            self.adjacent_bombs += 1
            
            if self.adjacent_bombs >= 0:
                self.number_image = pygame.image.load(f"Python/Campo Minado/assets/{self.adjacent_bombs}.png")
                self.number_image = pygame.transform.scale(self.number_image, (self.tile_width, self.tile_height))