import signal
from classes import *

def breedingpit():
    random.seed()
    print 'Initializing pygame'
    pygame.init()
    robots = []
    pickups = []
    bullets = []
    protobullet = projectile()
    protobot = robot()
    you = player()
    thisgame = gamedetails()
    print "Loading config file..."
    configfile = open('config', 'r')
    thisgame = pickle.load(configfile)
    configfile.close
    if thisgame.numbots < 4:
        thisgame.numbots = 4
    print "Opening display 640x480 full-screen"
    screen = pygame.display.set_mode((640, 480), FULLSCREEN)
    pygame.display.set_caption('EvoTank')
    pygame.mouse.set_visible(False)
    gameconsole = console()

    print "Loading images..."
    font = pygame.font.SysFont("Terminal", 14)
    background = pygame.image.load('images/bg.png').convert()
    armorpic = pygame.image.load('images/armor.png').convert_alpha()
    ammopic = pygame.image.load('images/ammo.png').convert_alpha()
    fuelpic = pygame.image.load('images/fuel.png').convert_alpha()
    heattx = font.render('HEAT', True, (255, 255, 255))
    armortx = font.render('ARMOR', True, (255, 255, 255))
    fueltx = font.render('FUEL', True, (255, 255, 255))
    ammotx = font.render('AMMO', True, (255, 255, 255))
    throttlex = font.render('THROTTLE', True, (255, 255, 255))

    picname = 'images/bullet0.png'
    bulletpic = pygame.image.load(picname).convert_alpha()
    picname = 'images/goodtank0.png'
    goodtankpic = pygame.image.load(picname).convert_alpha()
    picname = 'images/badtank0.png'
    badtankpic = pygame.image.load(picname).convert_alpha()
    
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
    pygame.mixer.music.load('sounds/breedingpit.ogg')
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(-1)
    gameconsole.write("Building robots...")
    for i in range(thisgame.numbots):
        botpath = 'bot' + str(i)
        print botpath
        if os.path.exists(botpath):
            f = open(botpath, 'r')
            protobot = pickle.load(f)
        else:
            gameconsole.write('creating new bot')
            protobot.randomizedna()
            protobot.showdna()
            f = open(botpath, 'w')
            pickle.dump(protobot, f)
        protobot.dead = 0
        protobot.hitstilmating = 5
        protobot.state = 0
        protobot.armor = maxarmor
        protobot.fuel = maxfuel
        protobot.ammo = maxammo
        protobot.offspring = robot()
        robots.append(protobot)
        f.close
        print robots[i].name
        print "*********"
        robots[i].showdna()
        print "*********"
        
    #initialize game coordinates and shit
    ptypes = ['fuel', 'armor', 'ammo']
    for i in range(36):
        if len(pickups) < 36:
            protopickup = pickup()
            protopickup.x = random.randrange(640 - pickupsize)
            protopickup.y = random.randrange(480 - pickupsize)
            protopickup.pickuptype = ptypes[random.randrange(3)]
            pickups.append(protopickup)
                
    you.x = random.randrange(640 - tanksize)
    you.y = random.randrange(480 - tanksize)
    you.rotate = random.randrange(8)
    
    for i in range(len(robots)):
        robots[i].x = random.randrange(640 - tanksize)
        robots[i].y = random.randrange(480 - tanksize)
        robots[i].rotate = random.randrange(8)
        robots[i].hits = 0
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
        #generate new pickups
        if random.randrange(500) == 1:
            if len(pickups) < 32:
                protopickup = pickup()
                protopickup.x = random.randrange(640 - pickupsize)
                protopickup.y = random.randrange(480 - pickupsize)
                protopickup.pickuptype = ptypes[random.randrange(3)]
                gameconsole.write('spawning new pickup of type ' + protopickup.pickuptype)
                pickups.append(protopickup)

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
            console.write('frame dropped (' + str(frametime) + ')')
            gameconsole.blit(screen, font)
        else:
            screen.blit(background, (0, 0))
            for i in range(len(pickups)):
                if pickups[i].pickuptype == 'fuel':
                    screen.blit(fuelpic, (pickups[i].x, pickups[i].y))
                if pickups[i].pickuptype == 'ammo':
                    screen.blit(ammopic, (pickups[i].x, pickups[i].y))
                if pickups[i].pickuptype == 'armor':
                    screen.blit(armorpic, (pickups[i].x, pickups[i].y))
            for i in range(len(bullets)):
                drawable = pygame.transform.rotate(bulletpic, 0 - bullets[i].rotate * 45)
                screen.blit(drawable, (bullets[i].x, bullets[i].y))
            for i in range(len(robots)):
                drawable = pygame.transform.rotate(badtankpic, 0 - robots[i].rotate * 45)
                screen.blit(drawable, (robots[i].x, robots[i].y))
            drawable = pygame.transform.rotate(goodtankpic, 0 - you.rotate * 45)
            screen.blit(drawable, (you.x, you.y))
            del robotstats[:]
            del robotstatspic[:]
            for i in range(len(robots)):
                robotag = robots[i].name + ' '
                if robots[i].state == 10:
                    robotag = robotag + '(***mating w/ ' + robots[i].partner + '***)'
                if robots[i].state == 11:
                    robotag = robotag + '(***gestating***)'
                robotstats.append(robotag)
            for i in range(len(robotstats)):
                robotstatspic.append(font.render(robotstats[i], True, (255, 0, 0)))

            for i in range(len(robots)):
                screen.blit(robotstatspic[i], (robots[i].x, robots[i].y))
            if showconsole == 1:
                gameconsole.blit(screen, font)
            if showmeters == 1:
                pygame.draw.rect(screen, (64, 0, 0), (0, 470, you.heat / 20, 10))
                pygame.draw.rect(screen, (0, 0, 64), (210, 470, you.armor, 10))
                pygame.draw.rect(screen, (0, 64, 0), (320, 470, (you.fuel / 50), 10))
                pygame.draw.rect(screen, (32, 32, 64), (430, 470, you.ammo, 10))
                if you.velocity < -1:
                    pygame.draw.rect(screen, (64, 64, 0), (550, 470, 25, 10))
                if you.velocity < 0:
                    pygame.draw.rect(screen, (64, 64, 0), (575, 470, 25, 10))
                if you.velocity > 0:
                    pygame.draw.rect(screen, (64, 64, 0), (600, 470, 25, 10))
                if you.velocity > 1:
                    pygame.draw.rect(screen, (64, 64, 0), (625, 470, 25, 10))
                screen.blit(heattx, (0, 470))
                screen.blit(armortx, (210, 470))
                screen.blit(fueltx, (320, 470))
                screen.blit(ammotx, (430, 470))
                screen.blit(throttlex, (565, 470))
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
                    you.control(event.key, bullets, bang)
                else:
                    code_entry.append(event.key)
        for i in range(len(robots)):
            robots[i].letsgo(bullets, pickups, robots, you, bang, i)
        
        #move everybody
        if dropframe != 1:
            for i in range(len(bullets)):
                bullets[i].move()
            for i in range(len(robots)):
                robots[i].move()
        you.move() #if your machine is going too slow, you get bullet-time!
            
        #and now the expensive part: collision checks and shit
        if dropframe != 1:
            for i in range(len(bullets)):
                if bullets[i].offscreen() == 1:
                    bullets[i].dead = 1
            
            for i in range(len(bullets)):
                if (detect_collision(bullets[i], bulletsize, you, tanksize) == 1) and (bullets[i].originator != you.name):
                    you.armor = you.armor - 5
                    for j in range(len(robots)):
                        if bullets[i].originator == robots[j].name:
                            robots[j].hits = robots[j].hits + 1
                            robots[j].hitstilmating = robots[j].hitstilmating - 1
                            if robots[j].hitstilmating < 0:
                                robots[j].hitstilmating = 5
                            gameconsole.write((robots[j].name + ' scored hit #' + str(robots[j].hits)))
                    bullets[i].dead = 1
                    clank.play(0)
                    
            for i in range(len(bullets)):
                for j in range(len(robots)):
                    if (detect_collision(bullets[i], bulletsize, robots[j], tanksize) == 1) and (bullets[i].originator != robots[j].name):
                        robots[j].armor = robots[j].armor - 5
                        bullets[i].dead = 1
                        clank.play(0)
                        
            for i in range(len(pickups)):
                if detect_collision(pickups[i], pickupsize, you, tanksize) == 1:
                    if you.cangetpickup(pickups[i].pickuptype):
                        you.getpickup(pickups[i].pickuptype)
                        pickups[i].dead = 1
                        ping.play(0)
                        
            for i in range(len(pickups)):
                for j in range(len(robots)):
                    if detect_collision(pickups[i], pickupsize, robots[j], tanksize) == 1:
                        if robots[j].cangetpickup(pickups[i].pickuptype):
                            robots[j].getpickup(pickups[i].pickuptype)
                            pickups[i].dead = 1
                            ping.play(0)
            
            for i in range(len(robots)):
                if detect_collision(robots[i], tanksize, you, tanksize) == 1:
                    bounce(robots[i], you)
                    clank.play(0)
                for j in range(len(robots)):
                    if i != j:
                        if detect_collision(robots[i], tanksize, robots[j], tanksize) == 1:
                            bounce(robots[i], robots[j])
                            clank.play(0)
                        
        #and now for the sad part: coping with death
        if you.armor <= 0:
            diesound.play(0)
            #figure out which bot did the best
            scores = []
            for i in range(len(robots)):
                iscore = computescore(robots[i])
                scores.append(iscore)
            winner = 0
            for i in range(len(scores)):
                if scores[i] > scores[winner]:
                    winner = i
            gameconsole.write("SCORES:")
            for i in range(len(robots)):
                gameconsole.write(robots[i].name + ": " + str(scores[i]))
                
            gameconsole.write(robots[winner].name + " is the winner with a score of" + str(scores[winner]))
            for i in range(len(robots)):
                gameconsole.write('saving ' + robots[i].name + ' in file bot' + str(i))
                f = open('bot' + str(i), 'w')
                pickle.dump(robots[i], f)
                f.close
            thisgame.numbots = len(robots)
            gameconsole.write('saving configfile for ' + str(thisgame.numbots) + ' robots')
            configfile = open('config', 'w')
            pickle.dump(thisgame, configfile)
            configfile.close
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
        for i in range(len(robots)):
            if robots[i].armor <=0:
                robots[i].dead = 1
                gameconsole.write(robots[i].name + ' died.')
        if len(robots) == 1:
            gameconsole.write(robots[0].name + " is the only survivor with a score of " + str(computescore(robots[i])))
            robots[0].armor = maxarmor
            f = open('bot0', 'w')
            pickle.dump(robots[0], f)
            gameconsole.write('saving ' + robots[0].name + ' in file bot0')
            f.close
            protobot = robots[0]
            protobot.mutate()
            protobot.name = generatename()
            protobot.x = random.randrange(640 - tanksize)
            protobot.y = random.randrange(480 - tanksize)
            robots.append(protobot)
            f = open('bot1', 'w')
            pickle.dump(protobot, f)
            gameconsole.write('saving ' + protobot.name + ' in file bot1')
            f.close
            thisgame.numbots = 1
            gameconsole.write('saving configfile for ' + str(thisgame.numbots) + ' robots')
            configfile = open('config', 'w')
            pickle.dump(thisgame, configfile)
            configfile.close
            gameconsole.write('do you wanna start over? y/n')
            screen.blit(background, (0, 0))
            gameconsole.blit(screen, font)
            pygame.display.flip()
            choicekey = 0
            signal.alarm(0)
            while choicekey != K_y:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        choicekey = event.key
                        if event.key == K_y:
                            return 1
                        elif event.key == K_n:
                            latersound.play(0)
                            pygame.time.wait(1500)
                            return 0
        if len(robots) < 1: #if there's a mass extinction somehow, just don't propagate and this generation gets another chance.
            print "Mass extinction."
            return 0
        
        #and getting rid of the bodies
        if dropframe != 1:
            for i in range(len(robots)):
                if i < len(robots):
                    if robots[i].dead == 1:
                        del robots[i]
                        diesound.play(0)
                        
            for i in range(len(bullets)):
                if i < len(bullets):
                    if bullets[i].dead == 1:
                        del bullets[i]
                        
            for i in range(len(pickups)):
                if i < len(pickups):
                    if pickups[i].dead ==1:
                        del pickups[i]
                        
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
        startagain = breedingpit()
    raise SystemExit

main()