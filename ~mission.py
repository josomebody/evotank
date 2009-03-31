import signal
from classes import *

def mission():
    random.seed()
    print 'Initializing pygame'
    pygame.init()
    levelfiles = ['/levels/level1']
    levels = []
    currentlevel = 0
    currentroom= 0
    protobullet = projectile()
    protobot = robot()
    you = player()
    thisgame = gamedetails()
    print "Opening display 640x480 full-screen"
    screen = pygame.display.set_mode((640, 480), FULLSCREEN)
    pygame.display.set_caption('EvoTank')
    pygame.mouse.set_visible(False)
    gameconsole = console()

    print "Loading images..."
    font = pygame.font.SysFont("Terminal", 14)
    armorpic = pygame.image.load('images/armor.png').convert_alpha()
    ammopic = pygame.image.load('images/ammo.png').convert_alpha()
    fuelpic = pygame.image.load('images/fuel.png').convert_alpha()
    barrelpic = pygame.image.load('images/barrel.png').convert_alpha()
    cratepic = pygame.image.load('images/crate.png').convert_alpha()
    heattx = font.render('HEAT', True, (255, 255, 255))
    armortx = font.render('ARMOR', True, (255, 255, 255))
    fueltx = font.render('FUEL', True, (255, 255, 255))
    ammotx = font.render('AMMO', True, (255, 255, 255))
    throttlex = font.render('THROTTLE', True, (255, 255, 255))

    bulletpic = []
    goodtankpic = []
    badtankpic = []
    doorpic = []
    for i in range(8):
        picname = 'images/bullet' + str(i) + '.png'
        tempic = pygame.image.load(picname).convert_alpha()
        bulletpic.append(tempic)
        picname = 'images/goodtank' + str(i) + '.png'
        tempic = pygame.image.load(picname).convert_alpha()
        goodtankpic.append(tempic)
        picname = 'images/badtank' + str(i) + '.png'
        tempic = pygame.image.load(picname).convert_alpha()
        badtankpic.append(tempic)
    for i in range(4):
        picname = 'images/door' + str(i) + '.png'
        tempic = pygame.image.load(picname).convert_alpha()
        doorpic.append(tempic)
    
    gameconsole.write("Loading sounds...")
    bang = pygame.mixer.Sound('sounds/bang.wav')
    clank = pygame.mixer.Sound('sounds/clank.wav')
    ping = pygame.mixer.Sound('sounds/ping.wav')
    diesound = pygame.mixer.Sound('sounds/die.wav')
    lowammosound = pygame.mixer.Sound('sounds/ammo.wav')
    lowarmorsound = pygame.mixer.Sound('sounds/armor.wav')
    lowfuelsound = pygame.mixer.Sound('sounds/fuel.wav')
    overheatsound = pygame.mixer.Sound('sounds/heat.wav')
    latersound = pygame.mixer.Sound('sounds/later.wav')
    letsgosound = pygame.mixer.Sound('sounds/letsgo.wav')
