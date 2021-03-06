import signal
from classes import *
states = ['search drone', 'lowarmor', 'lowfuel', 'lowammo', 'terminate']
def breedingpit():
    random.seed()
    print 'Initializing pygame'
    pygame.init()
    dropframe = 0
    framedelay = 0
    robots = []
    pickups = []
    bullets = []
    protobullet = projectile()
    protobot = robot()
    f = open('savedbots/trainer', 'r')
    you = pickle.load(f)
    f.close
    thisgame = gamedetails()
    print "Loading config file..."
    configfile = open('config', 'r')
    thisgame = pickle.load(configfile)
    configfile.close
    if thisgame.numbots < 4:
        thisgame.numbots = 4


    print "Building robots..."
    for i in range(thisgame.numbots):
        botpath = 'bot' + str(i)
        print botpath
        if os.path.exists(botpath):
            f = open(botpath, 'r')
            protobot = pickle.load(f)
        else:
            print 'creating new bot'
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
        protobot.x = random.randrange(640 - tanksize)
        protobot.y = random.randrange(480 - tanksize)
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
    bulletcount = 0
    lowfuelflag = 0
    lowammoflag = 0
    lowarmorflag = 0
    overheatflag = 0
        #main gameloop
    framestarttime = pygame.time.get_ticks()
    while 1:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)
        pygame.event.pump()
        #first of all, check for births
        for i in range(len(robots)):
               if robots[i].gestation == 1:
                robots.append(robots[i].givebirth())
        #generate new pickups
        if random.randrange(500) == 1:
            if len(pickups) < 32:
                protopickup = pickup()
                protopickup.x = random.randrange(640 - pickupsize)
                protopickup.y = random.randrange(480 - pickupsize)
                protopickup.pickuptype = ptypes[random.randrange(3)]
                pickups.append(protopickup)

        #everybody gets a turn
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    raise SystemExit
        you.letsgo(bullets, pickups, robots, robots[0], 0, 0)                    
        for i in range(len(robots)):
            robots[i].letsgo(bullets, pickups, robots, you, 0, i)
        
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
                    bullets[i].dead = 1
                    
            for i in range(len(bullets)):
                for j in range(len(robots)):
                    if (detect_collision(bullets[i], bulletsize, robots[j], tanksize) == 1) and (bullets[i].originator != robots[j].name):
                        robots[j].armor = robots[j].armor - 5
                        bullets[i].dead = 1
                        
            for i in range(len(pickups)):
                if detect_collision(pickups[i], pickupsize, you, tanksize) == 1:
                    if you.cangetpickup(pickups[i].pickuptype):
                        you.getpickup(pickups[i].pickuptype)
                        pickups[i].dead = 1
                        
            for i in range(len(pickups)):
                for j in range(len(robots)):
                    if detect_collision(pickups[i], pickupsize, robots[j], tanksize) == 1:
                        if robots[j].cangetpickup(pickups[i].pickuptype):
                            robots[j].getpickup(pickups[i].pickuptype)
                            pickups[i].dead = 1
            
            for i in range(len(robots)):
                if detect_collision(robots[i], tanksize, you, tanksize) == 1:
                    bounce(robots[i], you)
                for j in range(len(robots)):
                    if i != j:
                        if detect_collision(robots[i], tanksize, robots[j], tanksize) == 1:
                            bounce(robots[i], robots[j])
                        
        #and now for the sad part: coping with death
        if (you.armor <= 0) or (you.fuel <= 0):
            #figure out which bot did the best
            scores = []
            for i in range(len(robots)):
                iscore = computescore(robots[i])
                scores.append(iscore)
            winner = 0
            for i in range(len(scores)):
                if scores[i] > scores[winner]:
                    winner = i
            print "SCORES:"
            for i in range(len(robots)):
                print robots[i].name + ": " + str(scores[i])
                
            print robots[winner].name + " is the winner with a score of" + str(scores[winner])
            for i in range(len(robots)):
                print 'saving ' + robots[i].name + ' in file bot' + str(i)
                f = open('bot' + str(i), 'w')
                pickle.dump(robots[i], f)
                f.close
            thisgame.numbots = len(robots)
            print 'saving configfile for ' + str(thisgame.numbots) + ' robots'
            configfile = open('config', 'w')
            pickle.dump(thisgame, configfile)
            configfile.close
            print 'you got pwned.'
            signal.alarm(5)
            you.armor = 100
            you.fuel = maxfuel

        for i in range(len(robots)):
            if robots[i].armor <=0:
                robots[i].dead = 1
                print robots[i].name + ' died.'
        if len(robots) == 1:
            print robots[0].name + " is the only survivor with a score of " + str(computescore(robots[i]))
            robots[0].armor = maxarmor
            f = open('bot0', 'w')
            pickle.dump(robots[0], f)
            print 'saving ' + robots[0].name + ' in file bot0'
            f.close
            protobot = robots[0]
            protobot.mutate()
            protobot.name = generatename()
            protobot.x = random.randrange(640 - tanksize)
            protobot.y = random.randrange(480 - tanksize)
            robots.append(protobot)
            f = open('bot1', 'w')
            pickle.dump(protobot, f)
            print 'saving ' + protobot.name + ' in file bot1'
            f.close
            thisgame.numbots = 1
            print 'saving configfile for ' + str(thisgame.numbots) + ' robots'
            configfile = open('config', 'w')
            pickle.dump(thisgame, configfile)
            configfile.close
            signal.alarm(0)
            return 1
        if len(robots) < 1: #if there's a mass extinction somehow, just don't propagate and this generation gets another chance.
            print "Mass extinction."
            return 0
        
        #and getting rid of the bodies
        if dropframe != 1:
            for i in range(len(robots)):
                if i < len(robots):
                    if robots[i].dead == 1:
                        del robots[i]
                        
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
                lowarmorflag = 1
        else:
            lowarmorflag = 0
            
        if you.ammo < 10:
            if lowammoflag == 0:
                lowammoflag = 1
        else:
            lowammoflag = 0
            
        if you.fuel < 1000:
            if lowfuelflag == 0:
                lowfuelflag = 1
        else:
            lowfuelflag = 0
        if you.heat > 1000:
            if overheatflag == 0:
                overheatflag = 1
        elif you.heat < 950:
            overheatflag = 0
        
        #get the fps so we can act accordingly
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
