import pygame, time, math
pygame.init()
win = pygame.display.set_mode((800,600))
pygame.display.set_caption('VAMPIRE GAME : SCORE 10 AND YOU WIN !!')
block_color = (20,97,66)
clock = pygame.time.Clock()
player_img = pygame.image.load("Vampire-Game-main/images/player.png")
enemy_img1 = [pygame.image.load("Vampire-Game-main/images/enemies/bat/0.png"),pygame.image.load("Vampire-Game-main/images/enemies/bat/1.png"),pygame.image.load("Vampire-Game-main/images/enemies/bat/2.png"),pygame.image.load("Vampire-Game-main/images/enemies/bat/3.png")]
enemy_img2 = [pygame.image.load("Vampire-Game-main/images/enemies/blob/0.png"),pygame.image.load("Vampire-Game-main/images/enemies/blob/1.png"),pygame.image.load("Vampire-Game-main/images/enemies/blob/2.png"),pygame.image.load("Vampire-Game-main/images/enemies/blob/3.png")]
gun_img = pygame.image.load("Vampire-Game-main/images/gun.png")
gunshot=pygame.mixer.Sound('Vampire-Game-main/gunshot.wav')
pygame.mixer.music.load("Vampire-Game-main/music.mp3")
pygame.mixer.music.play()

