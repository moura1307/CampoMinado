import pygame
import random
from buttonClass import Button
from textClass import Label
from cellClass import Cell
from imageClass import Image

# presets de dificuldade: tiles = células por lado, bombs = quantidade de bombas
# (480 é divisível por 10, 15 e 20, então as células sempre encaixam certinho)
DIFFICULTIES = [
    {"name": "Easy",   "tiles": 10, "bombs": 12},
    {"name": "Medium", "tiles": 15, "bombs": 30},
    {"name": "Hard",   "tiles": 20, "bombs": 60},
]

# pygame setup
def startup():
    pygame.init()
    screenSize = 480
    screen = pygame.display.set_mode((screenSize, screenSize))

    pygame.display.set_caption("Mine Sweeper")
    pygame.display.set_icon(pygame.image.load('assets/bomb.png'))

    boldFont = 'assets/font/MSW98UI-Bold.ttf'
    regularFont = 'assets/font/MSW98UI-Regular.ttf'

    clock = pygame.time.Clock()
    running = True

    return running, screen, screenSize, clock, regularFont, boldFont

# menu
def setupMenu():
    centerx = screenSize // 2

    # tudo empilhado de cima pra baixo, centralizado no mesmo eixo
    titleText = Label("Mine Sweeper", (centerx, 90), boldFont, 48, "black", "center")

    playSize = (228, 96)
    playPos = (centerx - playSize[0] // 2, 160)
    playButton = Button(playPos, playSize, "assets/clean_5724.png", boldFont, "Start", "assets/bomb.png")

    # um botão pronto pra cada dificuldade (mesma posição/tamanho, só muda o texto)
    diffSize = (171, 72)
    diffPos = (centerx - diffSize[0] // 2, playPos[1] + playSize[1] + 20)
    diffButtons = [
        Button(diffPos, diffSize, "assets/clean_5724.png", boldFont, d["name"], None)
        for d in DIFFICULTIES
    ]

    # linha de info embaixo do botão de dificuldade
    infoY = diffPos[1] + diffSize[1] + 25
    infoTexts = [
        Label(f'{d["tiles"]}x{d["tiles"]} grid, {d["bombs"]} bombs', (centerx, infoY), regularFont, 16, "black", "center")
        for d in DIFFICULTIES
    ]

    posx, posy = screen.get_rect().midbottom
    creditText = Label("Made by: Moura Brandão", (posx, posy - 10), regularFont, 16, "black", "midbottom")

    return titleText, playButton, diffButtons, infoTexts, creditText

# definicao de vitoria
def setupWin():
    centerx, centery = screen.get_rect().center
    winText = Label("You Win!", (centerx, centery), boldFont, 48, "white", "center")
    hintText = Label("Click to return to the menu", (centerx, centery + 50), regularFont, 16, "white", "center")

    # semi-transparent dark layer drawn over the board
    winOverlay = pygame.Surface((screenSize, screenSize), pygame.SRCALPHA)
    winOverlay.fill((0, 0, 0, 140))

    return winText, hintText, winOverlay

def checkWin(cells):
    return all(cell.clicked for cell in cells if not cell.is_bomb)

# coisa do jogo de fato
def configureGame(diff):
    tiles = DIFFICULTIES[diff]["tiles"]
    bomb_count = DIFFICULTIES[diff]["bombs"]

    grid = []
    for row in range(tiles):
        current_row = []
        for col in range(tiles):
            # a célula precisa saber quantas células cabem na tela pra calcular o tamanho
            new_tile = Cell(row, col, (screenSize, screenSize), tiles)
            current_row.append(new_tile)
        grid.append(current_row)

    # lista única com todas as células
    all_cells = [cell for row in grid for cell in row]

    bombs = random.sample(all_cells, bomb_count)
    for cell in bombs:
        cell.is_bomb = True

    # depois que as bombas estao colocadas, calcule os vizinhos
    for cell in all_cells:
        cell.calculate_adjacent_bombs(grid)

    return all_cells, grid

running, screen, screenSize, clock, regularFont, boldFont = startup()
titleText, playButton, diffButtons, infoTexts, creditText = setupMenu()
winText, hintText, winOverlay = setupWin()

gameState = "MENU"
exploding = False
explosion_frame = 0
last_frame_time = 0
difficulty = 0

explosion_frames = []
for frame in range(16):
    explosion_frames.append(Image(f"assets/explosion/{frame}.png", (0, 0), (screenSize+20, screenSize+20)))

while running:
    screen.fill("gray")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gameState == "MENU" and event.button == 1:
                if playButton.check_press(event.pos):
                    all_cells, grid = configureGame(difficulty)
                    gameState = "GAME"

                # um clique = uma troca de dificuldade
                elif diffButtons[difficulty].rect.collidepoint(event.pos):
                    difficulty = (difficulty + 1) % len(DIFFICULTIES)

            elif gameState == "GAME" and not exploding:
                for tile in all_cells:
                    if not tile.rect.collidepoint(event.pos):
                        continue

                    # botão esquerdo: revela
                    if event.button == 1 and not tile.flagged and not tile.clicked:
                        tile.clicked = True

                        if tile.adjacent_bombs == 0 and not tile.is_bomb:
                            tile.revealNeighbors(grid)

                        if tile.is_bomb:
                            exploding = True
                            explosion_frame = 0
                            last_frame_time = pygame.time.get_ticks()

                    # botão direito: bandeira
                    elif event.button == 3 and not tile.clicked:
                        tile.flagged = not tile.flagged

                    break

            elif gameState == "WIN":
                gameState = "MENU"

    if gameState == "GAME" and not exploding and checkWin(all_cells):
        for tile in all_cells:
            if tile.is_bomb:
                tile.flagged = True
        gameState = "WIN"

    if gameState == "MENU":
        titleText.draw(screen)
        playButton.draw(screen)
        diffButtons[difficulty].draw(screen)
        infoTexts[difficulty].draw(screen)
        creditText.draw(screen)

    if gameState in ("GAME", "WIN"):
        for tile in all_cells:
            tile.draw(screen)

    if gameState == "GAME" and exploding:
        current_time = pygame.time.get_ticks()

        if current_time - last_frame_time >= 60:
            explosion_frame += 1
            last_frame_time += 60

        if explosion_frame < 16:
            explosion_frames[explosion_frame].draw(screen)
        else:
            exploding = False
            gameState = "MENU"

    elif gameState == "WIN":
        screen.blit(winOverlay, (0, 0))
        winText.draw(screen)
        hintText.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()