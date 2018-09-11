from random import random
from math import exp, sqrt, floor
#from lammps import lammps

class MolObject(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.score = 0.0
        self.eng = 0.0
        self.groupID = 0
        self.ffFile = ""
        self.coords = []
        self.dr = 200.0/20.0
        self.r = 0.0
    
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
        import copy
        nPart = len(self.coords)
        nSel = int(floor(random()*nPart))
        dx = 2.5*(2.0*random()-1.0)
        dy = 2.5*(2.0*random()-1.0)
        dz = 2.5*(2.0*random()-1.0)
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
            dx = 2.5 * (2.0*random()-1.0)
            dy = 2.5 * (2.0*random()-1.0)
            dz = 2.5 * (2.0*random()-1.0)
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
    def safetycheck(self):
        if self.r < 5.0:
            if self.score > 0.0:
                return True
        else:
            return False

    #----------------------------------------------------
    def setscore(self, score):
        self.score = score
    #----------------------------------------------------
    def getscore(self):
        return self.score
   #----------------------------------------------------
    def computescore(self):
        rx = self.coords[0][1] - self.coords[1][1]    
        ry = self.coords[0][2] - self.coords[1][2]    
        rz = self.coords[0][3] - self.coords[1][3]    
        self.r = sqrt(rx*rx + ry*ry + rz*rz)

        score, eng = objFunc(self)
#        print score, eng
        self.score = score
        self.eng = eng
        return
    #----------------------------------------------------
    def geteng(self):
        return self.eng

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
        if self.r <= 0.0:
            rx = self.coords[0][1] - self.coords[1][1]    
            ry = self.coords[0][2] - self.coords[1][2]    
            rz = self.coords[0][3] - self.coords[1][3]    
            self.r = sqrt(rx*rx + ry*ry + rz*rz)
        groupID = floor(self.dr*self.r)/self.dr
#        if groupID < 4.0:
        return groupID
#        else:
#            return 5.0
   #----------------------------------------------------
#============================================================
def objFuncLammps(obj):
    from lammps import PyLammps, lammps  
    sim = lammps()
    PyLmps = PyLammps(ptr=sim)
    sim.command("atom_style atomic")
    sim.command("region box block -10 10 -10 10 -10 10")
    sim.command("boundary p p p")
    sim.command("create_box 1 box")
    sim.command("pair_style lj/cut 2.5")
    sim.command("pair_coeff * * 1.0 1.0 2.5")
    sim.command("mass 1 1.0")
    coords = obj.getfeature()
    for atom in coords:
        sim.command("create_atoms %s single %s %s %s" % (tuple(atom)))
#    sim.command("read_data %s"%( obj.getffFile() ) )
#    sim.command("minimize 0.0 1.0e-8 1000000 10000000")
    sim.command("run 0")
#    print "run 0"
#    PyLmps.run(1, "pre no post no")
    eng = PyLmps.eval("pe")
#    val = exp(-eng/(1.987e-3*300))
    val = exp(-2*eng)
    print( val, eng)
#    sim.command("quit ")
    return val, eng

#============================================================
def objFunc(obj):
    coords = obj.getfeature()
    rx = coords[0][1] - coords[1][1]
    ry = coords[0][2] - coords[1][2]
    rz = coords[0][3] - coords[1][3]
    rsq = rx*rx + ry*ry + rz*rz
    LJ = 1.0/rsq
    LJ = LJ*LJ*LJ
    eng = 4.0*LJ*(LJ-1.0)
    val = exp(-(eng+1.0)/0.3)
#    print eng, val
    return val, eng

