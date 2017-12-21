from random import *

Speed_Limit = 3
def randInt( low, high ):
    return random( )*( high - low ) + low

def dist( obj1, obj2 ):
    return pow(pow(obj1.x-obj2.x,2)+pow(obj1.y-obj2.y,2),0.5)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.r = 3
        self.display =[["/", "^", "\\"],
                       ["|", "O", "|"],
                       ["\\","_", "/" ]]
        
    def setLoc( self, x, y ):
        self.x = x
        self.y = y
        
    def move( self ):
        self.x += self.dx
        self.y += self.dy
        
    def accelerate(self, dx, dy):
        self.dx+=dx
        self.dy+=dy
        if self.dx > Speed_Limit:
            self.dx = Speed_Limit
        if self.dy > Speed_Limit:
            self.dy = Speed_Limit
        
class Ball:
    def __init__(self, x, y, game):
        self.display = [[" ", " ", " "],
                       [" ", "O", " "],
                       [" "," ", " " ]]
        self.game = game
        self.xspeed = 2
        self.x = x
        self.y = y
        self.dx=0
        self.dy=0
        self.r = 1

    def setLoc( self, x, y ):
        self.x = x
        self.y = y
        
    def move( self ):
        if( self.y >= self.game.size[1] or self.y <= 0 ):
            self.dy *= -1
        self.x += self.dx
        self.y += self.dy
        if( self.x > self.game.size[0] ):
            return 1
        if( self.x < 0 ):
            return -1
        return 0
        
    def smack( self, dx, dy ):
        self.dx = round( dx * self.xspeed )
        self.dy = round( dy * self.xspeed )
        
    def isTouching( self, obj ):
        d = dist( self, obj )
        if( d <= obj.r + self.r ):
            return True
        return False
    
class Game:
    def __init__( self, size ):
        self.size = size
        self.players = []
        for i in range(1,3):
            self.players.append(Paddle( int((self.size[0]/3) * i),
                                        int((self.size[1] + 1)/2)))
        self.ball = Ball( int(self.size[0]/2),
                          int(self.size[1]/2),
                          self)
    def reset( self ):
        for i in range(1,3):
            self.players[i-1].setLoc( int((self.size[0])/3 * i),
                                    int((self.size[1] + 1)/2))
            self.players[i-1].dx=0
            self.players[i-1].dy=0
        self.ball.setLoc( int(self.size[0]/2),
                          int(self.size[1]/2))
        self.ball.dx=0
        self.ball.dy=0
        return self.getState()

    #a: array of 4 integers for accelerations of pucks, 1 per player,
    #need values for ax and ay (acceleration x, y)
    def step( self, a ):
        done = False
        won = self.ball.move( )
        for p in range(2):
            self.players[p].move( )
            self.players[p].accelerate( a[p*2], a[p*2+1] )
        #collision detection and handling
        hits = self.checkHit( )
        if( len(hits) > 0 ):
            dx = 0
            dy = 0
            for i in hits:
                dx += i.dx
                dy += i.dy
            dx = int( dx/len(hits) )
            dy = int( dy/len(hits) )
            self.ball.smack( dx, dy )
        #reward handling
        if( won != 0 ):
            r = [ -1 * won, 1 * won]
            done = True
        else:
            r =[0,0]
        #returns 1D array - state,
        #1D-array with len of 2(1 for each player) - rewards,
        #and boolean if someone won or not. 
        return self.getState( ), r, done

    def getState( self ):
        s = [ self.ball.x, self.ball.y, self.ball.dx, self.ball.dy]
        for p in self.players:
            s.append( p.x )
            s.append( p.y )
            s.append( p.dx )
            s.append( p.dy )
        return s
            
    def checkHit( self ):
        ball = self.ball
        players = []
        for p in self.players:
            if( ball.isTouching( p ) ):
                players.append( p )
        return players

    def display( self ):
        S = ""
        objs = self.players.copy()
        objs.append(self.ball)
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                t=True
                for p in objs:
                    if(t and p.x >=0 and p.y >= 0 and x-p.x <= 1 and x-p.x >= -1 and y-p.y <= 1 and y-p.y >= -1):
                        S += p.display[ y - p.y + 1 ][x - p.x + 1]
                        t=False
                if t:
                    S += " "
                        
            S += "\n"
        print(S)
        
def test( ):
    g = Game( [100,30] )
    g.step( [-5, 0,
             -5, 0] )
    while True:
        p = input("step")
        a,b,c = g.step( [1,0,
                         1,0] )
        if(c):
            g.reset()
        g.display( )
test()
