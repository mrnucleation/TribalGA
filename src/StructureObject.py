from random import random
from math import exp, sqrt
from lammps import lammps

class MolObject(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.score = 0.0
        self.eng = 0.0
        self.coords = []
    
    #----------------------------------------------------
    def __str__(self):
        return 'placeholder'
    #----------------------------------------------------
    def Mutate(self):
#        ranNum = random()
        newObj = self.Mutate_SingleMove()
        return newObj

    # ----------------------------------------------------
    def Mutate_SingleMove(self):
        from math import floor
        import copy
        nPart = len(self.coords)
        nSel = int(floor(random()*nPart))
        dx = 0.1*random()
        dy = 0.1*random()
        dz = 0.1*random()
        newCoords = copy.deepcopy(self.coords)
        newCoords[nSel][0] += dx
        newCoords[nSel][1] += dy
        newCoords[nSel][2] += dz
        newObj = MolObject()
        newObj.setfeature(newCoords=newCoords)
        newObj.computescore()
        return newObj

    # ----------------------------------------------------
    def Mutate_AllMove(self):
        from math import floor
        import copy
        newCoords = copy.deepcopy(self.coords)
        for i, atom in enumerate(newCoords):
            dx = 0.1 * random()
            dy = 0.1 * random()
            dz = 0.1 * random()
            newCoords[i][0] += dx
            newCoords[i][1] += dy
            newCoords[i][2] += dz
        newObj = MolObject()
        newObj.setfeature(newCoords=newCoords)
        newObj.computescore()
        return newObj
     #----------------------------------------------------
    def Mate(self, partner):
        return newObj

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
    def setfeature(self, newCoords):
        import copy
        self.coords = copy.deepcopy(newCoords)
    #----------------------------------------------------
#    def copyfeature(self, copyobj):
#        x,y,r = copyobj.getfeature()
#        self.setfeature(x=x, y=y)

   #----------------------------------------------------
    def getfeature(self):
        self.r = self.x**2 + self.y**2
        self.r = sqrt(self.r)
        return self.x, self.y, self.r
   #----------------------------------------------------
    def findgroup(self):
        groupID = floor(self.dr*self.r)/self.dr

        return groupID
   #----------------------------------------------------
#============================================================
def objFunc(obj):
    x, y, r = obj.getfeature()
#    r = x*x + y*y
#    r = sqrt(r)
    val = obj.degen*exp(-eng/10000.5)
    return val, eng


