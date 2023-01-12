import pygame, sys, math, random
from pygame.locals import QUIT

pygame.init()
running = True
image_scale = 0.5
scale= image_scale*4
dimensions = [1300*0.25,1890*0.25]
screenHeight = dimensions[1]*scale
screenWidth = dimensions[0]*scale
positions = [screenWidth*0.25, screenWidth*0.42, screenWidth*0.58, screenWidth*0.75]
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

static = pygame.transform.rotozoom(pygame.image.load('static.jpg').convert(), 0, image_scale*5)
alpha = 64
static.fill((255,255,255,alpha),None, pygame.BLEND_RGBA_MULT)
staticTime = 0

staticClose1 = pygame.transform.scale((pygame.transform.rotozoom(pygame.image.load('staticClose1.png').convert(), 0, image_scale)),(screenWidth,screenHeight))
staticClose2 = pygame.transform.scale((pygame.transform.rotozoom(pygame.image.load('staticClose2.png').convert(), 0, image_scale)),(screenWidth,screenHeight))
staticClose3 = pygame.transform.scale((pygame.transform.rotozoom(pygame.image.load('staticClose3.png').convert(), 0, image_scale)),(screenWidth,screenHeight))
staticClose4 = pygame.transform.scale((pygame.transform.rotozoom(pygame.image.load('staticClose4.png').convert(), 0, image_scale)),(screenWidth,screenHeight))
black_back = pygame.transform.scale((pygame.transform.rotozoom(pygame.image.load('black_back.png').convert(), 0, image_scale)),(screenWidth,screenHeight))



background = pygame.transform.rotozoom(pygame.image.load('road.png').convert(), 0, image_scale)
bg_height = background.get_height()
darkbackground = pygame.Surface((screenWidth,screenHeight))
darkbackground.set_alpha(16)
darkbackground.fill((20,0,0))
blackBack = False
timebackground = pygame.Surface((screenWidth,screenHeight))
timebackground.set_alpha(32)
timebackground.fill((255,255,0))
whiteBackground = pygame.Surface((screenWidth,screenHeight))
whiteBackground.fill((255,255,255))

# define game variables
scroll = 0
tiles = 2
Right = False
Left = False
main_y = 400
times = 0
red_y = -800
green_y = -800
black_y = -800
x_pos = positions[1]
time1 = 0
time2 = 0
time3 = 0
redwarn = False
greenwarn = False
blackwarn = False
blackspawn = False
speed = 0
timeStop = False


def randomisePos(x, y, z):
    x = positions[random.randint(0, 3)]
    if x == y or x == z:
        return randomisePos(x, y, z)
    else:
        return x


def warntimer(warning_rect, warntype, time):
    global redwarn, greenwarn, blackwarn
    if time < 30:
        time += 1
        screen.blit(warning_surf, (warning_rect))
        return time
    else:
        time = 0
        if warntype == 'redwarn':
            redwarn = False
        if warntype == 'greenwarn':
            greenwarn = False
        if warntype == 'blackwarn':
            blackwarn = False
        return time


def summonWarning(x):
    warning_rect = warning_surf.get_rect(midtop=(x, 20*scale))
    return warning_rect

#score
game_font = pygame.font.Font('Pixeltype.ttf',int(100*image_scale))
score_text = "0"
score = 0
scoreboard = pygame.transform.rotozoom(pygame.image.load('ScoreBoard.png').convert_alpha(), 0, image_scale*5)
scoreboard_rect = scoreboard.get_rect(center=(300 * scale, 450 * scale))
slowingTime = 1
timeSlowDuration = 0
timeSlowCooldown = 0

#Text
text = ""


