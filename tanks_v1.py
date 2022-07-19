import pygame
from random import randint
import time



pygame.init()
WIDTH, HEiGHT = 800,600
window = pygame.display.set_mode((WIDTH, HEiGHT))
pygame.display.set_caption("Tanks Dendy")
clock = pygame.time.Clock()
TITLE = 32
FPS = 60
fontUI = pygame.font.Font(None, 30)
i =1
MAXEnemy = 10

imgBrick = pygame.image.load('images/block_brick.png')
imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png')
    ]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png')
]

imgEnemy = [
    pygame.image.load('images/vrag1.png'),
    pygame.image.load('images/vrag2.png'),
    pygame.image.load('images/vrag3.png'),
]
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


#tankUP = pygame.image.load('ggu.png').convert()
#tankDown = pygame.transform.rotate(tank, 180)
#tankRight = pygame.transform.rotate(tank, 270)
#tankLeft = pygame.transform.rotate(tank, 90)

class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank' :
                #pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))
                myimage = imgTanks[obj.rank]
                myimage = pygame.transform.scale(myimage, (TITLE - 10, TITLE - 10))
                imgrect = center=(5 + i * 70, 5)
                text = fontUI.render(str(obj.hp), 1, 'green')
                rect = text.get_rect(center = (5 + i * 70 + 32, 5 + 11))
                window.blit(myimage, imgrect)
                window.blit(text, rect)
                i += 1
            if obj.type == 'enemy':
                myimage = imgEnemy[obj.rank]
                myimage = pygame.transform.scale(myimage, (TITLE - 10, TITLE - 10))
                imgrect = center = (5 + i * 70, 5)
                text = fontUI.render(str(obj.hp), 1, 'red')
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(myimage, imgrect)
                window.blit(text, rect)
                i += 1





class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TITLE, TITLE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5
        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLeft = keyList[0]
        self.keyRight = keyList[1]
        self.keyUp = keyList[2]
        self.keyDown = keyList[3]
        self.keyShot = keyList[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() -5))
        self.rect = self.image.get_rect(center=self.rect.center)

        oldX, oldY = self.rect.topleft
        if keys[self.keyLeft]:
            if self.rect.x >= 0:
                self.rect.x -= self.moveSpeed
                self.direct = 3
        elif keys[self.keyRight]:
            if self.rect.x <= WIDTH - TITLE:
                self.direct = 1
                self.rect.x += self.moveSpeed
        elif keys[self.keyUp]:
            if self.rect.y >= 0 + TITLE:
                self.direct = 0
                self.rect.y -= self.moveSpeed
        elif keys[self.keyDown]:
            if self.rect.y <= HEiGHT - TITLE:
                self.direct = 2
                self.rect.y += self.moveSpeed

        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keyShot] and self.shotTimer == 0 :
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):

       # pygame.draw.rect(window, self.color, self.rect)

        #x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        #y = self.rect.centery + DIRECTS[self.direct][1] * 30
        #pygame.draw.line(window, 'white', self.rect.center, (x, y), 4)
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color + " убит")

class Enemy:
    def __init__(self, px, py, rank):
        objects.append(self)
        self.type = 'enemy'
        self.rect = pygame.Rect(px, py, TITLE, TITLE)
        self.direct = randint(0, 3)
        self.moveSpeed = 1
        self.rank = rank
        #self.hp = 2
        self.shotTimer = 3
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = (self.rank + 1) * 2
        self.hp = self.rank + 2

        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)





    def update(self):
        self.image = pygame.transform.rotate(imgEnemy[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + 10, self.image.get_height() + 10))
        self.rect = self.image.get_rect(center=self.rect.center)
        oldX, oldY = self.rect.topleft

        if self.rank == 1:
            self.moveSpeed = 2
            self.shotDelay = 70
        if self.rank == 2:
            self.moveSpeed = 1
            self.shotDelay = 80


        if self.direct == 1:
            self.rect.x += self.moveSpeed
        if self.direct == 2:
            self.rect.y += self.moveSpeed
        if self.direct == 3:
            self.rect.x -= self.moveSpeed
        if self.direct == 0:
            self.rect.y -= self.moveSpeed

        if  self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1


        for obj in objects:
            if obj != self and obj.type == 'block'  and self.rect.colliderect(obj.rect) or self.rect.x < 0  or self.rect.y < 0 + TITLE or self.rect.x > WIDTH -TITLE or self.rect.y > HEiGHT - TITLE:
                self.rect.topleft = oldX, oldY
                self.direct = randint(0, 3)

        for obj in objects:
            if obj != self and  obj.type == 'tank'  and self.rect.colliderect(obj.rect) :
                self.rect.topleft = oldX, oldY
                self.direct = randint(0, 3)

        for obj in objects:
            if obj != self and  obj.type == 'enemy'  and self.rect.colliderect(obj.rect) :
                self.rect.topleft = oldX, oldY
                self.direct = randint(0, 3)


    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.direct = randint(0, 3)
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)



class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        #self.rect = pygame.Rect(px, py, 4, 4)


    def update(self):
        self.px += self.dx
        self.py += self.dy


        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEiGHT :
            bullets.remove(self)
        else:
            for obj in objects:

                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    if obj.type != self.parent.type:
                        obj.damage(self.damage)

                        bullets.remove(self)
                        Bang(self.px, self.py)
                        break
                    else:
                        bullets.remove(self)
                        Bang(self.px, self.py)



    def draw(self):

        pygame.draw.circle(window, 'yellow', (self.px, self.py), 4)

class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px = px
        self.py = py
        self.frame = 0


    def update(self):
        self.frame += 0.2
        if self.frame >= 3 : objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center = (self.px, self.py))
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)
        #pygame.draw.rect(window, 'green', self.rect)
        #pygame.draw.rect(window, 'gray20', self.rect, 2)

    def damage(self, value):
        self.hp -= value
        if self.hp  <= 0 :
            objects.remove(self)


bullets = []
objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP0))
ui = UI()



for _ in  range(5):
    while True:
        x = randint(0, WIDTH // TITLE - 1) * TITLE
        y = TITLE
        rect = pygame.Rect(x, y, TITLE, TITLE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True

        if not fined:
            break
    Enemy(x, y, (randint(0, 2)))










for _ in  range(100):
    while True:
        x = randint(0, WIDTH // TITLE -1) * TITLE
        y = randint(2, HEiGHT // TITLE -1) * TITLE
        rect = pygame.Rect(x, y, TITLE, TITLE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect): fined = True
        if not fined : break

    Block(x, y, TITLE)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for bullet in bullets:
        bullet.update()

    for obj in objects:
        obj.update()

    ui.update()
    window.fill('black')

    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()



    pygame.display.update()
    clock.tick(FPS)

pygame.quit()