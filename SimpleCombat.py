# Credit to Youtube Channel TechWithTim
# Modified by Iris Nguyen

import pygame #module

pygame.init()

#initialize window screen to draw on:
win = pygame.display.set_mode((500, 480)) #initialize screen - tuple: width, height of the window
pygame.display.set_caption("First game")

#load pictures
walkRight = [pygame.image.load('./images/R1.png'), pygame.image.load('./images/R2.png'), pygame.image.load('./images/R3.png'), pygame.image.load('./images/R4.png'), pygame.image.load('./images/R5.png'), pygame.image.load('./images/R6.png'),pygame.image.load('./images/R7.png'), pygame.image.load('./images/R8.png'), pygame.image.load('./images/R9.png')
]
#could just flip walkRight
walkLeft = [pygame.image.load('./images/L1.png'), pygame.image.load('./images/L2.png'), pygame.image.load('./images/L3.png'), pygame.image.load('./images/L4.png'), pygame.image.load('./images/L5.png'), pygame.image.load('./images/L6.png'),pygame.image.load('./images/L7.png'), pygame.image.load('./images/L8.png'), pygame.image.load('./images/L9.png')
]
bg = pygame.image.load('./images/bg.jpg')
idle = pygame.image.load('./images/standing.png')

bulletSound = pygame.mixer.Sound('./sound/bullet.wav')
hitSound = pygame.mixer.Sound('./sound/hit.wav')
music = pygame.mixer.music.load('./sound/music.mp3')
pygame.mixer.music.play(-1)

class player(object):#character's properties: pygame's coordinate is in the top left of character, instead of in the middle
    def __init__(self, x, y, width, height):
        self.x = x #2D space xy-axis
        self.y = y
        self.width = width
        self.height =height
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0
        self.left = False
        self.right = False
        self.standing = False #track if char is standing
        self.hitbox = (self.x + 17, self.y +11, 29, 52) # things in a tuple = rectangle = x, y, width, height

    def draw(self, win): #call player.draw()
        if self.walkCount + 1 >= 27: #avoid index error, 3 frames per sprite, frame rate = 27/per sec
            self.walkCount = 0
        if not(self.standing): #if not standing->walking pics
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) #floor division excludes remainder
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else: #keep track of the direction where he walks, change the facing direction to first frame accoridngly
            #win.blit(idle, (self.x, self.y))
            #self.walkCount = 0
            if self.right:
                win.blit(walkRight[0], (self.x, self.y)) #first image
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        #moving hitbox with walking character.
        self.hitbox = (self.x + 17, self.y +11, 29, 52)
        '''pygame.draw.rect(win, (255,0,0), self.hitbox,2)'''

    def collide(self): #collide with goblin
        self.isJump = False #so man does not go below the screen if jump on top of goblin
        self.jumpCount = 10
        self.x = 60#move back to left side of the screen
        self.y = 410
        self.walkCount = 0 #set to standing position, not mid-strike
        font2 = pygame.font.SysFont('comicsans', 100)
        text = font2.render('-1', 1, (255, 0,0))
        win.blit(text, (250 - (text.get_width()/2), 200)) # center of text in the center of screen. Get_width() = built in for text
        pygame.display.update()
        i = 0 #pause to see otherwise flash too quickly
        while i < 300: #1000 = 1 sec
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

#Change facing direction, Velocity for multiple bullets
class projectile(object):
    def __init__(self, x, y, radius, color, facing): #similar charactersitics as character + bullets' specifics
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing #facing = 1 or -1 = left or right
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius) #ourline of circle no fill in ,1

