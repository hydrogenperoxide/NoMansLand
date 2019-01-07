#!/usr/bin/python3
#No Man's Land v0.1
import pygame, sys, random

#DIMENSIONS:
#NUMBER OF CELLS
GRID_HEIGHT = 9
GRID_WIDTH = 9
#SIZE OF CELLS
CELL_HEIGHT = 100
CELL_WIDTH = 100
#OTHER
AREA = GRID_WIDTH*GRID_HEIGHT
BRD_THICKNESS = 1 #BORDER THICKNESS

#COLOURS
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (90, 90, 90)
BROWN = (100, 90, 30)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

MINEFACTOR = 7 #The lesser the factor the larger the number of mines and vice versa

pygame.init()

#TEXT
pygame.font.init()
FONT_BIG = pygame.font.SysFont("Comic Sans MS", 80)
FONT_SMALL = pygame.font.SysFont("Comic Sans MS", 40)
death_text = FONT_BIG.render("You Lose", False, RED)
win_text = FONT_BIG.render("You Win!", False, GREEN)
restart_text = FONT_SMALL.render("Press 'r' to restart", False, YELLOW)
death_text_width = death_text.get_width()
death_text_height = death_text.get_height()
restart_text_width = restart_text.get_width()
restart_text_height = restart_text.get_height()

screen = pygame.display.set_mode((CELL_WIDTH*GRID_WIDTH, CELL_HEIGHT*GRID_HEIGHT))

def createCells():
    x, y = 0, 0
    cells = []
    for row in range(1, GRID_HEIGHT+1):
        for column in range(1, GRID_WIDTH+1):
            cell = [x, y, CELL_WIDTH, CELL_HEIGHT]
            cells.append(cell)
            if column == GRID_WIDTH:
                x = 0
                y += CELL_HEIGHT
            else:
                x += CELL_WIDTH
    return cells

def showMines(cells, mines):
    for cell in cells:
        for mine in mines:
            if cell[0] == mine[0] and cell[1] == mine[1]:
                pygame.draw.rect(screen, BLACK, cell)

def generatePlayer():
    player_x, player_y = GRID_WIDTH//2*CELL_WIDTH, GRID_HEIGHT*CELL_HEIGHT
    return player_x, player_y

def generateMines():
    mines = []
    for i in range(AREA//MINEFACTOR):
        mine_x, mine_y = random.randrange(0, CELL_WIDTH*GRID_WIDTH, CELL_WIDTH), random.randrange(100, CELL_HEIGHT*GRID_HEIGHT-CELL_HEIGHT, CELL_HEIGHT)
        mine = [mine_x, mine_y]
        mines.append(mine)
    return mines

def draw(cells, player_x, player_y):

    for cell in cells:
        pygame.draw.rect(screen, BLACK, cell, BRD_THICKNESS)
        if cell[0] == player_x and cell[1] == player_y:
            pygame.draw.rect(screen, GRAY, cell)
            #pygame.draw.rect(screen, BLACK, cell, BRD_THICKNESS) Optional border around player
        else:
            pygame.draw.rect(screen, BROWN, cell)
            pygame.draw.rect(screen, BLACK, cell, BRD_THICKNESS)

def checkPos(player_x, player_y, mines):
    for mine in mines:
        if player_x == mine[0] and player_y == mine[1]:
            return "death"
    if 0 <= player_x <= GRID_WIDTH * CELL_WIDTH - CELL_WIDTH and player_y == 0:
        return "win"
    else:
        return "alive"

def createGame(): #CREATES CELLS, SETS PLAYER AND MINE
    cells = createCells()
    player_x, player_y = generatePlayer()
    mines = generateMines()
    return cells, player_x, player_y, mines

def newGame(): #GENERATES NEW PLAYER COORDINATES AND NEW MINES COORDINATES
    player_x, player_y = generatePlayer()
    mines = generateMines()
    return player_x, player_y, mines

def main():
    print("No Man's Land")
    cells, player_x, player_y, mines = createGame()
    status = "alive"
    while status == "alive":

        draw(cells, player_x, player_y)
        status = checkPos(player_x, player_y, mines)

        while status == "death":
            showMines(cells, mines)
            screen.blit(death_text, (GRID_WIDTH*CELL_WIDTH//2 - death_text_width/2,
                                     GRID_HEIGHT*CELL_HEIGHT//2 - death_text_height/2))
            screen.blit(restart_text, (GRID_WIDTH*CELL_WIDTH//2 - restart_text_width/2,
                                       GRID_HEIGHT*CELL_HEIGHT//2 + death_text_height/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    player_x, player_y, mines = newGame()
                    status = "alive"

        while status == "win":
            showMines(cells, mines)
            screen.blit(win_text, (GRID_WIDTH * CELL_WIDTH // 2 - death_text_width / 2,
                                     GRID_HEIGHT * CELL_HEIGHT // 2 - death_text_height / 2))
            screen.blit(restart_text, (GRID_WIDTH * CELL_WIDTH // 2 - restart_text_width / 2,
                                       GRID_HEIGHT * CELL_HEIGHT // 2 + death_text_height / 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    player_x, player_y, mines = newGame()
                    status = "alive"

        #KEYS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_x += CELL_WIDTH
                if event.key == pygame.K_LEFT:
                    player_x -= CELL_WIDTH
                if event.key == pygame.K_UP:
                    player_y -= CELL_HEIGHT
                if event.key == pygame.K_DOWN:
                    player_y += CELL_HEIGHT

        #BOUNDARIES
        if player_x <= 0:
            player_x = 0
        if player_x >= CELL_WIDTH*GRID_WIDTH-CELL_WIDTH:
            player_x = CELL_WIDTH*GRID_WIDTH-CELL_WIDTH
        if player_y <= 0:
            player_y = 0
        if player_y >= CELL_HEIGHT*GRID_HEIGHT-CELL_HEIGHT:
            player_y = CELL_HEIGHT*GRID_HEIGHT-CELL_HEIGHT

        pygame.display.update()

if __name__ == "__main__":
    main()
