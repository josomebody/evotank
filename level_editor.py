import classes, pygame, os, pickle
from evotanklevels import *
from evotankclasses import *
from pygame.locals import *

#will display room on screen in real size
#mouse: left-click = add item, right-click = remove item
#keys: r = new room (will ask for background image file)
#          x = player starting point for new level (there can only be one, so the old one will be replaced)
#          t = tank (will ask for tank bot file and orientation 0-7, 0 being up, and rotating clockwise
#         p = will cycle through pickups in order armor, fuel, ammo
#         o = add obstacle
#         d = add door (will ask for new room number)
#         m = select music for level (will ask for sound file)
#         s = save current level
#         l = load level from a file
#         q = quit
#spacebar will turn music off and on once it's selected
def cursor(action):
    #return the appropriate image to display based on current action
    if action == K_p:
        return pickuppics[currentpickup]
    elif action == K_x:
        return playerpics[0]
    elif action == K_t:
        return tankpics[0]
    elif action == K_o:
        return obstaclepics[currentobstacle]
    elif action == K_d:
        return doorpics[0]
    elif action == K_w:
        return obstaclepics[2]
    elif action == 43:
        return obstaclepics[2]
    
def popup(msg):
    #simple popup dialog that prints a message, takes input up to a carriage return, and returns the input
    msgpic = font.render(msg, True, (255,255,255))
    #read in keyboard input until a return key, output as a string (this is gonna take a while)
    screen.blit(msgpic, (100,100))
    pygame.display.flip()
    output = []
    returnkeypressed = 0
    while returnkeypressed != 1:
        pygame.draw.rect(screen, (0,0,255), (100, 100, 200, 28))
        screen.blit(msgpic, (100,100))
        outputpic = font.render(listtostring(output), True, (255,255,255))
        screen.blit(outputpic, (100, 114))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if (event.key != K_RETURN) and (event.key != K_BACKSPACE):
                    output.append(keytostring[event.key])
                elif (event.key == K_BACKSPACE):
                    del output[len(output) - 1]
                elif (event.key == K_RETURN):
                    returnkeypressed = 1
    return listtostring(output)

def listtostring(input):
    output = ''
    for i in range(len(input)):
        output += input[i]
    return output

keytostring = {K_1:'1', K_2:'2', K_3:'3', K_4:'4', K_5:'5', K_6:'6', K_7:'7', K_8:'8', K_9:'9', K_0:'0', 
K_q:'q', K_w:'w', K_e:'e', K_r:'r', K_t:'t', K_y:'y', K_u:'u', K_i:'i', K_o:'o', K_p:'p', 
K_a:'a', K_s:'s', K_d:'d', K_f:'f', K_g:'g', K_h:'h', K_j:'j', K_k:'k', K_l:'l', 
K_z:'z', K_x:'x', K_c:'c', K_v:'v', K_b:'b', K_n:'n', K_m:'m', K_PERIOD:'.'}

def closest(objects, pos):
    #returns the index of closest object in objects to coordinate tuple pos
    x, y = pos
    theone = 0
    for i in range(len(objects)):
        if points_distance(objects[i].x, objects[i].y, x, y) < points_distance(objects[theone].x, objects[theone].y, x, y):
            theone = i
    return theone

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('EvoTank Level Editor')
pygame.mouse.set_visible(True)
font = pygame.font.SysFont("Terminal", 14)
tankpics = []
pickuppics = []
obstaclepics = []
playerpics = []
doorpics = []
scratch = 0
for i in range(8):
    scratch = pygame.image.load('images/badtank' + str(i) + '.png').convert_alpha()
    tankpics.append(scratch)
    scratch = pygame.image.load('images/goodtank' + str(i) + '.png').convert_alpha()
    playerpics.append(scratch)
for i in range(4):
    scratch = pygame.image.load('images/door' + str(i) + '.png').convert_alpha()
    doorpics.append(scratch)
