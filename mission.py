import signal
#import psyco
from evotankclasses import *
from evotanklevels import *
#psyco.full()
def mission(currentlevel, levels, screen):
    random.seed()
    protobullet = projectile()
    protobot = robot()
    you = player()
    you.room= 0
    you.x = levels[currentlevel].playerx
    you.y = levels[currentlevel].playery
    you.rotate = levels[currentlevel].playerrotate
    thisgame = gamedetails()
    gameconsole = console()

    print "Loading images..."
    font = pygame.font.SysFont("Terminal", 14)
    armorpic = pygame.image.load('images/armor.png').convert_alpha()
    ammopic = pygame.image.load('images/ammo.png').convert_alpha()
    fuelpic = pygame.image.load('images/fuel.png').convert_alpha()
    barrelpic = pygame.image.load('images/barrel.png').convert_alpha()
    cratepic = pygame.image.load('images/crate.png').convert_alpha()
    wallpic = pygame.image.load('images/wall.png').convert_alpha()
    heattx = font.render('HEAT', True, (255, 255, 255))
    armortx = font.render('ARMOR', True, (255, 255, 255))
    fueltx = font.render('FUEL', True, (255, 255, 255))
    ammotx = font.render('AMMO', True, (255, 255, 255))
    throttlex = font.render('THROTTLE', True, (255, 255, 255))

    bulletpic = []
    goodtankpic = []
    badtankpic = []
    doorpic = []
    obstaclepic = []
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
    tempic = pygame.image.load('images/barrel.png').convert_alpha()
    obstaclepic.append(tempic)
    tempic = pygame.image.load('images/crate.png').convert_alpha()
    obstaclepic.append(tempic)
    tempic = pygame.image.load('images/wall.png').convert_alpha()
    obstaclepic.append(tempic)
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
    #initialize game coordinates and shit
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
    stillcheat = 0
    clipdoors = 0
    background = pygame.image.load(levels[currentlevel].rooms[you.room].background).convert()
        #main gameloop
    pygame.mixer.music.load(levels[currentlevel].music)
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(-1)
    font = pygame.font.SysFont('Terminal', 14)
    shotsfired = 0
    shotslanded = 0
    framestarttime = pygame.time.get_ticks()
    leveltimezero = pygame.time.get_ticks()
    while 1:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)
        pygame.event.pump()
        if fpsavg > 70:
            framedelay = (1000 - 1000 / frametime) / 60
        #first of all, check for births
        #for i in range(len(levels[currentlevel].rooms[you.room].robots)):
        #    if levels[currentlevel].rooms[you.room].robots[i].gestation == 1:
         #       levels[currentlevel].rooms[you.room].robots.append(levels[currentlevel].rooms[you.room].robots[i].givebirth())
          #      gameconsole.write(levels[currentlevel].rooms[you.room].robots[i].name + ' has given birth to ' + levels[currentlevel].rooms[you.room].robots[len(levels[currentlevel].rooms[you.room].robots) - 1].name)

        #draw everybody
        if fpsavg < 20:
            tooslow = tooslow + 1
            if tooslow > 30:
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
            for i in range(len(levels[currentlevel].rooms[you.room].pickups)):
                if levels[currentlevel].rooms[you.room].pickups[i].pickuptype == 'fuel':
                    screen.blit(fuelpic, (levels[currentlevel].rooms[you.room].pickups[i].x, levels[currentlevel].rooms[you.room].pickups[i].y))
                if levels[currentlevel].rooms[you.room].pickups[i].pickuptype == 'ammo':
                    screen.blit(ammopic, (levels[currentlevel].rooms[you.room].pickups[i].x, levels[currentlevel].rooms[you.room].pickups[i].y))
                if levels[currentlevel].rooms[you.room].pickups[i].pickuptype == 'armor':
                    screen.blit(armorpic, (levels[currentlevel].rooms[you.room].pickups[i].x, levels[currentlevel].rooms[you.room].pickups[i].y))
            for i in range(len(levels[currentlevel].rooms[you.room].bullets)):
                screen.blit(bulletpic[levels[currentlevel].rooms[you.room].bullets[i].rotate], (levels[currentlevel].rooms[you.room].bullets[i].x, levels[currentlevel].rooms[you.room].bullets[i].y))
            for i in range(len(levels[currentlevel].rooms[you.room].robots)):
                screen.blit(badtankpic[levels[currentlevel].rooms[you.room].robots[i].rotate], (levels[currentlevel].rooms[you.room].robots[i].x, levels[currentlevel].rooms[you.room].robots[i].y))
            screen.blit(goodtankpic[you.rotate], (you.x, you.y))
            for i in range(len(levels[currentlevel].rooms[you.room].obstacles)):
                screen.blit(obstaclepic[levels[currentlevel].rooms[you.room].obstacles[i].obstacletypenum], (levels[currentlevel].rooms[you.room].obstacles[i].x, levels[currentlevel].rooms[you.room].obstacles[i].y))
            for i in range(len(levels[currentlevel].rooms[you.room].doors)):
                screen.blit(doorpic[levels[currentlevel].rooms[you.room].doors[i].rotate], (levels[currentlevel].rooms[you.room].doors[i].x, levels[currentlevel].rooms[you.room].doors[i].y))
            del robotstats[:]
            del robotstatspic[:]
            for i in range(len(levels[currentlevel].rooms[you.room].robots)):
                robotag = levels[currentlevel].rooms[you.room].robots[i].name + ' '
                if levels[currentlevel].rooms[you.room].robots[i].state == 10:
                    levels[currentlevel].rooms[you.room].robots[i].state = 0 #robotag = robotag + '(***mating w/ ' + levels[currentlevel].rooms[you.room].robots[i].partner + '***)'
                if levels[currentlevel].rooms[you.room].robots[i].state == 11:
                    levels[currentlevel].rooms[you.room].robots[i].state = 0 #robotag = robotag + '(***gestating***)'
                robotstats.append(robotag)
            for i in range(len(robotstats)):
                robotstatspic.append(font.render(robotstats[i], True, (255, 0, 0)))

            for i in range(len(levels[currentlevel].rooms[you.room].robots)):
                screen.blit(robotstatspic[i], (levels[currentlevel].rooms[you.room].robots[i].x, levels[currentlevel].rooms[you.room].robots[i].y))
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
            letsgopic = font.render('LEVEL ' + str(currentlevel) + '...LET\'S GO!', True, (255, 255, 255))
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
                    didyoushoot = len(levels[currentlevel].rooms[you.room].bullets)
                    you.control(event.key, levels[currentlevel].rooms[you.room].bullets, bang)
                    if len(levels[currentlevel].rooms[you.room].bullets) > didyoushoot:
                        shotsfired += 1
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
                            protobot.moveable = 1
                            protobot.dead = 0
                            protobot.state = 0
                            protobot.gestation = 0
                            levels[currentlevel].rooms[you.room].robots.append(protobot)
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
                        for i in range(len(levels[currentlevel].rooms[you.room].robots)-1):
                            levels[currentlevel].rooms[you.room].robots[i].armor = 1
                    if code_entry == ['j', 'j', 's', 't', 'i', 'l', 'l']:
                        gameconsole.write('still cheat')
                        if stillcheat == 0:
                            stillcheat = 1
                        else:
                            stillcheat = 0
        for i in range(len(levels[currentlevel].rooms[you.room].robots)):
            levels[currentlevel].rooms[you.room].robots[i].letsgo(levels[currentlevel].rooms[you.room].bullets, levels[currentlevel].rooms[you.room].pickups, levels[currentlevel].rooms[you.room].robots, you, bang, i)
        
        #move everybody
        if dropframe != 1:
            for i in range(len(levels[currentlevel].rooms[you.room].bullets)):
                levels[currentlevel].rooms[you.room].bullets[i].move()
            for i in range(len(levels[currentlevel].rooms[you.room].robots)):
                if stillcheat == 0:
                    levels[currentlevel].rooms[you.room].robots[i].move()
        you.move() #if your machine is going too slow, you get bullet-time!
        if clipdoors > 0:
            clipdoors -= you.velocity
        if clipdoors < 0:
            clipdoors = 0
            
        #and now the expensive part: collision checks and shit
        for i in range(len(levels[currentlevel].rooms[you.room].doors)):
            if (detect_collision(you, tanksize, levels[currentlevel].rooms[you.room].doors[i], doorsize)) == 1 and (clipdoors == 0):
                clipdoors = doorsize * 2
                you.x = levels[currentlevel].rooms[you.room].doors[i].to_x
                you.y = levels[currentlevel].rooms[you.room].doors[i].to_y
                you.room = levels[currentlevel].rooms[you.room].doors[i].to_room
                pygame.draw.rect(screen, (0,0,0), (0,0,640,480))
                pygame.display.flip()
                background = pygame.image.load(levels[currentlevel].rooms[you.room].background).convert()
                gameconsole.write('Entering room #' + str(you.room + 1) + ' of ' + str(len(levels[currentlevel].rooms)) + ' of Level #' + str(currentlevel + 1))
                diesound.play(0)
                break
        for i in range(len(levels[currentlevel].rooms[you.room].obstacles)):
            if levels[currentlevel].rooms[you.room].obstacles[i].obstacletypenum == 2:
                usesize = wallsize
            else:
                usesize = obstaclesize
            if (detect_collision(you, tanksize, levels[currentlevel].rooms[you.room].obstacles[i], usesize)) == 1:
                bounce(you, levels[currentlevel].rooms[you.room].obstacles[i])
                clank.play(0)
            for j in range(len(levels[currentlevel].rooms[you.room].robots)):
                if (detect_collision(levels[currentlevel].rooms[you.room].robots[j], tanksize, levels[currentlevel].rooms[you.room].obstacles[i], usesize)) == 1:
                    bounce(levels[currentlevel].rooms[you.room].robots[j], levels[currentlevel].rooms[you.room].obstacles[i])
                    clank.play(0)
            for j in range(len(levels[currentlevel].rooms[you.room].bullets)):
                if (detect_collision(levels[currentlevel].rooms[you.room].bullets[j], bulletsize, levels[currentlevel].rooms[you.room].obstacles[i], usesize)) == 1:
                    levels[currentlevel].rooms[you.room].bullets[j].dead = 1
                    clank.play(0)
        if dropframe != 1:
            for i in range(len(levels[currentlevel].rooms[you.room].bullets)):
                if levels[currentlevel].rooms[you.room].bullets[i].offscreen() == 1:
                    levels[currentlevel].rooms[you.room].bullets[i].dead = 1
            
            for i in range(len(levels[currentlevel].rooms[you.room].bullets)):
                if (detect_collision(levels[currentlevel].rooms[you.room].bullets[i], bulletsize, you, tanksize) == 1) and (levels[currentlevel].rooms[you.room].bullets[i].originator != you.name):
                    you.armor = you.armor - 5
                    for j in range(len(levels[currentlevel].rooms[you.room].robots)):
                        if levels[currentlevel].rooms[you.room].bullets[i].originator == levels[currentlevel].rooms[you.room].robots[j].name:
                            levels[currentlevel].rooms[you.room].robots[j].hits = levels[currentlevel].rooms[you.room].robots[j].hits + 1
                            levels[currentlevel].rooms[you.room].robots[j].hitstilmating = levels[currentlevel].rooms[you.room].robots[j].hitstilmating - 1
                            if levels[currentlevel].rooms[you.room].robots[j].hitstilmating < 5:
                                levels[currentlevel].rooms[you.room].robots[j].hitstilmating = 5
                            gameconsole.write((levels[currentlevel].rooms[you.room].robots[j].name + ' scored hit #' + str(levels[currentlevel].rooms[you.room].robots[j].hits)))
                    levels[currentlevel].rooms[you.room].bullets[i].dead = 1
                    clank.play(0)
                    
            for i in range(len(levels[currentlevel].rooms[you.room].bullets)):
                for j in range(len(levels[currentlevel].rooms[you.room].robots)):
                    if (detect_collision(levels[currentlevel].rooms[you.room].bullets[i], bulletsize, levels[currentlevel].rooms[you.room].robots[j], tanksize) == 1) and (levels[currentlevel].rooms[you.room].bullets[i].originator != levels[currentlevel].rooms[you.room].robots[j].name):
                        levels[currentlevel].rooms[you.room].robots[j].armor = levels[currentlevel].rooms[you.room].robots[j].armor - 5
                        if levels[currentlevel].rooms[you.room].bullets[i].originator == 'bitch':
                            shotslanded += 1
                        levels[currentlevel].rooms[you.room].bullets[i].dead = 1
                        clank.play(0)
                        
            for i in range(len(levels[currentlevel].rooms[you.room].pickups)):
                if detect_collision(levels[currentlevel].rooms[you.room].pickups[i], pickupsize, you, tanksize) == 1:
                    if you.cangetpickup(levels[currentlevel].rooms[you.room].pickups[i].pickuptype):
                        you.getpickup(levels[currentlevel].rooms[you.room].pickups[i].pickuptype)
                        levels[currentlevel].rooms[you.room].pickups[i].dead = 1
                        ping.play(0)
                        
            for i in range(len(levels[currentlevel].rooms[you.room].pickups)):
                for j in range(len(levels[currentlevel].rooms[you.room].robots)):
                    if detect_collision(levels[currentlevel].rooms[you.room].pickups[i], pickupsize, levels[currentlevel].rooms[you.room].robots[j], tanksize) == 1:
                        if levels[currentlevel].rooms[you.room].robots[j].cangetpickup(levels[currentlevel].rooms[you.room].pickups[i].pickuptype):
                            levels[currentlevel].rooms[you.room].robots[j].getpickup(levels[currentlevel].rooms[you.room].pickups[i].pickuptype)
                            levels[currentlevel].rooms[you.room].pickups[i].dead = 1
                            ping.play(0)
            
            for i in range(len(levels[currentlevel].rooms[you.room].robots)):
                if detect_collision(levels[currentlevel].rooms[you.room].robots[i], tanksize, you, tanksize) == 1:
                    bounce(levels[currentlevel].rooms[you.room].robots[i], you)
                    clank.play(0)
                for j in range(len(levels[currentlevel].rooms[you.room].robots)):
                    if i != j:
                        if detect_collision(levels[currentlevel].rooms[you.room].robots[i], tanksize, levels[currentlevel].rooms[you.room].robots[j], tanksize) == 1:
                            bounce(levels[currentlevel].rooms[you.room].robots[i], levels[currentlevel].rooms[you.room].robots[j])
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
                                you.armor = maxarmor
                                you.fuel = maxfuel
                                you.ammo = maxammo
                                you.room = 0
                                background = pygame.image.load(levels[currentlevel].rooms[you.room].background).convert()
                                you.x = levels[currentlevel].playerx
                                you.y = levels[currentlevel].playery
                                you.rotate = levels[currentlevel].playerrotate
                                firstframe = 1
                                gameconsole.write('continuing after getting pwned')
                            elif event.key == K_n:
                                latersound.play(0)
                                pygame.time.wait(1500)
                                return (-2, shotsfired, shotslanded, pygame.time.get_ticks() - leveltimezero)
        for i in range(len(levels[currentlevel].rooms[you.room].robots)):
            if levels[currentlevel].rooms[you.room].robots[i].armor <=0:
                levels[currentlevel].rooms[you.room].robots[i].dead = 1
                gameconsole.write(levels[currentlevel].rooms[you.room].robots[i].name + ' died.')
        
        #and getting rid of the bodies
        if dropframe != 1:
            for i in range(len(levels[currentlevel].rooms[you.room].robots)):
                if i < len(levels[currentlevel].rooms[you.room].robots):
                    if levels[currentlevel].rooms[you.room].robots[i].dead == 1:
                        del levels[currentlevel].rooms[you.room].robots[i]
                        diesound.play(0)
                        
            for i in range(len(levels[currentlevel].rooms[you.room].bullets)):
                if i < len(levels[currentlevel].rooms[you.room].bullets):
                    if levels[currentlevel].rooms[you.room].bullets[i].dead == 1:
                        del levels[currentlevel].rooms[you.room].bullets[i]
                        
            for i in range(len(levels[currentlevel].rooms[you.room].pickups)):
                if i < len(levels[currentlevel].rooms[you.room].pickups):
                    if levels[currentlevel].rooms[you.room].pickups[i].dead ==1:
                        del levels[currentlevel].rooms[you.room].pickups[i]
        alldead = 1
        for i in range(len(levels[currentlevel].rooms)):
            if len(levels[currentlevel].rooms[i].robots) > 0:
                alldead = 0
        if alldead == 1:
            if currentlevel >= len(levels) - 1:
                print 'you beat the game.'
                return (-1, shotsfired, shotslanded, pygame.time.get_ticks() - leveltimezero)
            else:
                currentlevel += 1
                return (currentlevel, shotsfired, shotslanded, pygame.time.get_ticks() - leveltimezero)
                        
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
        #if (framedelay > 1) and (framedelay < 16):
            #pygame.time.wait(framedelay)
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
    levelfiles = ['levels/crisis']
    levels = []
    print 'loading level files...'
    for i in range(len(levelfiles)):
        protolevel = level()
        protolevel = protolevel.load(levelfiles[i])
        for j in range(len(protolevel.rooms)):
            print 'checking level ' + str(i + 1) + 'room ' + str(j) + '...'
            for k in range(len(protolevel.rooms[j].robots)):
                print 'loading robot ' + str(j) + '...'
                protolevel.rooms[j].robots[k].ammo = maxammo
                protolevel.rooms[j].robots[k].armor = maxarmor
                protolevel.rooms[j].robots[k].fuel = maxfuel
                protolevel.rooms[j].robots[k].gestating = 0
                protolevel.rooms[j].robots[k].hits = 0
                protolevel.rooms[j].robots[k].moveable = 1
            if len(protolevel.rooms[j].doors) < 0:
                print 'room #' + str(j) + ' has no doors.'
                raise SystemExit
        levels.append(protolevel)
    print 'Initializing pygame'
    pygame.init()
    print "Opening display 640x480 full-screen"
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('EvoTank')
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont('Terminal', 14)
    titlepic = pygame.image.load('images/title.png').convert()
    screen.blit(titlepic, (0,0))
    pygame.display.flip()
    pygame.mixer.music.load('sounds/title.ogg')
    pygame.mixer.music.play(-1)
    go = 0
    while go == 0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    go = 1
    
    currentlevel = 0
    while (currentlevel != -1) and (currentlevel != -2):
        currentlevel, shotsfired, shotslanded, time = mission(currentlevel, levels, screen)
        screen.blit(titlepic, (0,0))
        completepic = font.render('LEVEL COMPLETE', True, (255, 128, 0))
        if currentlevel == -2:
            completepic = font.render('YOU GOT PWNED', True, (255, 128, 0))
        shotsfiredpic = font.render('SHOTS FIRED: ' + str(shotsfired), True, (255, 128, 0))
        if shotsfired > 0:
            accuracypic = font.render('SHOTS LANDED: ' + str(shotslanded) + '(' + str(shotslanded * 100 / shotsfired) + '%)', True, (255, 128, 0))
        else:
            accuracypic = font.render('NO SHOTS FIRED', True, (255, 128, 0))
        levelseconds = time / 1000
        timesecs = levelseconds % 60
        timemins = (levelseconds - timesecs) / 60 
        if timesecs < 10:
           strsecs = '0' + str(timesecs)
        else:
           strsecs = str(timesecs)
        time = str(timemins) + ':' + strsecs
        timepic = font.render('TIME: ' + time, True, (255, 128, 0))
        screen.blit(completepic, (300, 20))
        screen.blit(shotsfiredpic, (300, 100))
        screen.blit(accuracypic, (300, 114))
        screen.blit(timepic, (300, 128))
        pygame.display.flip()
        pygame.mixer.music.load('sounds/endlevels.ogg')
        pygame.mixer.music.play(-1)
        go = 0
        signal.alarm(0)
        while go == 0:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        go = 1
    raise SystemExit

main()
