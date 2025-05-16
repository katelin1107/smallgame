#sprite 精靈/類別
import pygame
import random
import os

FPS = 60
WIDTH = 500
HIEGHT = 600

BLACK =(0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW =(255,255,0)


#遊戲初始化 & 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HIEGHT)) #寬＆高
pygame.display.set_caption("第一個遊戲")
clock = pygame.time.Clock()

#載入圖片，convert是將圖片轉換成pygame容易讀取的格式
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs =[]
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()



#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))

gun_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")) ,
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
shoot_sound.set_volume(0.3)
gun_sound.set_volume(0.3)
shield_sound.set_volume(0.3)
die_sound.set_volume(0.3)
for sound in expl_sounds:
    sound.set_volume(0.3)

pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.1)


font_name =os.path.join("font.ttf") #'arail' 通用字體
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # 2 為幾像素

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0,0)) #blit畫上去
    draw_text(screen,'太空生存戰', 64, WIDTH/2, HIEGHT/4)
    draw_text(screen,'左右鍵移動飛船 空白鍵發射子彈～', 22, WIDTH/2, HIEGHT/2)
    draw_text(screen,'按任意鍵開始遊戲', 18, WIDTH/2, HIEGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS) #在一秒鐘內最多只能執行?次(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP: #判斷鍵盤按了什麼
                waiting = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50,40)) #顯示圖片，pygame平面
        #self.image.fill(GREEN) #綠色平面 這兩行改成下面一行
        self.image = pygame.transform.scale(player_img,(50,38)) #改變大小
        self.image.set_colorkey(BLACK) #把黑色變透明
        self.rect = self.image.get_rect()
        self.radius = 20 #圓形半徑
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HIEGHT - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000 : #隱藏超過一秒就恢復顯示
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HIEGHT - 10    

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += 4
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= 4

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2 :
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HIEGHT+500) #讓飛船顯示在視窗外

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()



class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #self.image = pygame.Surface((30,40)) #顯示圖片，pygame平面
        #self.image.fill(RED)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int( self.rect.width * 0.85 /2 )#圓形半徑
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect = self.image.get_rect() #定位圖片，框起來
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3) #設定旋轉角度

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center =center

    def update(self): 
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HIEGHT or self.rect.left > WIDTH or self.rect.right < 0: #石頭超出視窗範圍就重置
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((10,20)) #顯示圖片，pygame平面
        #self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
                                
        self.rect = self.image.get_rect() #定位圖片，框起來
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10


    def update(self): 
        self.rect.y += self.speedy
        
        if self.rect.bottom < 0:
            self.kill()    

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
                             
        self.rect = self.image.get_rect() #定位圖片
        self.rect.center = center
        self.frame = 0 #記錄圖片更新到第幾張，一開始是第0張
        self.last_update = pygame.time.get_ticks()  #記錄圖片更新時間
        self.frame_rate = 50   #圖片更新時間50毫秒更新一張


    def update(self): 
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate :
            self.last_update = now 
            self.frame += 1
            if self.frame == len(expl_anim[self.size]): #判斷是不是更新到最後一張，如果是就刪除，如果不是就繼續下一張
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center  #對圖片重新定位
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
                                
        self.rect = self.image.get_rect() #定位圖片，框起來
        self.rect.center = center
        self.speedy = 3


    def update(self): 
        self.rect.y += self.speedy
        
        if self.rect.top >HIEGHT :
            self.kill()    

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()  #sprite有個函數可以判斷石頭跟子彈的位置是否相同
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_rock()
score = 0
pygame.mixer.music.play(-1)  # -1 代表會無限重複播放


#遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        draw_init()
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()  #sprite有個函數可以判斷石頭跟子彈的位置是否相同
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0


    clock.tick(FPS) #在一秒鐘內最多只能執行?次(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #判斷鍵盤按了什麼
            if event.key == pygame.K_SPACE: #鍵盤按了空白鍵
                player.shoot()
    #更新遊戲
    #這樣寫可以去執行這個群組裡面每一個物件的update函式
    all_sprites.update()  #全部的物件都做更新
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) #後面兩個布林值判斷物件要不要刪除，True => 刪除
    for hit in hits: #避免子彈打中所有石頭導致最後沒有任何石頭，打中一顆石頭就再創一個新石頭
        random.choice(expl_sounds).play()
        score += hit.radius #子彈打中石頭就加分
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9 : # 0.1掉寶率為9成 0.9掉寶率為10%
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    
    #判斷石頭有沒有撞到飛船，False是石頭不要刪除，從方形改成圓形
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) 
    for hit in hits: #hits是一個列表，判斷有無值
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
            
    #判斷寶物＆飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield' :
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()

        elif hit.type == 'gun' :
            player.gunup()
            gun_sound.play()

    if player.lives == 0 and not(death_expl.alive()):
        show_init = True

    #畫面顯示
    screen.fill(BLACK) #R,G,B 畫面填滿顏色
    screen.blit(background_img, (0,0)) #blit畫上去
    all_sprites.draw(screen) #sprites內的東西全都畫上去
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update() #畫面做更新

pygame.quit()