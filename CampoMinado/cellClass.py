import pygame


class Cell:
    _loaded_size = None
    bg_img = None
    bomb_img = None
    flag_img = None
    number_imgs = []

    @classmethod
    def load_images(cls, tile_w, tile_h):
        def load(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (tile_w, tile_h))

        cls.bg_img = load("assets/pixil-layer-Background.png")
        cls.bomb_img = load("assets/bomb_cell.png")
        cls.flag_img = load("assets/flag.png")
        cls.number_imgs = [load(f"assets/{n}.png") for n in range(9)]
        cls._loaded_size = (tile_w, tile_h)

    def __init__(self, row, col, screenSize, tiles=10):
        self.tile_width = screenSize[0] // tiles
        self.tile_height = screenSize[1] // tiles

        if Cell._loaded_size != (self.tile_width, self.tile_height):
            Cell.load_images(self.tile_width, self.tile_height)

        self.row = row
        self.col = col
        self.x = col * self.tile_width
        self.y = row * self.tile_height
        self.rect = pygame.Rect(self.x, self.y, self.tile_width, self.tile_height)

        self.is_bomb = False
        self.clicked = False
        self.flagged = False
        self.adjacent_bombs = 0

    def draw(self, surface):
        if self.flagged:
            surface.blit(Cell.flag_img, self.rect)
        elif self.clicked and self.is_bomb:
            surface.blit(Cell.bomb_img, self.rect)
        elif self.clicked:
            surface.blit(Cell.number_imgs[self.adjacent_bombs], self.rect)
        else:
            surface.blit(Cell.bg_img, self.rect)

    def neighbors(self, grid):
        # os limites sao do tamnho da grid
        rows = len(grid)
        cols = len(grid[0])
        for r_offset in (-1, 0, 1):
            for c_offset in (-1, 0, 1):
                if r_offset == 0 and c_offset == 0:
                    continue
                neighbor_row = self.row + r_offset
                neighbor_col = self.col + c_offset
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    yield grid[neighbor_row][neighbor_col]

    def calculate_adjacent_bombs(self, grid):
        self.adjacent_bombs = sum(1 for n in self.neighbors(grid) if n.is_bomb)

    def revealNeighbors(self, grid):
        for neighbor_cell in self.neighbors(grid):
            if neighbor_cell.clicked:
                continue
            neighbor_cell.clicked = True
            neighbor_cell.flagged = False

            if neighbor_cell.adjacent_bombs == 0:
                neighbor_cell.revealNeighbors(grid)