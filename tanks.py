import levels
import base
import pygame
from random import randint
import time

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

pygame.init()
WIDTH, HEiGHT = 800, 640
size = 800, 640
window = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Tanks Dendy")
clock = pygame.time.Clock()
TITLE = 32
FPS = 60
fontUI = pygame.font.Font(None, 30)
i = 1
startEnemy = 3
MAXEnemy = 8
enemy = 0
level = 0
lev = levels.lev[level]
helmet = 0
base = base.block[helmet]
firewall = base
matrix = lev



soundStart = pygame.mixer.Sound('music/battle-city_-tanchiki_-dend.mp3')
soundBlock = pygame.mixer.Sound('music/battle-city-sfx-3.mp3')
soundShoot = pygame.mixer.Sound('music/battle-city-sfx-6.mp3')
soundBang = pygame.mixer.Sound('music/battle-city-sfx-7.mp3')
soundDrive = pygame.mixer.Sound('music/battle-city-sfx-16.mp3')


imgBonus = [
    pygame.image.load('images/bonus_bomb.png'),
    pygame.image.load('images/bonus_helmet.png'),
    pygame.image.load('images/bonus_shovel.png'),
    pygame.image.load('images/bonus_star.png'),
    pygame.image.load('images/bonus_tank.png'),
    pygame.image.load('images/bonus_time.png'),
    ]

imgBlock =[
    pygame.image.load('images/block_none.png'),
    pygame.image.load('images/block_armor.png'),
    pygame.image.load('images/block_brick.png'),
    pygame.image.load('images/block_bushes.png'),
    pygame.image.load('images/block_water.png'),
    pygame.image.load('images/block_ice.png'),
    pygame.image.load('images/base.png'),
    ]



imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),
    pygame.image.load('images/ggu.png'),
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
                imgrect = center = (5 + i * 70, 5)
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
    def __init__(self, color, px, py, direct, keyList, rank):
        objects.append(self)
        self.type = 'tank'
        self.px = px
        self.py = py
        self.color = color
        self.rect = pygame.Rect(px, py, TITLE, TITLE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 10
        self.shotTimer = 3
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 3
        self.kills = 0
        self.keyLeft = keyList[0]
        self.keyRight = keyList[1]
        self.keyUp = keyList[2]
        self.keyDown = keyList[3]
        self.keyShot = keyList[4]
        self.frame = 0
        self.rank = rank
        self.oldRank = 1
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() -5))
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rank == 8:
            self.frame +=1
            if self.frame == 300:
                self.rank = self.oldRank
                self.frame = 0



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
            if  obj != self and obj.type == 'block' and obj.vid != 3 and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
            if  obj != self and obj.type == 'enemy' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
            if  obj != self and obj.type == 'bonus' and self.rect.colliderect(obj.rect):
                objects.remove(obj)
                if obj.type == 'bonus' and obj.bonus == 0:
                    for obj in objects:
                        if obj.type == 'enemy':
                            soundBang.play(0)
                            Bang(obj.px, obj.py)
                            objects.remove(obj)

                if obj.type == 'bonus' and obj.bonus == 2:
                    pole(firewall)

                if obj.type == 'bonus' and obj.bonus == 1:
                    self.oldRank = self.rank
                    start_ticks = pygame.time.get_ticks()
                    self.rank = 8

                if obj.type == 'bonus' and obj.bonus == 3:
                    if self.rank <= 7:
                        self.rank += 1

                if obj.type == 'bonus' and obj.bonus == 4:
                    if self.hp <= 10:
                        self.hp += 1

                if obj.type == 'bonus' and obj.bonus == 5:
                    for obj in objects:
                        if obj.type == 'enemy':
                            obj.direct = 5



        if keys[self.keyShot] and self.shotTimer == 0 :
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay
            soundShoot.play(0)

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):

        # pygame.draw.rect(window, self.color, self.rect)
        #
        # x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        # y = self.rect.centery + DIRECTS[self.direct][1] * 30
        # pygame.draw.line(window, 'white', self.rect.center, (x, y), 4)
        window.blit(self.image, self.rect)

    def damage(self, value, killer):
        if self.rank != 8:
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)
                print(self.color + " убит")

