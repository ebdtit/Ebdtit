import time
import pygame
clock = pygame.time.Clock()


tic = time.perf_counter()
play = True
frame =0
while play:
    frame += 1

    if frame > 600:
        sum = tic - time.perf_counter()
        print('tic = ' + str(int(tic)) + '\n'  + 'real_tic = ' + str(time.perf_counter()) + '\n' + 'разница = ' + str(sum))
        play = False
    clock.tick(60)

