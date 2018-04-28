from random import random
from math import exp, sqrt
from lammps import lammps

class MolObject(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.score = 0.0
        self.eng = 0.0
        self.groupID = 0
        self.ffFile = ""
        self.coords = []
    
    #----------------------------------------------------
    def __str__(self):
        return '%s %s' %(self.score, self.eng)
    #----------------------------------------------------
    def setForcefield(self, filename):
        self.ffFile = str(filename)

    #----------------------------------------------------
    def Mutate(self):
        ranNum = random()
        if ranNum < 0.1:
            newObj = self.Mutate_SingleMove()
        else:
            newObj = self.Mutate_AllMove()
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
            dx = 0.01 * (2.0*random()-1.0)
            dy = 0.01 * (2.0*random()-1.0)
            dz = 0.01 * (2.0*random()-1.0)
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
        return self.seng

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
    def getffFile(self):
        return self.ffFile

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
    sim.command("create_box 2 box")
    coords = obj.getfeature()
    for atom in coords:
        sim.command("create_atoms %s single %s %s %s" % (tuple(atom))
    sim.command("read_data %s"%( obj.getffFile() ) )
#    sim.command("minimize 0.0 1.0e-8 1 1")
#    sim.command("minimize 0.0 1.0e-8 1000000 10000000")
    eng = PyLmps.eval("pe")
    val = exp(-eng/(1.987e-3*300))
    print val, eng

    return val, eng


