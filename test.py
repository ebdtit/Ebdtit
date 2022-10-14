import pygame

size = 800, 640
window = pygame.display.set_mode(size)
pygame.display.set_caption("Tanks Dendy")

go = False

imgMenu = pygame.image.load('images/start.png')


    #global menu, menu2, menupos, menupos2, done
while go == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            go = True



    window.blit(imgMenu, (0, 0))
    pygame.display.flip()