class Player():
    def __init__(self,x,y,width,height,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

    def draw(self):
        win.blit(player_img,(self.x,self.y))
        self.gun()

    def move(self,flag):
        if flag == 1:
            if not((200-self.height<=self.y<=400-2) and (425-self.vel<=self.x<=425+2)):
                if not((480-self.height<=self.y<=530) and (675+25-self.vel<=self.x<=675+2+25)):
                    if not((70-self.height<=self.y<=120) and (500+25-self.vel<=self.x<=500+2+25)):
                        self.x-=self.vel
        elif flag == 0:
            if not((125-25-self.width<=self.x<=500+25) and (120-self.vel<=self.y<=120+2)):
                if not((375-self.width<=self.x<=425) and (375+25-self.vel<=self.y<=375+25+2)):
                    if not((325-25-self.width<=self.x<=675+25) and (530-self.vel<=self.y<=530+2)):
                        self.y-=self.vel
        elif flag == 2:
            if not((200-self.height<=self.y<=400-2) and (375-2<=self.x+self.width<=375+self.vel)):
                if not((480-self.height<=self.y<=530) and (325-25-2<=self.x+self.width<=325-25+self.vel)):
                    if not((70-self.height<=self.y<=120) and (125-25-2<=self.x+self.width<=125-25+self.vel)):
                        self.x+=self.vel
        elif flag == 3:
            if not((125-25-self.width<=self.x<=500+25) and (70-2<=self.y+self.height<=70+self.vel)):
                if not((375-self.width<=self.x<=425) and (225-25-2<=self.y+self.height<=225-25+self.vel)):
                    if not((325-25-self.width<=self.x<=675+25) and (480-2<=self.y+self.height<=480+self.vel)):
                        self.y+=self.vel

    def gun(self):
        global avg_rect
        if mouse_x<=self.x+self.width//2:
            gun_x,gun_y = self.x,self.y+self.height//2
        else:
            gun_x,gun_y = self.x+self.width,self.y+self.height//2
        gun_img_rect = gun_img.get_rect(center = (gun_x,gun_y))
        image_x, image_y = self.x+self.width//2,self.y+self.height//2
        gun_img_x, gun_img_y = gun_img_rect.center
        self.angle = math.degrees(math.atan2((mouse_y-image_y),(mouse_x-image_x)))
        self.angle2 = math.degrees(math.atan2(mouse_y-gun_img_y,mouse_x-gun_img_x))
        rotated_gun = pygame.transform.rotate(gun_img,-self.angle2)
        new_rect = rotated_gun.get_rect(center = gun_img_rect.center)
        win.blit(rotated_gun, new_rect.topleft)
        #pygame.draw.rect(win,(0,0,0),new_rect,2)
        pygame.display.flip()
        avg_rect = new_rect

class Bullet():
    def __init__(self,radius,vel):
        self.radius = radius
        self.vel = vel
        self.angle = -((player.angle/180)*math.pi)
        self.x = player.x+(player.width//2)+(50*math.cos(self.angle))
        self.y = player.y+(player.height//2)-(50*math.sin(self.angle))

    def draw(self):
        pygame.draw.circle(win,(0,0,0),(self.x,self.y),self.radius)
        self.move()

    def move(self):
        self.x+=self.vel*math.cos(self.angle)
        self.y-=self.vel*math.sin(self.angle)

class Enemy():
    def __init__(self,width,height,vel,rand):
        self.rand = rand
        if self.rand:
            self.x,self.y = 200,300
        else:
            self.x,self.y = 200,500
        self.width = width
        self.height = height
        self.vel = vel
        self.i1 = 0
        self.i2 = 0

    def draw(self):
        self.move()
        if self.rand == 1:
            win.blit(enemy_img1[self.i1%4],(self.x,self.y))
            self.i1+=1
            if self.i1>4:
                self.i1 = 0
        else:
            win.blit(enemy_img2[self.i2%4],(self.x,self.y))
            self.i2+=1
            if self.i2>4:
                self.i2 = 0

    def move(self):
        global collide
        if ((self.x+self.width//2<400 and player.x+player.width//2>=400) or (self.x+self.width//2>=400 and player.x+player.width//2<400)):
            if self.x+self.width//2<400:
                if not((200-self.height<=self.y<=400-5) and (375-5<=self.x+self.width<=375+self.vel)):
                    if not((480-self.height-5<=self.y<=530) and (325-25-5<=self.x+self.width<=325-25+self.vel)):
                        if not((70-self.height<=self.y<=120) and (125-25-5<=self.x+self.width<=125-25+self.vel)):
                            self.x+=self.vel
            else:
                if not((200-self.height<=self.y<=400-5) and (375-5<=self.x+self.width<=375+self.vel)):
                    if not((480-self.height-5<=self.y<=530) and (325-25-5<=self.x+self.width<=325-25+self.vel)):
                        if not((70-self.height<=self.y<=120) and (125-25-5<=self.x+self.width<=125-25+self.vel)):
                            self.x-=self.vel
            if ((130<self.y<=300) or (430<=self.y<505) or (10<self.y<=95) or (self.y>590-self.height)):
                self.y-=self.vel
            else:
                self.y+=self.vel

        else:
            if player.x>self.x:
                if not((200-self.height<=self.y<=400-2) and (375-2<=self.x+self.width<=375+self.vel)):
                    if not((480-self.height<=self.y<=530) and (325-25-2<=self.x+self.width<=325-25+self.vel-10)):
                        if not((70-self.height<=self.y<=120) and (125-25-2<=self.x+self.width<=125-25+self.vel-10)):
                            self.x+=self.vel
            if player.x<self.x:
                if not((200-self.height<=self.y<=400-2) and (425-self.vel<=self.x<=425+2)):
                    if not((480-self.height<=self.y<=530) and (675+25-self.vel<=self.x<=675+2+25-10)):
                        if not((70-self.height<=self.y<=120) and (500+25-self.vel<=self.x<=500+2+25-10)):
                            self.x-=self.vel
            if player.y>self.y:
                if not((125-25-self.width<=self.x<=500+25) and (70-2<=self.y+self.height<=70+self.vel)):
                    if not((375-self.width<=self.x<=425) and (225-25-2<=self.y+self.height<=225-25+self.vel)):
                        if not((325-25-self.width<=self.x<=675+25) and (480-2<=self.y+self.height<=480+self.vel)):
                            self.y+=self.vel
            if player.y<self.y:
                if not((125-25-self.width<=self.x<=500+25) and (120-self.vel<=self.y<=120+2)):
                    if not((375-self.width<=self.x<=425) and (375+25-self.vel<=self.y<=375+25+2)):
                        if not((325-25-self.width<=self.x<=675+25) and (530-self.vel<=self.y<=530+2)):
                            self.y-=self.vel

        if player.x-player.width<self.x<player.x+player.width and player.y-player.height<self.y<player.y+player.height:
            collide = True

    def hit(self):
        global score
        score+=1
        if player.x<400:
            if self.rand:
                self.x = 600
                self.y = 400
            else:
                self.x = 600
                self.y = 200
        else:
            if self.rand:
                self.x = 200
                self.y = 300
            else:
                self.x = 200
                self.y = 500
        
def draw_map():
    pygame.draw.rect(win,block_color,(125,70,375,50))
    pygame.draw.circle(win,block_color,(125,95),25)
    pygame.draw.circle(win,block_color,(500,95),25)

    pygame.draw.rect(win,block_color,(375,225,50,150))
    pygame.draw.circle(win,block_color,(400,225),25)
    pygame.draw.circle(win,block_color,(400,375),25)

    pygame.draw.rect(win,block_color,(325,480,350,50))
    pygame.draw.circle(win,block_color,(325,505),25)
    pygame.draw.circle(win,block_color,(675,505),25)

    player.draw()
    enemy1.draw()
    enemy2.draw()
    for i in bullets:
        if (100<i.x<525 and 70<i.y<120) or (375<i.x<425 and 200<i.y<400) or (300<i.x<700 and 480<i.y<530):
            bullets.remove(i)
        if (enemy1.x<i.x<enemy1.x+enemy1.width and enemy1.y<i.y<enemy1.y+enemy1.height):
            bullets.remove(i)
            enemy1.hit()
        elif (enemy2.x<i.x<enemy2.x+enemy2.width and enemy2.y<i.y<enemy2.y+enemy2.height):
            bullets.remove(i)
            enemy2.hit()
        if not(0<=i.x<=800) or not(0<=i.y<=600):
            bullets.remove(i)
        i.draw()
    text = font.render('Score : '+str(score),1,(0,0,0))
    win.blit(text,(685,20))

player = Player(625,270,50,50,13)
enemy1 = Enemy(70,42,6,True)
enemy2 = Enemy(70,42,5,False)
bullets = []
avg_rect = pygame.Rect(0,0,0,0)
shootLoop = 0
score = 0
collide = False
font = pygame.font.SysFont('comicsans', 20, True)

while True:
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 8:
        shootLoop = 0

    mouse_x,mouse_y = pygame.mouse.get_pos()
    clock.tick(30)
    win.fill((175,215,70))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        else:
            continue

    keys = pygame.key.get_pressed()
    clicks = pygame.mouse.get_pressed()
    if keys[pygame.K_w] and player.y > player.vel:
        player.move(0)
    if keys[pygame.K_a] and player.x > player.vel:
        player.move(1)
    if keys[pygame.K_d] and player.x < 800-player.width-5:
        player.move(2)
    if keys[pygame.K_s] and player.y < 600-player.height-5:
        player.move(3)
    if clicks[0] and shootLoop == 0:
        pygame.mixer.Sound.play(gunshot)
        bullets.append(Bullet(7,24))
        shootLoop = 1

    x,y = avg_rect.center
    draw_map()
    pygame.display.update()
    if collide == True:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('Vampire-Game-main/lost.mp3')
        pygame.mixer.music.play()
        time.sleep(1)
        pygame.quit()
    if score == 10:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('Vampire-Game-main/victory.mp3')
        pygame.mixer.music.play()
        time.sleep(2)
        pygame.quit()
