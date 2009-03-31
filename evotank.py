import random, os, shutil, math, pygame, pickle
from pygame.locals import *

#constants
maxfuel = 4000
maxammo = 100
maxarmor = 100
tanksize = 44
bulletsize = 16
pickupsize = 16

class gamedetails:
    numbots = 0

class console:
    consolepic = []
    def write(self, msg, font, screen):
        self.consolepic.append(font.render(msg, True, (128,64,0)))
    def blit(self, screen):
        for i in range(len(self.consolepic)):
            screen.blit(self.consolepic[i], (0, (i * 14)))
        if len(self.consolepic) > 3:
            del self.consolepic[0]
class pickup:
    dead = 0
    x = 0
    y = 0
    pickuptype = ''

class projectile:
    dead = 0
    x = 0
    y = 0
    rotate = 0
    velocity = 0
    originator = ''
    def move(self):
        if self.rotate == 0:
            self.y = self.y - self.velocity
        if self.rotate == 1:
            self.x = self.x + self.velocity
            self.y = self.y - self.velocity
        if self.rotate == 2:
            self.x = self.x + self.velocity
        if self.rotate == 3:
            self.x = self.x + self.velocity
            self.y = self.y + self.velocity
        if self.rotate == 4:
            self.y = self.y + self.velocity
        if self.rotate == 5:
            self.x = self.x - self.velocity
            self.y = self.y + self.velocity
        if self.rotate == 6:
            self.x = self.x - self.velocity
        if self.rotate == 7:
            self.x = self.x - self.velocity
            self.y = self.y - self.velocity

    def offscreen(self):
        if self.x < 0:
            return 1
        if self.x > 640:
            return 1
        if self.y < 0:
            return 1
        if self.y > 480:
            return 1
        return 0