#        protobot.dead = 0
#        protobot.hitstilmating = 5
#        protobot.state = 0
#        protobot.armor = maxarmor
#        protobot.fuel = maxfuel
#        protobot.ammo = maxammo
#        protobot.offspring = robot()
#        robots.append(protobot)
    gameconsole.write('Loading levels...')
    for i in range(len(levelfiles)):
        protolevel = level()
        protolevel = protolevel.load(levelfiles[i])
    #initialize game coordinates and shit
    currentlevel = 
    ptypes = ['fuel', 'armor', 'ammo']                
    robotstats = []
    robotstatspic = []
    bulletcount = 0
    lowfuelflag = 0
    lowammoflag = 0
    lowarmorflag = 0
    overheatflag = 0
    fps = [0]
    fpsavg = 0
    frametime = 0
    showfps = 1
    showconsole = 1
    showmeters = 1
    code_entry = []
    tooslow = 0
    dropframe = 0
    framedelay = 0
    firstframe = 1
        #main gameloop
    framestarttime = pygame.time.get_ticks()
    while 1:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)
        pygame.event.pump()
        if fpsavg > 70:
            framedelay = (1000 - 1000 / frametime) / 60
        #first of all, check for births
        for i in range(len(robots)):
               if robots[i].gestation == 1:
                robots.append(robots[i].givebirth())
                gameconsole.write(robots[i].name + ' has given birth to ' + robots[len(robots) - 1].name)

        #draw everybody
        if fpsavg < 20:
            tooslow = tooslow + 1
            if tooslow > 3:
                print 'Dropped frame (fps: ' + str(fps[len(fps) - 1]) + ') (average fps for last 100 frames:' + str(fpsavg) + ')'
                dropframe = 1
                tooslow = 0
        else:
            tooslow = 0
            dropframe = 0
        if dropframe == 1:
            gameconsole.write('frame dropped (' + str(frametime) + ')')
            gameconsole.blit(screen, font)
        else:
            screen.blit(background, (0, 0))
            for i in range(len(currentlevel.rooms[currentroom].pickups)):
                if currentlevel.rooms[currentroom].pickups[i].pickuptype == 'fuel':
                    screen.blit(fuelpic, (currentlevel.rooms[currentroom].pickups[i].x, currentlevel.rooms[currentroom].pickups[i].y))
                if currentlevel.rooms[currentroom].pickups[i].pickuptype == 'ammo':
                    screen.blit(ammopic, (currentlevel.rooms[currentroom].pickups[i].x, currentlevel.rooms[currentroom].pickups[i].y))
                if currentlevel.rooms[currentroom].pickups[i].pickuptype == 'armor':
                    screen.blit(armorpic, (currentlevel.rooms[currentroom].pickups[i].x, currentlevel.rooms[currentroom].pickups[i].y))
            for i in range(len(currentlevel.rooms[currentroom].bullets)):
                screen.blit(bulletpic[currentlevel.rooms[currentroom].bullets[i].rotate], (currentlevel.rooms[currentroom].bullets[i].x, currentlevel.rooms[currentroom].bullets[i].y))
            for i in range(len(currentlevel.rooms[currentroom].robots)):
                screen.blit(badtankpic[currentlevel.rooms[currentroom].robots[i].rotate], (currentlevel.rooms[currentroom].robots[i].x, currentlevel.rooms[currentroom].robots[i].y))
            screen.blit(goodtankpic[you.rotate], (you.x, you.y))
            del robotstats[:]
            del robotstatspic[:]
            for i in range(len(currentlevel.rooms[currentroom].robots)):
                robotag = currentlevel.rooms[currentroom].robots[i].name + ' '
                if currentlevel.rooms[currentroom].robots[i].state == 10:
                    robotag = robotag + '(***mating w/ ' + currentlevel.rooms[currentroom].robots[i].partner + '***)'
                if currentlevel.rooms[currentroom].robots[i].state == 11:
                    robotag = robotag + '(***gestating***)'
                robotstats.append(robotag)
            for i in range(len(robotstats)):
                robotstatspic.append(font.render(robotstats[i], True, (255, 0, 0)))

            for i in range(len(currentlevel.rooms[currentroom].robots)):
                screen.blit(robotstatspic[i], (currentlevel.rooms[currentroom].robots[i].x, currentlevel.rooms[currentroom].robots[i].y))
            if showconsole == 1:
                gameconsole.blit(screen, font)
            if showmeters == 1:
                pygame.draw.rect(screen, (64, 0, 0), (0, 470, you.heat / 20, 10))
                pygame.draw.rect(screen, (0, 0, 64), (110, 470, you.armor, 10))
                pygame.draw.rect(screen, (0, 64, 0), (220, 470, (you.fuel / 50), 10))
                pygame.draw.rect(screen, (32, 32, 64), (330, 470, you.ammo, 10))
                if you.velocity < -1:
                    pygame.draw.rect(screen, (64, 64, 0), (450, 470, 25, 10))
                if you.velocity < 0:
                    pygame.draw.rect(screen, (64, 64, 0), (475, 470, 25, 10))
                if you.velocity > 0:
                    pygame.draw.rect(screen, (64, 64, 0), (500, 470, 25, 10))
                if you.velocity > 1:
                    pygame.draw.rect(screen, (64, 64, 0), (525, 470, 25, 10))
                screen.blit(heattx, (0, 470))
                screen.blit(armortx, (110, 470))
                screen.blit(fueltx, (220, 470))
                screen.blit(ammotx, (330, 470))
                screen.blit(throttlex, (465, 470))
        if showfps == 1:
            fpsstring = 'fps: ' + str(fpsavg)
            fpspic = font.render(fpsstring, True, (255, 128, 0))
            screen.blit(fpspic, (640 - len(fpsstring) * 7, 0))
        dropframe = 0
        if firstframe == 1:
            letsgopic = font.render('LET\'S GO!', True, (255, 255, 255))
            screen.blit(letsgopic, (257, 233))
            pygame.display.flip()
            letsgosound.play(0)
            for killsometime in range(10):
                screen.blit(badtankpic[you.rotate], (you.x, you.y))
                pygame.display.flip()
                pygame.time.wait(50)
                screen.blit(goodtankpic[you.rotate], (you.x, you.y))
                pygame.display.flip()
                pygame.time.wait(50)
            firstframe = 0
        pygame.display.flip()
        #everybody gets a turn
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    gameconsole.write('SELF-DESTRUCT')
                    you.armor = 0
                elif event.key == K_f:
                    if showfps == 0:
                        showfps = 1
                    elif showfps == 1:
                        showfps = 0
                    else:
                        showfps = 0
                elif event.key == K_c:
                    if showconsole == 0:
                        showconsole = 1
                    else:
                        showconsole = 0
                elif event.key == K_m:
                    if showmeters == 0:
                        showmeters = 1
                    else:
                        showmeters = 0
                elif (event.key == K_UP) or (event.key == K_DOWN) or (event.key == K_LEFT) or (event.key == K_RIGHT) or (event.key == K_SPACE):
                    you.control(event.key, currentlevel.rooms[currentroom].bullets, bang)
                else:
                    code_entry.append(decoderkey(event.key))
                    if pygame.time.get_ticks() % 2000 == 0:
                        if len(entry_code) > 0:
                            del code_entry[0]
                    if code_entry == ['i', 'd']:
                        del code_entry[:]
                        gameconsole.write('this ain\'t doom, moron!')
                        for i in range(15):
                            punishment = open('savedbots/cicte', 'r')
                            protobot = pickle.load(punishment)
                            punishment.close
                            protobot.x = you.x
                            protobot.y = you.y
                            protobot.dead = 0
                            protobot.state = 0
                            protobot.gestation = 0
                            currentlevel.rooms[currentroom].robots.append(protobot)
                    if code_entry == ['j', 'j', 'g', 'u', 'n']:
                        del code_entry[:]
                        gameconsole.write('ammo cheat')
                        you.ammo = maxammo
                    if code_entry == ['j', 'j', 'g', 'a', 's']:
                        del code_entry[:]
                        gameconsole.write('fuel cheat')
                        you.fuel = maxfuel
                    if code_entry == ['j', 'j', 's', 'u', 'i', 't']:
                        del code_entry[:]
                        gameconsole.write('armor cheat')
                        you.armor = maxarmor
                    if code_entry == ['j', 'j', 'k', 'o', 'o', 'l']:
                        del code_entry[:]
                        gameconsole.write('heat cheat')
                        you.heat = 0
                    if code_entry == ['j', 'j', 'k', 'i', 'l', 'l', 'a', 'l', 'l']:
                        del code_entry[:]
                        gameconsole.write('massacre cheat')
                        for i in range(len(currentlevel.rooms[currentroom].robots)-1):
                            currentlevel.rooms[currentroom].robots[i].armor = 1
                            
        for i in range(len(currentlevel.rooms[currentroom].robots)):
            currentlevel.rooms[currentroom].robots[i].letsgo(currentlevel.rooms[currentroom].bullets, currentlevel.rooms[currentroom].pickups, currentlevel.rooms[currentroom].robots, you, bang, i)
        
        #move everybody
        if dropframe != 1:
            for i in range(len(currentlevel.rooms[currentroom].bullets)):
                currentlevel.rooms[currentroom].bullets[i].move()
            for i in range(len(currentlevel.rooms[currentroom].robots)):
                currentlevel.rooms[currentroom].robots[i].move()
        you.move() #if your machine is going too slow, you get bullet-time!
            
        #and now the expensive part: collision checks and shit
        if dropframe != 1:
            for i in range(len(currentlevel.rooms[currentroom].bullets)):
                if currentlevel.rooms[currentroom].bullets[i].offscreen() == 1:
                    currentlevel.rooms[currentroom].bullets[i].dead = 1
            
            for i in range(len(currentlevel.rooms[currentroom].bullets)):
                if (detect_collision(currentlevel.rooms[currentroom].bullets[i], currentlevel.rooms[currentroom].bulletsize, you, tanksize) == 1) and (currentlevel.rooms[currentroom].bullets[i].originator != you.name):
                    you.armor = you.armor - 5
                    for j in range(len(currentlevel.rooms[currentroom].robots)):
                        if currentlevel.rooms[currentroom].bullets[i].originator == currentlevel.rooms[currentroom].robots[j].name:
                            currentlevel.rooms[currentroom].robots[j].hits = currentlevel.rooms[currentroom].robots[j].hits + 1
                            currentlevel.rooms[currentroom].robots[j].hitstilmating = currentlevel.rooms[currentroom].robots[j].hitstilmating - 1
                            if currentlevel.rooms[currentroom].robots[j].hitstilmating < 0:
                                currentlevel.rooms[currentroom].robots[j].hitstilmating = 5
                            gameconsole.write((currentlevel.rooms[currentroom].robots[j].name + ' scored hit #' + str(currentlevel.rooms[currentroom].robots[j].hits)))
                    currentlevel.rooms[currentroom].bullets[i].dead = 1
                    clank.play(0)
                    
            for i in range(len(currentlevel.rooms[currentroom].bullets)):
                for j in range(len(currentlevel.rooms[currentroom].robots)):
                    if (detect_collision(currentlevel.rooms[currentroom].bullets[i], bulletsize, currentlevel.rooms[currentroom].robots[j], tanksize) == 1) and (currentlevel.rooms[currentroom].bullets[i].originator != currentlevel.rooms[currentroom].robots[j].name):
                        currentlevel.rooms[currentroom].robots[j].armor = currentlevel.rooms[currentroom].robots[j].armor - 5
                        currentlevel.rooms[currentroom].bullets[i].dead = 1
                        clank.play(0)
                        
            for i in range(len(currentlevel.rooms[currentroom].pickups)):
                if detect_collision(currentlevel.rooms[currentroom].pickups[i], pickupsize, you, tanksize) == 1:
                    if you.cangetpickup(currentlevel.rooms[currentroom].pickups[i].pickuptype):
                        you.getpickup(currentlevel.rooms[currentroom].pickups[i].pickuptype)
                        currentlevel.rooms[currentroom].pickups[i].dead = 1
                        ping.play(0)
                        
            for i in range(len(currentlevel.rooms[currentroom].pickups)):
                for j in range(len(currentlevel.rooms[currentroom].robots)):
                    if detect_collision(currentlevel.rooms[currentroom].pickups[i], pickupsize, currentlevel.rooms[currentroom].robots[j], tanksize) == 1:
                        if currentlevel.rooms[currentroom].robots[j].cangetpickup(currentlevel.rooms[currentroom].pickups[i].pickuptype):
                            currentlevel.rooms[currentroom].robots[j].getpickup(currentlevel.rooms[currentroom].pickups[i].pickuptype)
                            currentlevel.rooms[currentroom].pickups[i].dead = 1
                            ping.play(0)
            
            for i in range(len(currentlevel.rooms[currentroom].robots)):
                if detect_collision(currentlevel.rooms[currentroom].robots[i], tanksize, you, tanksize) == 1:
                    bounce(currentlevel.rooms[currentroom].robots[i], you)
                    clank.play(0)
                for j in range(len(currentlevel.rooms[currentroom].robots)):
                    if i != j:
                        if detect_collision(currentlevel.rooms[currentroom].robots[i], tanksize, currentlevel.rooms[currentroom].robots[j], tanksize) == 1:
                            bounce(currentlevel.rooms[currentroom].robots[i], currentlevel.rooms[currentroom].robots[j])
                            clank.play(0)
                        
        #and now for the sad part: coping with death
        if you.armor <= 0:
            diesound.play(0)
            screen.blit(background,(0,0))
            gameconsole.write('you got pwned. continue? y/N')
            gameconsole.blit(screen, font)
            pygame.display.flip()
            pygame.time.wait(1000)
            choicekey = 0
            signal.alarm(0)
            while choicekey != K_y:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                            choicekey = event.key
                            if event.key == K_y:
                                signal.alarm(5)
                                you.armor = 100
                                firstframe = 1
                                gameconsole.write('continuing after getting pwned')
                            elif event.key == K_n:
                                latersound.play(0)
                                pygame.time.wait(1500)
                                return 0
        for i in range(len(currentlevel.rooms[currentroom].robots)):
            if currentlevel.rooms[currentroom].robots[i].armor <=0:
                currentlevel.rooms[currentroom].robots[i].dead = 1
                gameconsole.write(currentlevel.rooms[currentroom].robots[i].name + ' died.')
        
        #and getting rid of the bodies
        if dropframe != 1:
            for i in range(len(currentlevel.rooms[currentroom].robots)):
                if i < len(currentlevel.rooms[currentroom].robots):
                    if currentlevel.rooms[currentroom].robots[i].dead == 1:
                        del currentlevel.rooms[currentroom].robots[i]
                        diesound.play(0)
                        
            for i in range(len(currentlevel.rooms[currentroom].bullets)):
                if i < len(currentlevel.rooms[currentroom].bullets):
                    if currentlevel.rooms[currentroom].bullets[i].dead == 1:
                        del currentlevel.rooms[currentroom].bullets[i]
                        
            for i in range(len(currentlevel.rooms[currentroom].pickups)):
                if i < len(currentlevel.rooms[currentroom].pickups):
                    if currentlevel.rooms[currentroom].pickups[i].dead ==1:
                        del currentlevel.rooms[currentroom].pickups[i]
                        
        #and playing game warning sounds
        if you.armor < 50:
            if lowarmorflag == 0:
                lowarmorsound.play(0)
                lowarmorflag = 1
        else:
            lowarmorflag = 0
            
        if you.ammo < 10:
            if lowammoflag == 0:
                lowammosound.play(0)
                lowammoflag = 1
        else:
            lowammoflag = 0
            
        if you.fuel < 1000:
            if lowfuelflag == 0:
                lowfuelsound.play(0)
                lowfuelflag = 1
        else:
            lowfuelflag = 0
        if you.heat > 1000:
            if overheatflag == 0:
                overheatsound.play(0)
                overheatflag = 1
        elif you.heat < 950:
            overheatflag = 0
        
        #get the fps so we can act accordingly
        if (framedelay > 1) and (framedelay < 16):
            pygame.time.wait(framedelay)
        frametime = pygame.time.get_ticks() - framestarttime
        if frametime > 0: #you never know. if a frame is executed in less than 1 ms, don't worry about it
            fps.append(1000 / frametime)
            if len(fps) > 100:
                del fps[0]
            fpsavg = sum(fps) / len(fps)
        framestarttime = pygame.time.get_ticks()
        signal.alarm(0)

def handler(signum, frame):
    print "CRASH! Frame got stuck!"
    raise SystemExit
                   
def main():
    startagain = 1
    while startagain == 1:
        startagain = mission()
    raise SystemExit

main()