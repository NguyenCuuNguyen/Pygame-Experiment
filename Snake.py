import pygame #module
pygame.init()

#initialize window screen to draw on:
win = pygame.display.set_mode((500, 480)) #tuple: width, height of the window
pygame.display.set_caption("First game")

#load pictures
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')
]
#could just flip walkRight
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')
]
bg = pygame.image.load('bg.jpg')
idle = pygame.image.load('standing.png')


#character's properties: pygame's coordinate is in the top left of character, instead of in the middle
x = 50 #2D space xy-axis
y = 400
width = 64
height = 64
velocity = 5

clock = pygame.time.Clock() #allow to change SPF

isJump = False
jumpCount = 10
walkCount = 0

left = False
right = False

def reDrawWindow():
    global walkCount #refer to the same global var

    #fill background before drawing the rect to see it changes:
    win.blit(bg, (0,0))#win.fill((140, 100, 227))
    #circle(surface drawn on, (RGB color), (dimension)),....
    #pygame.draw.rect(win, (255, 224, 48), (x, y, width, height))
    if walkCount + 1 >= 27: #avoid index error, 3 frames per sprite, frame rate = 27/per sec
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//3], (x,y)) #exclude remainder
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(idle, (x,y))
        walkCount = 0

    pygame.display.update()


#Main Loop:
run = True
while run:
    clock.tick(27)#pygame.time.delay(50) #frame rate
    #event = user activity
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Move the rectangle: 1)for() like above, but not account for holding down key so 2)

    keys = pygame.key.get_pressed() #getting a representation of the state of the keyboard at the time of get_pressed() being called.
    if keys[pygame.K_LEFT] and x > velocity: #0:0 is top left of the screen, 500: 500bottom right
        x -= velocity #move left = subtracting from x-coordinate
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 500 - width -velocity: #bc cooridnate is on the left
        x += velocity
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not(isJump):
        # if keys[pygame.K_UP] and y > 0: # y > velocity
        #     y -= velocity
        # if keys[pygame.K_DOWN] and y < 500 - height-velocity:
        #     y += velocity
        if keys[pygame.K_SPACE]: #cannot move up/down when jump, cannot jump in midair
            isJump = True #jump = acceleration to the top + hang time + descending increasingly faster
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10: #negative variable to follow quadratic formula
            neg = 1
            if jumpCount <0: #descend
                neg = -1
            y -= (jumpCount ** 2) *0.5 *neg #ascend: decrement jumpCount; descend: - neg -1 = +1
            jumpCount -=1 # 10 to -10
        else:
            isJump = False #not jumping
            jumpCount = 10 #return to the OG height

    reDrawWindow()


pygame.quit()