#Car Surfaces
warning_surf = pygame.transform.rotozoom(pygame.image.load('Warning.png').convert_alpha(), 0, image_scale * 0.5)
maincar_surf = pygame.transform.rotozoom(pygame.image.load('maincar.png').convert_alpha(), 0, image_scale * 0.1)
redcar_surf = pygame.transform.rotozoom(pygame.image.load('red_car.png').convert_alpha(), 0, image_scale * 0.12)
greencar_surf = pygame.transform.rotozoom(pygame.image.load('green_car.png').convert_alpha(), 0, image_scale * 0.15)
blackcar_surf = pygame.transform.rotozoom(pygame.image.load('black_car.png').convert_alpha(), 0, image_scale * 0.1)

#Hourglass states
hourglass1 = pygame.transform.rotozoom(pygame.image.load('Hourglass1.png').convert_alpha(), 0, image_scale * 5)
hourglass2 = pygame.transform.rotozoom(pygame.image.load('Hourglass2.png').convert_alpha(), 0, image_scale * 5)
hourglass3 = pygame.transform.rotozoom(pygame.image.load('Hourglass3.png').convert_alpha(), 0, image_scale * 5)
hourglass4 = pygame.transform.rotozoom(pygame.image.load('Hourglass4.png').convert_alpha(), 0, image_scale * 5)
hourglass5 = pygame.transform.rotozoom(pygame.image.load('Hourglass5.png').convert_alpha(), 0, image_scale * 5)
hourglass6 = pygame.transform.rotozoom(pygame.image.load('Hourglass6.png').convert_alpha(), 0, image_scale * 5)
hourglass7 = pygame.transform.rotozoom(pygame.image.load('Hourglass7.png').convert_alpha(), 0, image_scale * 5)
hourglass8 = pygame.transform.rotozoom(pygame.image.load('Hourglass8.png').convert_alpha(), 0, image_scale * 5)
hourglass9 = pygame.transform.rotozoom(pygame.image.load('Hourglass9.png').convert_alpha(), 0, image_scale * 5)
hourglass10 = pygame.transform.rotozoom(pygame.image.load('Hourglass10.png').convert_alpha(), 0, image_scale * 5)
hourglassFULL = pygame.transform.rotozoom(pygame.image.load('HourglassFULL.png').convert_alpha(), 0, image_scale * 5)
currentHourGlassState = hourglassFULL

#Car Positions
redx_pos = positions[random.randint(0, 3)]
greenx_pos = positions[random.randint(0, 3)]
blackx_pos = -100
redx_pos = randomisePos(redx_pos, greenx_pos,blackx_pos)


#Cannon Variables
cannon_up_surf = pygame.transform.rotozoom(pygame.image.load('Cannon_up.png').convert_alpha(), 0, image_scale*5)
cannon_2_surf = pygame.transform.rotozoom(pygame.image.load('Cannon_2.png').convert_alpha(), 0, image_scale*5)
cannon_fire_surf = pygame.transform.rotozoom(pygame.image.load('Cannon_fire.png').convert_alpha(), 0, image_scale*5)
bomb = pygame.transform.rotozoom(pygame.image.load('bomb.png').convert_alpha(), 0, image_scale*3)
bomb_rect = bomb.get_rect(center=(0, 0))
cannonPositions = [25*scale,300*scale]
canLeft = False
canRight = True
cannonTime = 0
cannonActivate = False
cannonY = screenHeight+40
respawn = True
canScoreFreq = 500
canTimeIncrease = 1