class enemy(object):
    walkRight = [pygame.image.load('./images/R1E.png'), pygame.image.load('./images/R2E.png'), pygame.image.load('./images/R3E.png'), pygame.image.load('./images/R4E.png'), pygame.image.load('./images/R5E.png'), pygame.image.load('./images/R6E.png'), pygame.image.load('./images/R7E.png'), pygame.image.load('./images/R8E.png'), pygame.image.load('./images/R9E.png'), pygame.image.load('./images/R10E.png'), pygame.image.load('./images/R11E.png')]
    walkLeft = [pygame.image.load('./images/L1E.png'), pygame.image.load('./images/L2E.png'), pygame.image.load('./images/L3E.png'), pygame.image.load('./images/L4E.png'), pygame.image.load('./images/L5E.png'), pygame.image.load('./images/L6E.png'), pygame.image.load('./images/L7E.png'), pygame.image.load('./images/L8E.png'), pygame.image.load('./images/L9E.png'), pygame.image.load('./images/L10E.png'), pygame.image.load('./images/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end] #list
        self.walkCount = 0
        self.velocity = 3
        self.hitbox = (self.x +15, self.y +2, 31, 57)
        self.health = 10
        self.visible = True #once health=0, enemy disappears
    def draw(self, win):
        self.move() #first move then draw
        if self.visible == True: #only draws when health !=0
            if self.walkCount + 1 >= 33: #Why 33? It's always smaller than 33
                self.walkCount = 0
            if self.velocity > 0: #moving right
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount +=1
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1]-20, 50, 10))#Red health background, move hitbox's y coordinate up to not draw over character
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1]-20, 50-(5 * (10-self.health)), 10))
             #Green health, move left slowly as hit proportionately. Die with 11 hit, if want 10 => health =9, 4.75*...
            '''pygame.draw.rect(win, (255,0,0), self.hitbox,2)'''

    def move(self):
        if self.velocity > 0: #go right
            if self.x + self.velocity < self.path[1]: #add to the velocity of x coordinate < path limit self.end
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.walkCount = 0
        else: #velocity is negative now, go left
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity #add negative velocity
            else:
                self.velocity *= -1 #change velocity to positive, go right again.
                self.walkCount = 0
        self.hitbox = (self.x +17, self.y +2, 31, 57)


    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        hitSound.play()

clock = pygame.time.Clock() #allow to change SPF


def reDrawWindow():
    #global walkCount #refer to the same global var
    #fill background before drawing the rect to see it changes:
    win.blit(bg, (0,0))#win.fill((140, 100, 227))
    #circle(surface drawn on, (RGB color), (dimension)),....
    #pygame.draw.rect(win, (255, 224, 48), (x, y, width, height))
    text = font.render("Score: " + str(score), 1, (0, 0, 0)) #rendering new text render("text", 1, (color))
    win.blit(text, (380, 10)) #draw score onto screen
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()



#Main Loop:
run = True
man = player(50, 400, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
bullets = [] #
shootLoop = 0
score = 0
font = pygame.font.SysFont('comicsans', 30, True) #size, bold

while run:
    clock.tick(27)#pygame.time.delay(50) #frame rate
    #event = user activity
    if goblin.visible == True: #only allow collision if goblin is visible/alive
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]: #check left and right side of box
                man.collide()
                score -= 1

    if shootLoop >0:
        shootLoop +=1
    if shootLoop > 3:
        shootLoop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        #check if bullet is in the y-coordinate:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]: # - bullet.radius --> check if top of bullet is above goblin's bottom of rec. AND + bullet.radius --> check if bullet's bottom is under goblin's top of rec
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x-bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: #+ bullet.radius --> check if bullet's right passes goblin's rec top left x AND - bullet --> check if bullet's left passes goblin's rec top right x
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet)) #remvove bullet from list
        if bullet.x < 500 and bullet.x > 0:#bullet's property of x not go off screen
            bullet.x += bullet.velocity
        else: #offscreen
            bullets.pop(bullets.index(bullet)) #find index of offscreen bullet from the list and pop

    #Move the rectangle: 1)for() like above, but not account for holding down key so 2)

    keys = pygame.key.get_pressed() #getting a representation of the state of the keyboard at the time of get_pressed() being called.
    if keys[pygame.K_SPACE] and shootLoop==0:#not elif cuz shoot while walking is OK and limit bullet being shoot, give abreak between bullets
        bulletSound.play()
        if man.left:
            facing = -1 #shoot left on x axis->move backwards 500 to 0
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0,0,0), facing)) #bullet coming from the middle of the man
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.velocity: #0:0 is top left of the screen, 500: 500bottom right
        man.x -= man.velocity #move left = subtracting from x-coordinate
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.velocity: #bc cooridnate is on the left
        man.x += man.velocity
        man.right = True
        man.left = False
        man.standing = False
    else:
        # man.right = False #not reset these bc won't know which direction he's facing
        # man.left = False
        man.walkCount = 0
        man.standing = True

    if not(man.isJump):
        # if keys[pygame.K_UP] and y > 0: # y > velocity
        #     y -= velocity
        # if keys[pygame.K_DOWN] and y < 500 - height-velocity:
        #     y += velocity
        if keys[pygame.K_UP]: #cannot move up/down when jump, cannot jump in midair
            man.isJump = True #jump = acceleration to the top + hang time + descending increasingly faster
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10: #negative variable to follow quadratic formula
            neg = 1
            if man.jumpCount <0: #descend
                neg = -1
            man.y -= (man.jumpCount ** 2) *0.5 *neg #ascend: decrement jumpCount; descend: - neg -1 = +1
            man.jumpCount -=1 # 10 to -10
        else:
            man.isJump = False #not jumping
            man.jumpCount = 10 #return to the OG height

    reDrawWindow()


pygame.quit()