class Enemy:
    def __init__(self, px, py, rank):
        objects.append(self)
        self.type = 'enemy'
        self.rect = pygame.Rect(px, py, TITLE, TITLE)
        self.px = px
        self.py = py
        self.direct = randint(0, 3)
        self.moveSpeed = 1
        self.rank = rank
        #self.hp = 2
        self.shotTimer = 3
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = (self.rank + 1) * 2
        self.hp = self.rank + 2
        self.frame = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    #def init(self):
        #Enemy(TITLE, TITLE, (randint(0, 2)))


    def update(self):
        self.image = pygame.transform.rotate(imgEnemy[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + 10, self.image.get_height() + 10))
        self.rect = self.image.get_rect(center=self.rect.center)
        oldX, oldY = self.rect.topleft

        if self.direct == 5:
            self.frame += 1
            if self.frame >= 300:
                self.direct = randint(0, 3)
                self.frame = 0


        if self.rank == 1:
            self.moveSpeed = 2
            self.shotDelay = 50
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
            if self.direct != 5:

                dx = DIRECTS[self.direct][0] * self.bulletSpeed
                dy = DIRECTS[self.direct][1] * self.bulletSpeed
                Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
                self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1


        for obj in objects:
            if obj != self and obj.type == 'block' and obj.vid != 3 and self.rect.colliderect(obj.rect) or self.rect.x < 0  or self.rect.y < 0 + TITLE or self.rect.x > WIDTH -TITLE or self.rect.y > HEiGHT - TITLE:
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

    def damage(self, value, killer):
        self.hp -= value
        if self.hp <= 0:

            objects.remove(self)
            soundBang.play(0)
            for obj in objects:
                if obj != self and obj == killer:
                    obj.kills += 1
                    print(obj.color + " Количество убийств: " + str(obj.kills))
                    # if obj.kills > 3:
                    #     obj.rank += 1



class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        self.rect = pygame.Rect(px, py, 4, 4)

    def update(self):
        self.px += self.dx
        self.py += self.dy


        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEiGHT :
            bullets.remove(self)
        else:
            for obj in objects:


                if obj != self.parent and obj.type != 'block' and obj.type != 'bang' and obj.type != 'bonus' and obj.rect.collidepoint(self.px, self.py):
                    if obj.type != self.parent.type:
                        obj.damage(self.damage, self.parent)

                        bullets.remove(self)
                        Bang(self.px, self.py)
                        break
                elif obj.type == "block" and obj.vid != 3 and obj.vid != 4 and obj.type != 'bang' and obj.type != 'bonus' and obj.rect.collidepoint(self.px, self.py):
                    soundBlock.play(0)
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py)
                    break
                # else:s
                #     obj.damage(self.damage)
                #     bullets.remove(self)
                #     Bang(self.px, self.py)



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
        if self.frame >= 3 :
            objects.remove(self)


    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center = (self.px, self.py))
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size, vid):
        objects.append(self)
        self.type = 'block'
        self.vid = vid
        self.image = imgBlock[self.vid]
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1
        if self.vid == 1:
            self.hp = 5

    def update(self):
        pass

    def draw(self):


        window.blit(self.image, self.rect)
        #pygame.draw.rect(window, 'green', self.rect)
        #pygame.draw.rect(window, 'gray20', self.rect, 2)

    def damage(self, value):
        self.hp -= value
        if self.hp  <= 0 :
            objects.remove(self)