scratch = pygame.image.load('images/armor.png').convert_alpha()
pickuppics.append(scratch)
scratch = pygame.image.load('images/fuel.png').convert_alpha()
pickuppics.append(scratch)
scratch = pygame.image.load('images/ammo.png').convert_alpha()
pickuppics.append(scratch)
scratch = pygame.image.load('images/barrel.png').convert_alpha()
obstaclepics.append(scratch)
scratch = pygame.image.load('images/crate.png').convert_alpha()
obstaclepics.append(scratch)
scratch = pygame.image.load('images/wall.png').convert_alpha()
obstaclepics.append(scratch)
musicpicked = 0
playmusic = 0
quit = 0
actions = [K_x, K_t, K_p, K_o, K_d, K_w]
currentaction = K_x
pickuptypes = ['armor', 'fuel', 'ammo']
currentpickup = 0
currentobstacle = 0
obstacletypes = ['barrel', 'crate', 'wall']
currentlevel = level()
currentroom = room()
currentroom.background = 'images/bg.png'
currentlevel.rooms.append(currentroom)
roomnum = 0
filename = ''
msg = font.render('EVOTANK LEVEL EDITOR', True, (255, 0,0))
background = pygame.image.load(currentlevel.rooms[roomnum].background).convert()
while quit == 0:
    if currentlevel.rooms[roomnum].background != 0:
        screen.blit(background, (0,0))
    for i in range(len(currentlevel.rooms[roomnum].doors)):
        screen.blit(doorpics[currentlevel.rooms[roomnum].doors[i].rotate], (currentlevel.rooms[roomnum].doors[i].x, currentlevel.rooms[roomnum].doors[i].y))
    for i in range(len(currentlevel.rooms[roomnum].pickups)):
        screen.blit(pickuppics[currentlevel.rooms[roomnum].pickups[i].pickuptypenum], (currentlevel.rooms[roomnum].pickups[i].x, currentlevel.rooms[roomnum].pickups[i].y))
    for i in range(len(currentlevel.rooms[roomnum].obstacles)):
        screen.blit(obstaclepics[currentlevel.rooms[roomnum].obstacles[i].obstacletypenum], (currentlevel.rooms[roomnum].obstacles[i].x, currentlevel.rooms[roomnum].obstacles[i].y))
    for i in range(len(currentlevel.rooms[roomnum].robots)):
        screen.blit(tankpics[currentlevel.rooms[roomnum].robots[i].rotate], (currentlevel.rooms[roomnum].robots[i].x,  currentlevel.rooms[roomnum].robots[i].y))
    if roomnum == 0:
        screen.blit(playerpics[currentlevel.playerrotate], (currentlevel.playerx, currentlevel.playery))
    screen.blit(msg, (0,0))
    coords = font.render(str(pygame.mouse.get_pos()), True, (255, 255, 255))
    screen.blit(coords, (586, 0))
    screen.blit(cursor(currentaction), (pygame.mouse.get_pos()))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                quit = 1
            elif event.key == K_UP:
                roomnum += 1
                if roomnum >= len(currentlevel.rooms):
                    roomnum = 0
                msg = font.render('room ' + str(roomnum), True, (255, 0,0))
                background = pygame.image.load(currentlevel.rooms[roomnum].background).convert()

            elif event.key == K_DOWN:
                roomnum -= 1
                if roomnum < 0:
                    roomnum = len(currentlevel.rooms) - 1
                msg = font.render('room ' + str(roomnum), True, (255, 0,0))
                background = pygame.image.load(currentlevel.rooms[roomnum].background).convert()

            elif actions.count(event.key) > 0:
                if event.key == K_p:
                    if currentaction == K_p:
                        currentpickup += 1
                        if currentpickup >= 3:
                            currentpickup = 0
                if event.key == K_o:
                    if currentaction == K_o:
                        currentobstacle += 1
                        if currentobstacle >= 3:
                            currentobstacle = 0
                if event.key == K_w:
                    vorh = popup('Enter \'v\' for a vertical wall, or \'h\' for a horizontal wall and press enter')
                    oldmsg = msg
                    msg = font.render('Click start of wall', True, (255, 0,0))
                currentaction = event.key

            elif event.key == K_b:
                currentlevel.rooms[roomnum].background = 'images/' + popup('Enter new background image filename.')
                background = pygame.image.load(currentlevel.rooms[roomnum].background).convert()
            elif event.key == K_m:
                currentlevel.music = 'sounds/' + popup('Enter music filename')
                pygame.mixer.music.load(currentlevel.music)
                playmusic = 1
            elif event.key == K_SPACE:
                if playmusic == 1:
                    if currentlevel.music != 0:
                        pygame.mixer.music.stop()
                    playmusic = 0
                else:
                    playmusic = 1
                    if currentlevel.music != 0:
                        pygame.mixer.music.play(-1)
            elif event.key == K_s:
                if filename == '':
                    filename = 'levels/' + popup('Enter filename to save')
                currentlevel.save(filename)
            elif event.key == K_a:
                filename = 'levels/' + popup('Enter filename to save')
            elif event.key == K_l:
                filename = 'levels/' + popup('Enter filename to load')
                currentlevel = currentlevel.load(filename)
                background = pygame.image.load(currentlevel.rooms[0].background).convert()
                roomnum = 0
                pygame.mixer.music.load(currentlevel.music)
            elif event.key == K_r:
                protoroom = room()
                protoroom.background = 'images/bg.png'
                currentlevel.rooms.append(protoroom)
                del protoroom
                roomnum += 1
                msg = font.render('room ' + str(roomnum), True, (255, 0,0))

    if (pygame.mouse.get_pressed() == (True, False, False)) and (checkforhold == 0):
        checkforhold = 1
        if currentaction == K_x:
            currentlevel.playerrotate = int(popup('Enter player start rotation(0-7)'))
            currentlevel.playerx, currentlevel.playery = pygame.mouse.get_pos()
            
        elif currentaction == K_t:
            f = open('savedbots/' + popup('Enter tank bot filename'), 'r')
            prototank = pickle.load(f)
            prototank.x, prototank.y = pygame.mouse.get_pos()
            prototank.rotate = int(popup('Enter tank rotation(0-7)'))
            currentlevel.rooms[roomnum].robots.append(prototank)
            
        elif currentaction == K_p:
            protopickup = pickup()
            protopickup.pickuptypenum = currentpickup
            protopickup.pickuptype = pickuptypes[currentpickup]
            protopickup.x, protopickup.y = pygame.mouse.get_pos()
            currentlevel.rooms[roomnum].pickups.append(protopickup)
            
        elif currentaction == K_o:
            protoobstacle = obstacle()
            protoobstacle.obstacletypenum = currentobstacle
            protoobstacle.obstacletype = obstacletypes[currentobstacle]
            protoobstacle.x, protoobstacle.y = pygame.mouse.get_pos()
            currentlevel.rooms[roomnum].obstacles.append(protoobstacle)
            
        elif currentaction == K_d:
            protodoor = door()            
            protodoor.x, protodoor.y = pygame.mouse.get_pos()
            protodoor.to_x, protodoor.to_y = protodoor.x, protodoor.y
            protodoor.rotate = int(popup('Enter wall number (0=N, 1=E, 2=S, 3=W)'))
            if protodoor.rotate == 0:
                protodoor.y = 0
                protodoor.to_y = 416
            if protodoor.rotate == 1:
                protodoor.x = 576
                protodoor.to_x = 0
            if protodoor.rotate == 2:
                protodoor.y = 416
                protodoor.to_y = 0
            if protodoor.rotate == 3:
                protodoor.x = 0
                protodoor.to_x = 576
            protodoor.to_room = int(popup('Enter destination room #'))
            currentlevel.rooms[roomnum].doors.append(protodoor)
            if len(currentlevel.rooms) >= protodoor.to_room:
                exitdoor = door()
                exitdoor.x = protodoor.to_x
                exitdoor.y = protodoor.to_y
                exitdoor.rotate = (protodoor.rotate + 2) % 4
                exitdoor.to_room = roomnum
                exitdoor.to_x = protodoor.x
                exitdoor.to_y = protodoor.y
                currentlevel.rooms[protodoor.to_room].doors.append(exitdoor)
                
        elif currentaction == K_w:
            wallstartx, wallstarty = pygame.mouse.get_pos()
            currentaction = 43
            msg = font.render('Click end of wall', True, (255, 0,0))
            
        elif currentaction == 43:
            wallendx, wallendy = pygame.mouse.get_pos()
            if vorh == 'v':
                walllength = (wallstarty - wallendy) / 64
                if walllength < 0:
                    delta = -64
                    wally = wallendy
                else:
                    delta = 64
                    wally = wallstarty
                wallx = wallstartx
                for i in range(abs(walllength)):
                    protowall = obstacle()
                    protowall.obstacletypenum = 2
                    protowall.x = wallx
                    protowall.y = wally
                    currentlevel.rooms[roomnum].obstacles.append(protowall)
                    print 'added wall section at ' + str((protowall.x, protowall.y))
                    wally += delta
            
            if vorh == 'h':
                walllength = (wallstartx - wallendx) / 64
                if walllength < 0:
                    delta = -64
                    wallx = wallendx
                else:
                    delta = 64
                    wallx = wallstartx
                wally = wallstarty
                for i in range(abs(walllength)):
                    protowall = obstacle()
                    protowall.obstacletypenum = 2
                    protowall.x = wallx
                    protowall.y = wally
                    currentlevel.rooms[roomnum].obstacles.append(protowall)
                    print 'added wall section at ' + str((protowall.x, protowall.y))
                    wallx += delta
            print 'added wall of length ' + str(walllength)
            msg = oldmsg
            
    elif (pygame.mouse.get_pressed() == (False, False, True)) and (checkforhold == 0):
        checkforhold = 1
        if currentaction == K_t:
            del currentlevel.rooms[roomnum].robots[closest(currentlevel.rooms[roomnum].robots, pygame.mouse.get_pos())]
        elif currentaction == K_p:
            del currentlevel.rooms[roomnum].pickups[closest(currentlevel.rooms[roomnum].pickups, pygame.mouse.get_pos())]
        elif currentaction == K_o:
            del currentlevel.rooms[roomnum].obstacles[closest(currentlevel.rooms[roomnum].obstacles, pygame.mouse.get_pos())]
        elif currentaction == K_d:
            del currentlevel.rooms[roomnum].doors[closest(currentlevel.rooms[roomnum].doors, pygame.mouse.get_pos())]
            
    if pygame.mouse.get_pressed() == (False, False, False):
        checkforhold = 0
                