class tank: #basic tank class, contains mechanical instructions and physical rules. decision-making code goes in child classes player and robot
    dead = 0
    x = 0
    y = 0
    rotation = 0 #0 = north, 1=northeast, 2=east, 3=southeast, 4=south, 5=southwest, 6=west, 7=northwest
    velocity = 0
    heat = 0
    armor = maxarmor
    ammo = maxammo
    fuel = maxfuel
    hitflag = 0

    def turn(self, dir): #-1 = left, 1=right
        self.rotate = self.rotate + dir
        if self.rotate == -1:
            self.rotate = 7
        if self.rotate == 8:
            self.rotate = 0

    def accel(self, delta):
        self.velocity = self.velocity + delta
        if self.velocity > 5:
            self.velocity = 5
        if self.velocity < -3:
            self.velocity = -3

    def cangetpickup(self, pickuptype):
        if pickuptype == "fuel":
            if self.fuel < maxfuel / 4:
                return 1
        if pickuptype == "armor":
            if self.armor < maxarmor:
                return 1
        if pickuptype == "ammo":
            if self.ammo < maxammo:
                return 1 
        return 0

    def getpickup (self, pickuptype):
        if self.cangetpickup(pickuptype) == 1:
            if pickuptype == "fuel":
                self.fuel = maxfuel
            if pickuptype == "armor":
                self.armor = maxarmor
            if pickuptype == "ammo":
                self.ammo = maxammo
            return 1
        return 0

    def shoot (self, bang):
        if self.heat > 2000:
            self.heat = 2000
        if self.heat > 1000:
            return -1
        if self.ammo > 0:
            self.ammo = self.ammo - 1
            self.heat = self.heat + 50
            bullet = projectile()
            bullet.rotate = self.rotate
            if self.rotate == 0:
                bullet.x = self.x + tanksize / 2
                bullet.y = self.y - bulletsize - 1
            if self.rotate == 1:
                bullet.x = self.x + tanksize + 1
                bullet.y = self.y - 1
            if self.rotate == 2:
                bullet.x = self.x + tanksize + 1
                bullet.y = self.y + tanksize / 2
            if self.rotate == 3:
                bullet.x = self.x + tanksize + 1
                bullet.y = self.y + tanksize + 1
            if self.rotate == 4:
                bullet.x = self.x + tanksize / 2 
                bullet.y = self.y + tanksize + 1 
            if self.rotate == 5:
                bullet.x = self.x - bulletsize - 1
                bullet.y = self.y + tanksize + 1
            if self.rotate == 6:
                bullet.x = self.x - bulletsize - 1
                bullet.y = self.y + tanksize / 2
            if self.rotate == 7:
                bullet.x = self.x - bulletsize - 1
                bullet.y = self.y - bulletsize - 1
            bullet.velocity = 8
            bullet.originator = self.name
            bang.play(0)
            return bullet
        else:
            return -1
        
    def move (self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > 640 - tanksize:
            self.x = 640 - tanksize
        if self.y > 480 - tanksize:
            self.y = 480 - tanksize
        self.heat = self.heat - 1
        if self.fuel <= 0:
            return
        if self.rotate == 0:
            self.y = self.y - self.velocity
        if self.rotate == 1:
            self.x = self.x + self.velocity
            self.y = self.y - self.velocity
        if self.rotate == 2:
            self.x = self.x + self.velocity
        if self.rotate == 3:
            self.x = self.x + self.velocity
            self.y = self.y + self.velocity
        if self.rotate == 4:
            self.y = self.y + self.velocity
        if self.rotate == 5:
            self.x = self.x - self.velocity
            self.y = self.y + self.velocity
        if self.rotate == 6:
            self.x = self.x - self.velocity
        if self.rotate == 7:
            self.x = self.x - self.velocity
            self.y = self.y - self.velocity
        self.fuel = self.fuel - math.fabs(self.velocity)

class player(tank):
    name = 'bitch'
    def control(self, action, bullets, bang):
        if action == K_UP:
            self.accel(1)
        if action == K_DOWN:
            self.accel(-1)
        if action == K_LEFT:
            self.turn(-1)
        if action == K_RIGHT:
            self.turn(1)
        if action == K_SPACE:
            newbullet = self.shoot(bang)
            if newbullet != -1:
                bullets.append(newbullet)

class robot(tank): #this is where the magic should be happening...
    name = ''
    hits = 0
    state = 0 #0=search drone, 1=low armor, 2=low fuel, 3=low ammo, 4=kill, tentatively. the bots will decide.
    op = 0 #0=nop, 1=turn right, 2=turn left, 3=accel, 4=decel, 5=target you, 6=target fuel, 7=target armor, 8=target ammo, 9=shoot
    ip = 0 #just the instruction pointer, should reset to 0 any time state changes
    minarmor = 0 #minimum before going into state 1
    minfuel = 0 #to go into state 2
    minammo = 0 #to go into state 3
    mindist = 0 #minimum distance between self and you to go into state kill, otherwise, search drone
    gestation = 0
    hitstilmating = 5
    partner = ''
 
    #to do: come up with a way to evolve priorities, until then, default to checking in order: armor, fuel, ammo, distance (could do a 16-possibilities thing,
    #but that's a lot of code to start, do it later)
    search = [0, 0, 0, 0, 0, 0, 0, 0]
    getarmor = [0, 0, 0, 0, 0, 0, 0, 0]
    getfuel = [0, 0, 0, 0, 0, 0, 0, 0]
    getammo = [0, 0, 0, 0, 0, 0, 0, 0]
    kill = [0, 0, 0, 0, 0, 0, 0, 0]
    def __init__(self):
        self.search = [0, 0, 0, 0, 0, 0, 0, 0]
        self.getarmor = [0, 0, 0, 0, 0, 0, 0, 0]
        self.getfuel = [0, 0, 0, 0, 0, 0, 0, 0]
        self.getammo = [0, 0, 0, 0, 0, 0, 0, 0]
        self.kill = [0, 0, 0, 0, 0, 0, 0, 0]
        self.name = generatename()
        self.hitstilmating = 5   
    def showdna(self):
        print "STATE THRESHOLDS"
        print "armor: " + str(self.minarmor)
        print "fuel: " + str(self.minfuel)
        print "ammo: " + str(self.minammo)
        print "attack range: " + str(self.mindist)
        print "STATE CODE"
        print "=========="
        print "search drone: "
        print self.search
        print "retreat:"
        print self.getarmor
        print "economy mode:"
        print self.getfuel
        print "ammo forage:"
        print self.getammo
        print "terminate"
        print self.kill
        
    def getstate(self, you): #this would be so much fucking easier in lisp
        if (self.state != 10) and (self.state != 11):
            if self.hitstilmating == 0:
                self.hitstilmating = 5
                return 10
        if self.state == 10:
            return 10
        elif self.state == 11:
            return 11
        elif self.gestation > 0:
            return 11
        elif self.armor < self.minarmor:
            return 1
        elif self.fuel < self.minfuel:
            return 2
        elif self.ammo < self.minammo:
            return 3
        elif distance(self, you) < self.mindist:
            return 4
        else:
            return 0

    def sexecute(self, bullets, pickups, you, bang): #reads current op and runs it
        if self.op == 0:
            return
        if self.op == 1:
            self.turn(1)
        if self.op == 2:
            self.turn(-1)
        if self.op == 3:
            self.accel(1)
        if self.op == 4:
            self.accel(-1)
        if self.op == 5: #these need some serious thinking about
            self.target(you)
        if self.op == 6:
            getit = nearestpickup(self, "fuel", pickups)
            if getit != -1:
                self.target(pickups[getit])
        if self.op == 7:
            getit = nearestpickup(self, "armor", pickups)
            if getit != -1:
                self.target(pickups[getit])
        if self.op == 8:
            getit = nearestpickup(self, "ammo", pickups)
            if getit != -1:
                self.target(pickups[getit])
        if self.op == 9: 
            newbullet = self.shoot(bang)
            if newbullet != -1:
                bullets.append(newbullet)

    def target(self, object): #returns -1 if to the left, 1 if to the right, 0 if dead on. this would be a serious hell of a lot easier in radians instead of 8-d.
        direction = self.rotate
        if (object.x == self.x) and (object.y < self.y):
            direction = 0
        if (object.x > self.x) and (object.y < self.y):
            direction = 1
        if (object.x > self.x) and (object.y == self.y):
            direction = 2
        if (object.x > self.x) and (object.y > self.y):
            direction = 3
        if (object.x == self.x) and (object.y > self.y):
            direction = 4
        if (object.x < self.x) and (object.y > self.y):
            direction = 5
        if (object.x < self.x) and (object.y == self.y):
            direction = 6
        if (object.x < self.x) and (object.y < self.y):
            direction = 7
        self.rotate = direction
        return 
                
    def letsgo(self, bullets, pickups, robots, you, bang, i): #the code to actually run the damned thing after all that. 
        #figure out what state we should be in
        newstate = self.getstate(you)
        if newstate != self.state:
            self.ip = 0
            self.state = newstate
        #check for ip overflow and reset if needed
        if self.ip > 7:
            self.ip = 0
        #run from the right state code buffer
        if self.state == 0:
            self.op = self.search[self.ip]
        if self.state == 1:
            self.op = self.getarmor[self.ip]
        if self.state == 2:
            self.op = self.getfuel[self.ip]
        if self.state == 3:
            self.op = self.getammo[self.ip]
        if self.state == 4:
            self.op = self.kill[self.ip]
        if self.state == 10: 
        #get freakah
            self.fuck(robots[bestof(robots, i)])
            return
        if self.state == 11:
            self.gestate(you)
            return
        #run the opcode
        self.sexecute(bullets, pickups, you, bang)
        self.ip = self.ip + 1

    def randomizedna (self): #to be used in generation of completely new bots
        self.name = generatename()
        self.minarmor = random.randrange(100)
        self.minfuel = random.randrange(10000)
        self.minammo = random.randrange(100)
        self.mindist = random.randrange(423) #this is the biggest integer distance on 640x480 grid
        for i in range(8):
            self.search[i] = random.randrange(10)
            self.getarmor[i] = random.randrange(10)
            self.getfuel[i] = random.randrange(10)
            self.getammo[i] = random.randrange(10)
            self.kill[i] = random.randrange(10)
            
    def mutate (self): #for propagation
        self.name = generatename() 
        thresholdmuts = random.randrange(4)
        for i in range(thresholdmuts):
            pick = random.randrange(4)
            if pick == 0:
                self.minarmor = self.armor + random.randrange(20) - 10
                if self.minarmor < 0:
                    self.minarmor = 0
                if self.minarmor > 100:
                    self.minarmor = 100
            if pick == 1:
                self.minfuel = self.minfuel + random.randrange(200) - 100
                if self.minfuel < 0:
                    self.minfuel = 0
                if self.minfuel > 10000:
                    self.minfuel = 10000
            if pick == 2:
                self.minammo = self.minammo + random.randrange(20) - 10
                if self.minammo < 0:
                    self.minammo = 0
                if self.minammo > 100:
                    self.minammo = 100
            if pick == 3:
                self.mindist = self.mindist + random.randrange(32) - 16
                if self.mindist < 0:
                    self.mindist = 0
                if self.mindist > 423:
                    self.mindist = 423
        i = random.randrange(8)
        v = random.randrange(10)
        pick = random.randrange(5)
        if pick == 0:
            self.search[i] = v
        if pick == 1:
            self.getarmor[i] = v
        if pick == 2:
            self.getfuel[i] = v
        if pick == 3:
            self.getammo[i] = v
        if pick == 4:
            self.kill[i] = v
            
    def fuck(self, luckyguy):
        self.partner = luckyguy.name
        self.target(luckyguy)
        if self.velocity < 1:
            self.accel(1)
        self.fuel = maxfuel
        if distance(self,  luckyguy) < tanksize * 2:
            self.armor = 100
            luckyguy.armor = 100
            self.offspring = dnamingle(self, luckyguy)
            self.state = 11
            self.gestation = 250
            self.hitstilmating = 5
            print self.name + ' has successfully mated with ' + luckyguy.name
        
    def gestate(self, you):
        self.gestation = self.gestation - 1
        self.target(you)
        self.accel(-1)
        self.fuel = maxfuel
        if self.gestation == 1:
            self.state = 0
            
    def givebirth(self):
        self.gestation = 0
        self.offspring.x = self.x
        self.offspring.y = self.y
        self.offspring.armor = maxarmor
        self.offspring.ammo = maxammo
        self.offspring.fuel = maxfuel
        self.offspring.rotate = self.rotate
        self.offspring.velocity = 0
        self.offspring.state = 0
        self.offspring.hits = 0
        self.offspring.name = generatename()
        print self.name + ' has given birth to ' + self.offspring.name
        return self.offspring
    
def bestof(robots, i):
    luckyguy = 0
    if i == 0:
        if len(robots) > 1:
            luckyguy = 1
    for j in range(len(robots)):
        if j != i:
            if computescore(robots[j]) > computescore(robots[luckyguy]):
                luckyguy = j
    return luckyguy

def dnamingle(mom, dad):
    offspring = robot()
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.minarmor = dad.minarmor
    else:
        offspring.minarmor = mom.minarmor
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.minfuel = dad.minfuel
    else:
        offspring.minfuel = mom.minfuel
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.minammo = dad.minammo
    else:
        offspring.minammo = mom.minammo
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.mindist = dad.mindist
    else:
        offspring.mindist = mom.mindist
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.search = dad.search
    else:
        offspring.search = mom.search
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.getarmor = dad.getarmor
    else:
        offspring.getarmor = mom.getarmor
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.getfuel = dad.getfuel
    else:
        offspring.getfuel = mom.getfuel
    mendel = random.randrange(2)
    if mendel == 1:
        offspring.kill = dad.kill
    else:
        offspring.kill = mom.kill
    
    powerplant = random.randrange(10)
    if powerplant == 1:
        offspring.mutate()
    return offspring
    
            
def detect_collision(guy1, guy1_size, guy2, guy2_size): #simple collision detection for two square guys side guyx_size
    if guy1.y + guy1_size > guy2.y:
        if guy1.y < guy2.y + guy2_size:
            if guy1.x + guy1_size > guy2.x:
                if guy1.x < guy2.x + guy2_size:
                    return 1
    if guy1.x + guy1_size > guy2.x:
        if guy1.x < guy2.x + guy2_size:
            if guy1.y + guy1_size > guy2.y:
                if guy1.y < guy2.y + guy2_size:
                    return 1
    return 0

def distance(guy1, guy2): #find distance between two objects using pythagorean theorem
    return math.sqrt(math.pow(math.fabs(guy1.x - guy2.x), 2) + math.pow(math.fabs(guy1.y - guy2.y), 2))

def nearestpickup(guy, type, pickups):
    righttype = []
    for j in range(len(pickups)): #make a list of pickup indexes with the right type
        if pickups[j].pickuptype == type:
            righttype.append(j)
    theone = 0
    if len(righttype) > 0:
        for j in righttype: #search through that index for the closest one
            if distance(guy, pickups[j]) < distance(guy, pickups[theone]):
                theone = j
    else:
         theone = -1
    return theone

def bounce(guy1, guy2):
    if guy1.x > guy2.x:
        guy1.x = guy1.x + tanksize / 2
        guy2.x = guy2.x - tanksize / 2
    else:
        guy1.x = guy1.x - tanksize / 2
        guy2.x = guy2.x + tanksize / 2
    if guy1.y > guy2.y:
        guy1.y = guy1.y + tanksize / 2
        guy2.y = guy2.y - tanksize / 2
    else:
        guy1.y = guy1.y - tanksize / 2
        guy2.y = guy2.y + tanksize / 2
    guy1.armor = guy1.armor - math.fabs(guy2.velocity)
    guy2.armor = guy2.armor - math.fabs(guy1.velocity)
    guy1.velocity = 0
    guy2.velocity = 0
    
def generatename():
    consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    consclusters = ['CH', 'PH', 'SH', 'TH', 'CK', 'LM', 'BR', 'CR', 'DR', 'FR', 'GR', 'KR', 'PR', 'TR', 'PS', 'RS', 'SS', 'TS', 'CT', 'KT', 'PT', 'RT', 'ST']
    vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
    dipthongs = ['AE', 'AI', 'AU', 'AY', 'EA', 'EE', 'EI', 'EU', 'EY', 'IA', 'IE', 'IO', 'IY', 'OE', 'OI', 'OY', 'UY']
    length = random.randrange(1) + 1
    constart = random.randrange(2)
    name = []
    if constart == 1:
        vd = random.randrange(2)
        if vd == 1:
            name.append(consclusters[random.randrange(len(consclusters))])
        else:
            name.append(consonants[random.randrange(len(consonants))])
    for i in range(length):
        vd = random.randrange(2)
        if vd == 1:
            name.append(vowels[random.randrange(len(vowels))])
        else:
            name.append(dipthongs[random.randrange(len(dipthongs))])
        vd = random.randrange(2)
        if vd == 1:
            name.append(consclusters[random.randrange(len(consclusters))])
        else:
            name.append(consonants[random.randrange(len(consonants))])
    ev = random.randrange(2)
    if ev == 1:
        vd = random.randrange(2)
        if vd == 1:
            name.append(vowels[random.randrange(len(vowels))])
        else:
            name.append(dipthongs[random.randrange(len(dipthongs))])
    namestring = ''
    for i in name:
        namestring = namestring + i
    return namestring

def computescore(guy):
    score = math.floor(guy.hits * 100 + guy.armor * 5 + guy.fuel / 100 + guy.ammo)
    return score

def main():
    print 'Running main'
    random.seed()
    print 'Initializing pygame'
    pygame.init()
    print 'building objects...'
    print 'robots'
    robots = []
    print 'pickups'
    pickups = []
    print 'bullets'
    bullets = []
    print 'bullet loader'
    protobullet = projectile()
    print 'robot loader'
    protobot = robot()
    print 'player loader'
    you = player()
    print 'game loader'
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
    background = pygame.image.load('bg.png').convert()
    armorpic = pygame.image.load('armor.png').convert_alpha()
    ammopic = pygame.image.load('ammo.png').convert_alpha()
    fuelpic = pygame.image.load('fuel.png').convert_alpha()
    heattx = font.render('HEAT', True, (255, 255, 255))
    armortx = font.render('ARMOR', True, (255, 255, 255))
    fueltx = font.render('FUEL', True, (255, 255, 255))
    ammotx = font.render('AMMO', True, (255, 255, 255))
    throttlex = font.render('THROTTLE', True, (255, 255, 255))

    bulletpic = []
    goodtankpic = []
    badtankpic = []
    for i in range(8):
        picname = 'bullet' + str(i) + '.png'
        tempic = pygame.image.load(picname).convert_alpha()
        bulletpic.append(tempic)
        picname = 'goodtank' + str(i) + '.png'
        tempic = pygame.image.load(picname).convert_alpha()
        goodtankpic.append(tempic)
        picname = 'badtank' + str(i) + '.png'
        tempic = pygame.image.load(picname).convert_alpha()
        badtankpic.append(tempic)
    
    gameconsole.write("Loading sounds...", font, screen)
    bang = pygame.mixer.Sound('bang.wav')
    clank = pygame.mixer.Sound('clank.wav')
    ping = pygame.mixer.Sound('ping.wav')
    diesound = pygame.mixer.Sound('die.wav')
    lowammosound = pygame.mixer.Sound('ammo.wav')
    lowarmorsound = pygame.mixer.Sound('armor.wav')
    lowfuelsound = pygame.mixer.Sound('fuel.wav')
    pygame.mixer.music.load('music.ogg')
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(-1)
    while 1:
        gameconsole.write("Building robots...", font, screen)
        for i in range(thisgame.numbots):
            botpath = 'bot' + str(i)
            print botpath
            if os.path.exists(botpath):
                f = open(botpath, 'r')
                protobot = pickle.load(f)
            else:
                gameconsole.write('creating new bot', font, screen)
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
            protopickup = pickup()
            protopickup.x = random.randrange(640 - pickupsize)
            protopickup.y = random.randrange(480 - pickupsize)
            protopickup.pickuptype = ptypes[random.randrange(3)]
            pickups.append(protopickup)
                    
        you.x = random.randrange(640 - tanksize)
        you.y = random.randrange(480 - tanksize)
        you.rotate = random.randrange(8)
        
        for i in range(thisgame.numbots):
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
     
        startagain = 0
        #main gameloop
        while startagain == 0:
            #first of all, check for births
            for i in range(len(robots)):
                if robots[i].gestation == 1:
                    robots.append(robots[i].givebirth())
                    gameconsole.write(robots[i].name + ' has given birth to ' + robots[len(robots) - 1].name, font, screen)
            if random.randrange(500) == 1:
                protopickup = pickup()
                protopickup.x = random.randrange(640 - pickupsize)
                protopickup.y = random.randrange(480 - pickupsize)
                protopickup.pickuptype = ptypes[random.randrange(3)]
                gameconsole.write('spawning new pickup of type ' + protopickup.pickuptype, font, screen)
                pickups.append(protopickup)

            #draw everybody
            screen.blit(background, (0, 0))
            for i in range(len(pickups)):
                if pickups[i].pickuptype == 'fuel':
                    screen.blit(fuelpic, (pickups[i].x, pickups[i].y))
                if pickups[i].pickuptype == 'ammo':
                    screen.blit(ammopic, (pickups[i].x, pickups[i].y))
                if pickups[i].pickuptype == 'armor':
                    screen.blit(armorpic, (pickups[i].x, pickups[i].y))
            for i in range(len(robots)):
                screen.blit(badtankpic[robots[i].rotate], (robots[i].x, robots[i].y))
            screen.blit(goodtankpic[you.rotate], (you.x, you.y))
            for i in range(len(bullets)):
                screen.blit(bulletpic[bullets[i].rotate], (bullets[i].x, bullets[i].y))
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
            gameconsole.blit(screen)
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
            pygame.display.flip()
            
            #everybody gets a turn
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        you.armor = 0
                    else:
                        you.control(event.key, bullets, bang)
            for i in range(len(robots)):
                robots[i].letsgo(bullets, pickups, robots, you, bang, i)
            
            #move everybody
            for i in range(len(bullets)):
                bullets[i].move()
            for i in range(len(robots)):
                robots[i].move()
            you.move()
                
            #and now the expensive part: collision checks and shit
            for i in range(len(bullets)):
                if bullets[i].offscreen() == 1:
                    bullets[i].dead = 1
            
            for i in range(len(bullets)):
                if detect_collision(bullets[i], bulletsize, you, tanksize) == 1:
                    you.armor = you.armor - 5
                    for j in range(len(robots)):
                        if bullets[i].originator == robots[j].name:
                            robots[j].hits = robots[j].hits + 1
                            robots[j].hitstilmating = robots[j].hitstilmating - 1
                            if robots[j].hitstilmating < 0:
                                robots[j].hitstilmating = 5
                            gameconsole.write((robots[j].name + ' scored hit #' + str(robots[j].hits)), font, screen)
                    bullets[i].dead = 1
                    clank.play(0)
                    
            for i in range(len(bullets)):
                for j in range(len(robots)):
                    if detect_collision(bullets[i], bulletsize, robots[j], tanksize) == 1:
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
                screen.blit(background,(0,0))
                gameconsole.write('you got pwned. continue? y/N', font, screen)
                gameconsole.blit(screen)
                pygame.display.flip()
                pygame.time.wait(1000)
                choicekey = 0
                while choicekey != K_y:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                                choicekey = event.key
                                if event.key == K_y:
                                    you.armor = 100
                                    gameconsole.write('continuing after getting pwned', font, screen)
                                elif event.key == K_n:
                                    raise SystemExit
            for i in range(len(robots)):
                if robots[i].armor <=0:
                    robots[i].dead = 1
                    gameconsole.write(robots[i].name + ' died.', font, screen)
            if len(robots) == 1:
                gameconsole.write(robots[0].name + " is the only survivor with a score of " + str(computescore(robots[i])), font, screen)
                f = open('bot' + str(i), 'w')
                pickle.dump(robots[0], f)
                f.close
                thisgame.numbots = len(robots)
                gameconsole.write('saving configfile for ' + str(thisgame.numbots) + ' robots', font, screen)
                configfile = open('config', 'w')
                pickle.dump(thisgame, configfile)
                configfile.close
                gameconsole.write('do you wanna start over? y/n', font, screen)
                screen.blit(background, (0, 0))
                gameconsole.blit(screen)
                pygame.display.flip()
                pygame.time.wait(1000)
                choicekey = 0
                while choicekey != K_y:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            choicekey = event.key
                            if event.key == K_y:
                                startagain = 1
                            elif event.key == K_n:
                                raise SystemExit
            if len(robots) < 1: #if there's a mass extinction somehow, just don't propagate and this generation gets another chance.
                print "Mass extinction."
                raise SystemExit
            
            #and getting rid of the bodies
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
                    
main()