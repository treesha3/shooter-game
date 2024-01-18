from pygame import *
from random import*
from time import time as timer
mixer.init()
font.init()
window = display.set_mode((700,500))

display.set_caption('Стреляем туда сюда')

windows = transform.scale(image.load('galaxy.jpg'),(700,500))
bull = transform.scale(image.load('rocket.png'),(80,150))
monsterrr = transform.scale(image.load('ufo.png'),(100,120))
pulya = transform.scale(image.load('bullet.png'),(5,10))

mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')

lost = 0
score = 0
font1 = font.SysFont(None, 36)
font2 = font.SysFont(None, 80)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
clock = time.Clock()
hp = 3
FPS = 30

rel_time = False


num_fire = 0



life_color = (0,255,0)

if hp == 2:
    life_color = (150,150,0)

if hp == 1:
    life_color = (255,0,0)











class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player (GameSprite):
    def update(self):
        key_pressed = key.get_pressed()

        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if key_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top,15,20,-15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 520:
            lost = lost + 1
            self.rect.y = 0
            self.rect.x = randint(100,600)



class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80,620),-20,80,50, randint(1,7))
    asteroids.add(asteroid)

for i in range(6):
    monster = Enemy('ufo.png', randint(80,620),-20,80,50, randint(1,4))
    monsters.add(monster)

player = Player('rocket.png', 350,420,80,100, 7)
finish = False
run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
    
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True 
    if not finish:
        window.blit(windows,(0,0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose,(20,20))

        text_win = font1.render('Счет:' + str(score), 1, (255,255,255))
        window.blit(text_win,(20,55))

        healt = font2.render('ХП:' + str(hp), 1, life_color)
        window.blit(healt,(550,10))

        collides = sprite.groupcollide(monsters,bullets, True, True)

        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80,620),-20,80,50, randint(1,4))
            monsters.add(monster)




        if lost == 3 or sprite.spritecollide(player,monsters,False) or hp == 0:
            finish = True
            lose_text = font2.render('ТЫ ПРОИГРАЛ', True, (255,0,0))
            window.blit(lose_text, (170,200))

        if score == 11:
            finish = True
            win_text = font2.render('ТЫ ВЫЙГРАЛ', True, (255,0,0))
            window.blit(win_text, (170,200))


        if sprite.spritecollide(player, asteroids,True):
            hp -= 1
            
        
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font1.render('Wait, reload...', 1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0 
                rel_time = False





        bullets.update()
        bullets.draw(window)

        player.update()
        player.reset()

        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        display.update()
        clock.tick(FPS)
    


    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)

        for i in range(6):
            monster = Enemy('ufo.png', randint(80,620),-20,80,50, randint(1,4))
            monsters.add(monster)

    