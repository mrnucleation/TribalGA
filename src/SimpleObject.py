from random import random
from math import exp, sqrt

class RadialObj(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.x = 0.0
        self.y = 0.0
        self.r = 0.0
        self.dr = 70.0/7.0
        self.degen = 1.0
        self.score = 0.0
        self.eng = 0.0
        if initial:
            self.x = 7.0*random()
            self.y = 7.0*random()
            while self.x**2 + self.y**2 > 7.0**2:
                self.x = 7.0*(2.0*random()-1.0)
                self.y = 7.0*(2.0*random()-1.0)
            self.computescore()
            self.findgroup()
     
    #----------------------------------------------------
    def __str__(self):
        self.r = self.x**2 + self.y**2
        self.r = sqrt(self.r)
        return '%s, %s' % (self.r, self.eng)
    #----------------------------------------------------
    def Mutate(self):
        xn = 71.0
        yn = 71.0
        while xn**2 + yn**2 > 7.0**2:
            dx = 7.0*(2.0*random()-1.0)
            dy = 7.0*(2.0*random()-1.0)
            xn = self.x + dx
            yn = self.y + dy
        newObj = RadialObj()
        newObj.setfeature(x=xn, y=yn)
        newObj.computescore()
        return newObj
#        print newObj
     #----------------------------------------------------
    def Mate(self, partner):
        xp,yp = partner.getfeature()
        xn = 0.5*(self.x + xp)
        yn = 0.5*(self.y + yp)
        newObj = RadialObj()
        newObj.setfeature(x=xn, y=yn)
        newObj.computescore()
#        newObj.findgroup
        return newObj

    #----------------------------------------------------
    def fight(self, opponent):
        if self.score <= 0.0:
           loser = 1
           return
        if opponent.score <= 0.0:
           loser = 2
           return
        
        winprob = self.score/(opponent.score+self.score)
        if random() < winprob:
            loser = 2
        else:
            loser = 1
#        print winprob, loser
        return loser

    #----------------------------------------------------
    def setscore(self, score):
        self.score = score
    #----------------------------------------------------
    def getscore(self):
        return self.score
   #----------------------------------------------------
    def computescore(self):
        score, eng = objFunc(self)
        self.score = score
        self.eng = eng
    #----------------------------------------------------
    def geteng(self):
        return self.score
    #----------------------------------------------------
    def setfeature(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.r = self.x*self.x + self.y*self.y
        self.r = sqrt(self.r)
        self.computescore()
    #----------------------------------------------------
    def copyfeature(self, copyobj):
        x,y,r = copyobj.getfeature()
        self.setfeature(x=x, y=y)

    #----------------------------------------------------
    def safetycheck(self):
        return True
   #----------------------------------------------------
    def getfeature(self):
        self.r = self.x**2 + self.y**2
        self.r = sqrt(self.r)
        return self.x, self.y, self.r

   #----------------------------------------------------
    def addmember(self, mag=None):
        if mag is None:
            self.degen += 1.0
        else:
#            print self.degen
            self.degen += mag
#            print mag, self.degen

        if self.degen > 5000:
            self.degen = 5000
        self.computescore()
   #----------------------------------------------------
    def removemember(self, mag=None):
        if mag is None:
            self.degen -= 1.0
        else:
            self.degen -= mag
        self.computescore()
   #----------------------------------------------------
    def getmembers(self):
        return self.degen
   #----------------------------------------------------
    def degencheck(self):
        return self.degen
   #----------------------------------------------------
    def findgroup(self):
        from math import floor
#        dr = 50.0/7.0
        groupID = floor(self.dr*self.r)/self.dr

        return groupID

   #----------------------------------------------------
#============================================================
def objFunc(obj):
    x, y, r = obj.getfeature()
#    r = x*x + y*y
#    r = sqrt(r)
    eng = 20.0*((r-1.0)**2 * (r-5.0)**2 + 0.2*(r-1.0)**2)
    val = obj.degen*exp(-eng/10000.5)
    return val, eng


