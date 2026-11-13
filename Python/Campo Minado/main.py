import pygame
import random
from buttonClass import Button
from textClass import Label
from cellClass import Cell

# pygame setup
def startup():
    pygame.init()
    screenSize = 480
    screen = pygame.display.set_mode((screenSize, screenSize))

    pygame.display.set_caption("Mine Sweeper")
    pygame.display.set_icon(pygame.image.load('Python/Campo Minado/assets/bomb.png'))

    boldFont = 'Python/Campo Minado/assets/font/MSW98UI-Bold.ttf'
    regularFont = 'Python/Campo Minado/assets/font/MSW98UI-Regular.ttf'

    clock = pygame.time.Clock()
    running = True

    return running, screen, screenSize, clock, regularFont, boldFont

# menu 
def setupMenu():
    playButton = Button((((screenSize-228)/2, ((screenSize-96)/2))),((228, 96)),"Python/Campo Minado/assets/clean_5724.png", boldFont, "Start", "Python/Campo Minado/assets/bomb.png")
    #diffButton = Button((((screenSize-(int(228*0.70)))/2, ((screenSize-int(96*0.70))/2)+40)),((int(228*0.75), int(96*0.75))),"Python/Campo Minado/assets/clean_5724.png", boldFont, "Easy", None)

    posx, posy = screen.get_rect().midbottom
    creditText = Label("Made by: Moura Brandão", (posx, posy - 10), regularFont, 16, "black", "midbottom",)

    return playButton, creditText

# coisa do jogo de fato
def configureGame():

    tile_size = 10

    grid = []
    for row in range(10):
        current_row = []
        for col in range(10):
            new_tile = Cell(row, col, (screenSize, screenSize))
            current_row.append(new_tile)
        grid.append(current_row)

    # lista única com as 100 células
    all_cells = [cell for row in grid for cell in row]

    bombs = random.sample(all_cells, 12)
    for cell in bombs:
        cell.is_bomb = True

    # depois que as bombas estao colocadas, calcule os vizinhos
    for cell in all_cells:
        cell.calculate_adjacent_bombs(grid)

    return all_cells

running, screen, screenSize, clock, regularFont, boldFont = startup()
all_cells = configureGame()
playButton, creditText = setupMenu()

gameState = "MENU"
while running:
    screen.fill("gray")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if gameState == "MENU":
        playButton.draw(screen)
        #diffButton.draw(screen)
        creditText.draw(screen)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.check_press(event.pos):
                gameState = "GAME"
                
    elif gameState == "GAME":
        for tile in all_cells:
            tile.draw(screen)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tile.rect.collidepoint(event.pos):
                    if pygame.mouse.get_pressed[0]:
                        tile.clicked = True
                    elif pygame.mouse.get_pressed[2]:
                        if tile.flagged:
                            tile.flagged = False
                        else:
                            tile.flagged = True
                        

        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

