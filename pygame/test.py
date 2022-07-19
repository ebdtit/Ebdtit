import time
from threading import Thread
import pygame


class XThread(Thread):
    flag = True
    def __init__(self, function):
        super().__init__()
        self.function = function
    def stop(self):
        self.flag = False
    def run(self):
        while self.flag:
            self.function()

runGame = True

fpsClock = pygame.time.Clock()

pygame.init()
FPS = 30

gameScreen = pygame.display.set_mode((800, 800))
BLACK = (0, 0, 0)
YELLOW = (255, 255, 150)
RED = (255, 0, 0)
w, h = 8, 8


field = [[0 for x in range(w)] for y in range(h)]

for y in range(0, 8):
    for x in range(0, 8):
        if (x + y) % 2 == 0:
            field[y][x] = 1

print(field)

def drawBoard():
    size = [800, 800]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("TBS")
    gameScreen.fill((YELLOW))

    for y in range(0, 8):
        for x in range(0, 8):
            if field[y][x] == 1:
                pygame.draw.rect(gameScreen, BLACK,
                    (x * 100, y * 100, 100, 100))

    pygame.display.flip()

def drawFlashingSquare():
    while 1:
        pygame.draw.line(gameScreen, RED,
            [x // 100 * 100, y // 100 * 100], [x // 100 * 100 + 100, y // 100 * 100], 5)
        pygame.draw.line(gameScreen, RED,
            [x // 100 * 100, y // 100 * 100], [x // 100 * 100, y // 100 * 100 + 100], 5)
        pygame.draw.line(gameScreen, RED,
            [x // 100 * 100, y // 100 * 100 + 100], [x // 100 * 100 + 100, y // 100 * 100 + 100],
                             5)
        pygame.draw.line(gameScreen, RED,
            [x // 100 * 100 + 100, y // 100 * 100], [x // 100 * 100 + 100, y // 100 * 100 + 100],
                             5)
        pygame.display.flip()
        pygame.time.wait(300)
        pygame.draw.line(gameScreen, YELLOW,
            [x // 100 * 100, y // 100 * 100], [x // 100 * 100 + 100, y // 100 * 100], 5)
        pygame.draw.line(gameScreen, YELLOW,
            [x // 100 * 100, y // 100 * 100], [x // 100 * 100, y // 100 * 100 + 100], 5)
        pygame.draw.line(gameScreen, YELLOW,
            [x // 100 * 100, y // 100 * 100 + 100], [x // 100 * 100 + 100, y // 100 * 100 + 100],
                             5)
        pygame.draw.line(gameScreen, YELLOW,
            [x // 100 * 100 + 100, y // 100 * 100], [x // 100 * 100 + 100, y // 100 * 100 + 100],
                             5)
        pygame.display.flip()

drawBoard()

xthread = None

while runGame:
    fpsClock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
            if xthread is None:
                pass
            else:
                xthread.stop()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawBoard()
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if xthread == None:
                    xthread = XThread(drawFlashingSquare)
                    xthread.start()
                elif xthread.isAlive() == True:
                    xthread.stop()
            if event.button == 3:
                pass
pygame.quit()