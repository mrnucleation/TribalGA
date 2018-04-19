from random import random
from math import exp, sqrt
from lammps import lammps

class MolObject(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.score = 0.0
        self.eng = 0.0
        self.groupID = 0
        self.coords = []
    
    #----------------------------------------------------
    def __str__(self):
        return '%s %s' %(self.score, self.eng)
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
        dx = 0.1*(2.0*random()-1.0)
        dy = 0.1*(2.0*random()-1.0)
        dz = 0.1*(2.0*random()-1.0)
        newCoords = copy.deepcopy(self.coords)
        newCoords[nSel][1] += dx
        newCoords[nSel][2] += dy
        newCoords[nSel][3] += dz
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
            dx = 0.1 * (2.0*random()-1.0)
            dy = 0.1 * (2.0*random()-1.0)
            dz = 0.1 * (2.0*random()-1.0)
            newCoords[i][1] += dx
            newCoords[i][2] += dy
            newCoords[i][3] += dz
        newObj = MolObject()
        newObj.setfeature(newCoords=newCoords)
        newObj.computescore()
        return newObj
     #----------------------------------------------------
#    def Mate(self, partner):
#        return newObj

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
    def geteng(self):
        return self.score

    #----------------------------------------------------
    def setfeature(self, newCoords):
        self.coords = newCoords
    #----------------------------------------------------
    def copyfeature(self, copyobj):
        newCoords = copyobj.getfeature()
        self.setfeature(newCoords)
   #----------------------------------------------------
    def getfeature(self):
        return self.coords
   #----------------------------------------------------
    def findgroup(self):
        groupID = 0

        return groupID
   #----------------------------------------------------
#============================================================
def objFunc(obj):
    from lammps import PyLammps, lammps  
    sim = lammps()
    PyLmps = PyLammps(ptr=sim)
    sim.command("region box block -1000 -1000 -1000 1000 1000 1000")
    coords = obj.getfeature()
    for atom in coords:
        sim.command("create_atoms %s single %s %s %s" % (tuple(atom))
    result = PyLmps.eval("pe")





    return val, eng


