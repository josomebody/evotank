import pickle
doorsize = 32

class level:
    playerx = 0
    playery = 0
    playerrotate = 0
    music = 0
    rooms = []
    def __init__(self, level_file=0):
        self.rooms = []
        
    def save(self, level_file):
        f = open(level_file, 'w')
        pickle.dump(self, f)
        f.close
        
    def load(self, level_file):
        newlevel = level()
        f= open(level_file, 'r')
        newlevel = pickle.load(f)
        f.close
        return newlevel
    
class room:
    background = 0
    robots = []
    pickups = []
    obstacles = []
    doors = []
    bullets = []
    background = 0
    def __init__(self):
        self.playerx = 0
        self.playery = 0
        self.playerrotate = 0
        self.robots = []
        self.pickups = []
        self.obstacles = []
        self.doors = []
        self.bullets = []
        self.background = 0
    
class door:
    x = 0
    y = 0
    to_room = 0
    to_x = 0
    to_y = 0
    def teleport(self, object):
        object.room = self.to_room
        object.x = self.to_x
        object.y = self.to_y