#Music/Sounds
music = pygame.mixer.music.load('Pixel_City.mp3')
pygame.mixer.music.play(-1)
cannonBlast = pygame.mixer.Sound('CannonBlast.mp3')
JojoTS = pygame.mixer.Sound('Jojo_TimeStop_2xSpeed.mp3')
static_sound = pygame.mixer.Sound('static_sound_effect.mp3')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and running == True:
            if event.key == pygame.K_a and Right == False:
                if x_pos > positions[0]:
                    Left = True
                    maincar_surf = pygame.transform.rotozoom(pygame.image.load('maincarLeft.png').convert_alpha(), 0,
                                                             image_scale * 0.1)
            elif event.key == pygame.K_d and Left == False:
                if x_pos < positions[3]:
                    Right = True
                    maincar_surf = pygame.transform.rotozoom(pygame.image.load('maincarRight.png').convert_alpha(), 0,
                                                             image_scale * 0.1)
            elif event.key == pygame.K_SPACE and timeSlowCooldown == 0:
                timeStop = True
                pygame.mixer.music.pause()
                JojoTS.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and main_y > 100*scale and running == True:
        main_y -= scale
    elif keys[pygame.K_s] and main_y < 440*scale and running == True:
        main_y += scale
    # drawing scrolling background
    for i in range(0, tiles):
        screen.blit(background, (0, -(i * bg_height) - scroll))

    # scroll background
    scroll -= 5*scale*slowingTime
    if abs(scroll) > bg_height:
        scroll = 0

    # checking and changing directions
    if Left == True and running == True:
        if times <= 11:
            x_pos -= 2.5*scale
        elif times > 11:
            x_pos -= 1.25*scale
        times += 1
        if times == 33:
            Right = False
            Left = False
            times = 0
            maincar_surf = pygame.transform.rotozoom(pygame.image.load('maincar.png').convert_alpha(), 0,
                                                     image_scale * 0.1)

    if Right == True and running == True:
        if times <= 11:
            x_pos += 2.5*scale
        elif times > 11:
            x_pos += 1.25*scale
        times += 1
        if times == 33:
            Right = False
            Left = False
            times = 0
            maincar_surf = pygame.transform.rotozoom(pygame.image.load('maincar.png').convert_alpha(), 0,
                                                     image_scale * 0.1)

    if red_y >= screenHeight and respawn == True:
        red_y = -400
        redx_pos = randomisePos(redx_pos, greenx_pos,blackx_pos)
        redwarn = True
    if green_y >= screenHeight and respawn == True:
        green_y = -400
        greenx_pos = randomisePos(greenx_pos, redx_pos, blackx_pos)
        greenwarn = True
    if black_y >= screenHeight and respawn == True and blackspawn == True:
        black_y = -400
        blackx_pos = randomisePos(blackx_pos, redx_pos, greenx_pos)
        blackwarn = True

    if greenwarn == True:
        warning_rect = summonWarning(greenx_pos)
        time1 = warntimer(warning_rect, 'greenwarn', time1)
    if redwarn == True:
        warning_rect = summonWarning(redx_pos)
        time2 = warntimer(warning_rect, 'redwarn', time2)
    if blackwarn == True:
        warning_rect = summonWarning(blackx_pos)
        time3 = warntimer(warning_rect, 'blackwarn', time3)

    maincar_rect = maincar_surf.get_rect(center=(x_pos, main_y))
    screen.blit(maincar_surf, (maincar_rect))
    redcar_rect = redcar_surf.get_rect(midtop=(redx_pos, red_y))
    greencar_rect = greencar_surf.get_rect(midtop=(greenx_pos, green_y))
    blackcar_rect = blackcar_surf.get_rect(midtop = (blackx_pos, black_y))
    screen.blit(redcar_surf, (redcar_rect))
    screen.blit(greencar_surf, (greencar_rect))
    screen.blit(blackcar_surf,blackcar_rect)
    red_y += (3+speed)*scale*slowingTime
    green_y += (2+speed)*scale*slowingTime
    black_y += (3.5+speed)*scale*slowingTime

    if maincar_rect.colliderect(greencar_rect) or maincar_rect.colliderect(redcar_rect) or maincar_rect.colliderect(blackcar_rect) or maincar_rect.colliderect(bomb_rect):
        running = False

    #score dependent events (fun fun fun)

    #Cannon
    if score % canScoreFreq == 0 and respawn == True:
        currentY = round(main_y)
        cannonActivate = True
        cannonX = cannonPositions[random.randint(0,1)]
        bombX = cannonX
        if cannonX == cannonPositions[1] and canLeft == True:
            cannon_2_surf = pygame.transform.rotate(cannon_2_surf, 180)
            cannon_fire_surf = pygame.transform.rotate(cannon_fire_surf, 180)
            canRight = True
            canLeft = False
        if cannonX == cannonPositions[0] and canRight == True:
            cannon_2_surf = pygame.transform.rotate(cannon_2_surf, 180)
            cannon_fire_surf = pygame.transform.rotate(cannon_fire_surf, 180)
            canRight = False
            canLeft = True

    if cannonActivate == True and respawn == True and score >=2500:
        if cannonY > currentY and cannonTime == 0:
            cannon_rect = cannon_up_surf.get_rect(center=(cannonX, cannonY))
            cannonY-=5*scale*slowingTime
            screen.blit(cannon_up_surf, cannon_rect)
        else:
            cannon_rect = cannon_2_surf.get_rect(center = (cannonX,cannonY))
            cannonTime += canTimeIncrease * slowingTime
            if cannonTime <= 15:
                screen.blit(cannon_2_surf, cannon_rect)
            if cannonTime > 15 and cannonTime <=30:
                cannon_rect = cannon_fire_surf.get_rect(center=(cannonX, cannonY))
                screen.blit(cannon_fire_surf, cannon_rect)
            if cannonTime == 30:
                cannonBlast.play()
            elif cannonTime > 30:
                if canRight == True:
                    bombX -= 4*scale*canTimeIncrease*slowingTime
                elif canLeft == True:
                    bombX +=4*scale*canTimeIncrease*slowingTime
                bomb_rect = bomb.get_rect(center=(bombX, currentY))
                screen.blit(bomb, bomb_rect)
                if cannonTime > 30 and cannonTime <=45:
                    screen.blit(cannon_fire_surf, cannon_rect)
                if cannonTime > 45 and cannonTime <=60:
                    screen.blit(cannon_2_surf, cannon_rect)
                if cannonTime > 60:
                    screen.blit(cannon_up_surf, cannon_rect)
                    cannonY+=5*scale*slowingTime
                if cannonY > screenHeight+(20*scale) and cannonTime > 150:
                    cannonActivate = False
                    cannonTime = 0
    #Score
    score_surface = game_font.render(score_text, True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(302 * scale, 452 * scale))
    screen.blit(scoreboard, scoreboard_rect)
    screen.blit(score_surface, score_rect)
    if running == True:
        score += 1 * slowingTime
    score_text = str(round(score))


    #Music
    if score == 7000:
        pygame.mixer.music.fadeout(5000)
        respawn = False
        text = "Did you think it would be that easy?"
    if score == 7250:
        pygame.mixer.music.unload()
        music = pygame.mixer.music.load('Apashe.mp3')
        pygame.mixer.music.play(-1)
        text = "How about we speed things up a bit."

    if blackBack == True:
        screen.blit(darkbackground,(0,0))

    if score == 7500:
        text = ""
        respawn = True
        canScoreFreq = 250
        canTimeIncrease = 1.5
        speed = 1
    if score == 17500:
        pygame.mixer.music.fadeout(5000)
        respawn = False
        text = "Still alive?"
    if score == 17650:
        text = "Let's slow done things a little."
    if score == 17850:
        text = "You'll need a rest for what comes next."
    if score == 18001:
        respawn = True
        text = ""
        pygame.mixer.music.unload()
        music = pygame.mixer.music.load('Pixel_City.mp3')
        pygame.mixer.music.play(-1)
        canScoreFreq = 500
        canTimeIncrease = 1
        speed = 0

    if score == 22000:
        respawn = False
        pygame.mixer.music.fadeout(5000)
        text = "I told you it wouldn't be so easy."
    if score == 22250:
        text = "How about I add something... extra?"
    #TheBlackCar
    if score == 22501:
        respawn = True
        text = ""
        blackspawn = True
        pygame.mixer.music.unload()
        music = pygame.mixer.music.load('The_Rebel_path.mp3')
        pygame.mixer.music.play(-1)
        blackBack = True
        speed = 0.5

    if score == 30000:
        respawn = False
        text = "You're tougher than expected."
    if score == 30250:
        text = "Time to speed things up."
    if score == 30501:
        respawn = True
        text =""
        speed = 1.25
        canScoreFreq = 350
        canTimeIncrease = 1.5
    if score == 40000:
        respawn = False
        text = "I've seen enough."
    if score == 40200:
        text = "This is it."
    if score == 40400:
        text = "This is where you die. No-matter what."
    if score == 40600:
        text = "Survive."
        text_surface = game_font.render(text, True, (0,0,0))
    if score == 40750:
        text = ""
        text_surface = game_font.render(text, True, (0, 0, 0))
        respawn = True
        speed = 2
        canScoreFreq = 250
        canTimeIncrease = 2


    #Text
    if score < 40600:
        text_surface = game_font.render(text, True, (139,0,0))
    text_rect = text_surface.get_rect(center=(screenWidth/2,80*scale))
    screen.blit(text_surface,text_rect)

    if timeStop == True:
        slowingTime = 0.25
        screen.blit(timebackground,(0,0))
        timeSlowDuration +=1
        timeSlowCooldown+=15
        if timeSlowDuration == 240:
            timeSlowDuration = 0
            timeStop = False
            slowingTime = 1
            currentHourGlassState = hourglass1
            score=round(score)
            pygame.mixer.music.unpause()

    if timeSlowCooldown !=0 and timeStop == False:
        timeSlowCooldown -=1

    screen.blit(currentHourGlassState,(0,0))
    #Stinky Inefficent but easy alternating hourglass display method
    if timeSlowCooldown == 3240:
        currentHourGlassState = hourglass2
    if timeSlowCooldown == 2880:
        currentHourGlassState = hourglass3
    if timeSlowCooldown == 2520:
        currentHourGlassState = hourglass4
    if timeSlowCooldown == 2160:
        currentHourGlassState = hourglass5
    if timeSlowCooldown == 1800:
        currentHourGlassState = hourglass6
    if timeSlowCooldown == 1440:
        currentHourGlassState = hourglass7
    if timeSlowCooldown == 1080:
        currentHourGlassState = hourglass8
    if timeSlowCooldown == 720:
        currentHourGlassState = hourglass9
    if timeSlowCooldown == 360:
        currentHourGlassState = hourglass10
    if timeSlowCooldown == 0:
        currentHourGlassState = hourglassFULL

    if running == False:
        pygame.mixer.music.stop()
        slowingTime = 0
        if staticTime == 0:
            static_sound.play()
        if staticTime < 150:
            static_rect = static.get_rect(center=(screenWidth / 2, screenHeight / 2))
            screen.blit(static,static_rect)
        staticTime+=1
        if staticTime % 5 ==0:
            static = pygame.transform.rotate(static,90)
        if staticTime >= 150 and staticTime < 160:
            screen.blit(staticClose1,(0,0))
        if staticTime >= 160 and staticTime < 170:
            screen.blit(staticClose2,(0,0))
        if staticTime >= 170 and staticTime < 180:
            screen.blit(staticClose3,(0,0))
        if staticTime >= 180 and staticTime < 190:
            screen.blit(staticClose4,(0,0))
        if staticTime >= 190 and staticTime < 250:
            screen.blit(black_back,(0,0))
        if staticTime >=250:
            game_font = pygame.font.Font('Pixeltype.ttf', int(200 * image_scale))
            text_surface = game_font.render(text, True, (0, 0, 0))
            text = "Score: "+str(score)
            text_rect = text_surface.get_rect(center=(screenWidth/2,screenHeight/2))
            screen.blit(whiteBackground,(0,0))
            screen.blit(text_surface, text_rect)

    pygame.display.update()
    clock.tick(60)