class Bonus:
    def __init__(self, bonus):
        objects.append(self)
        self.type = 'bonus'
        self.bonus = bonus
        self.image = imgBonus[self.bonus]
        self.rect = pygame.Rect((randint(0, WIDTH - TITLE)), (randint(0, HEiGHT - TITLE)), TITLE, TITLE)
        self.frame = 0

    def update(self):

        self.frame += 1
        while self.frame <= 50:
            self.image = imgBonus[randint(0, 5)]
            break
        self.image = imgBonus[self.bonus]

        if self.frame > 500:
            objects.remove(self)



    def draw(self):
        window.blit(self.image, self.rect)


def init(num):
    global enemy
    enemy += num
    # if MAXEnemy - enemy <= startEnemy and MAXEnemy - enemy > 0:
    #     num = MAXEnemy - enemy

    print(enemy)
    for _ in range(num):

        while True:
            x = randint(0, WIDTH // TITLE - 1) * TITLE
            y = TITLE
            rect = pygame.Rect(x, y, TITLE, TITLE)
            fined = False
            for obj in objects:
                if obj.type != "bang" and rect.colliderect(obj.rect):
                    fined = True

            if not fined:
                break

        Enemy(x, y, (randint(0, 2)))



def pole(a):
    x = 0
    y = 0
    i = 0
    while i < 500:
        if a[y][x] == 0:
            pass

            #window.blit(imgNone, (x * TITLE, y * TITLE))
        elif a[y][x] == 1:
            Block(x * TITLE, y * TITLE, TITLE, 1)
            #window.blit(imgBeton, (x * TITLE, y * TITLE))
        elif a[y][x] == 2:
            Block(x * TITLE, y * TITLE, TITLE, 2)
            #window.blit(imgBrick, (x * TITLE, y * TITLE))
        elif a[y][x] == 3:
            Block(x * TITLE, y * TITLE, TITLE, 3)
            #window.blit(imgForest, (x * TITLE, y * TITLE))
        elif a[y][x] == 4:
            Block(x * TITLE, y * TITLE, TITLE, 4)
            #window.blit(imgWater, (x * TITLE, y * TITLE))
        elif a[y][x] == 5:
            Block(x * TITLE, y * TITLE, TITLE, 5)
            #window.blit(imgBase, (x * TITLE, y * TITLE))
        elif a[y][x] == 6:
            Block(x * TITLE, y * TITLE, TITLE, 6)
            #window.blit(imgBase, (x * TITLE, y * TITLE))
        x += 1
        if x > 24:
            x = 0
            y += 1
        i += 1



bullets = []
objects = []
Tank('blue', 10 * TITLE, 19 * TITLE, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), 8)
Tank('red', 14 * TITLE, 19 * TITLE, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP0), 8)
ui = UI()

#window.fill('black')

init(startEnemy)
pole(matrix)
soundStart.play(0)


# for _ in  range(100):
#     while True:
#         x = randint(0, WIDTH // TITLE -1) * TITLE
#         y = randint(2, HEiGHT // TITLE -1) * TITLE
#         rect = pygame.Rect(x, y, TITLE, TITLE)
#         fined = False
#         for obj in objects:
#             if rect.colliderect(obj.rect): fined = True
#         if not fined : break
#
#     Block(x, y, TITLE)ws
frame = 0
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


    countEnemu = len([obj for obj in objects if obj.type == 'enemy'])
    if countEnemu < startEnemy and MAXEnemy - enemy >= startEnemy:
        frame += 1
        if frame > 200:
            frame = 0
            init(startEnemy)
    else:
        if countEnemu < startEnemy and MAXEnemy - enemy < startEnemy and MAXEnemy - enemy > 0:
            #print(MAXEnemy - enemy)
            frame += 1
            if frame > 200:
                frame = 0
                init(MAXEnemy - enemy)



    countbonus = len([obj for obj in objects if obj.type == 'bonus']) # считаем количество бонусов
    frame += 1
    if countbonus < 3 and frame > 200:
        frame = 0
        Bonus(randint(0, 5))


    ui.update()
    window.fill('black')

    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()