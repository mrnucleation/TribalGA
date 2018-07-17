from random import random
from math import exp, sqrt, floor, acos, atan2, pi, fabs
from scipy.special import sph_harm
from itertools import combinations
import copy
#from lammps import lammps

qNVal = 6
qconst = 4.0*pi/(2.0*qNVal+1.0)
class MolObject(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.score = 0.0
        self.eng = 0.0
        self.groupID = 0
        self.ffFile = ""
        self.coords = []
        self.dq = 100.0/1.0
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
        if ranNum < 0.5:
            newObj = self.Mutate_SingleMove()
        else:
            newObj = self.Mutate_AllMove()
        return newObj

    # ----------------------------------------------------
    def Mutate_SingleMove(self):
#        import copy
        nPart = len(self.coords)
        nSel = int(floor(random()*nPart))
        dx = 0.5*(2.0*random()-1.0)
        dy = 0.5*(2.0*random()-1.0)
        dz = 0.5*(2.0*random()-1.0)
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
#        import copy
        newCoords = copy.deepcopy(self.coords)
        for i, atom in enumerate(newCoords):
            dx = 0.5 * (2.0*random()-1.0)
            dy = 0.5 * (2.0*random()-1.0)
            dz = 0.5 * (2.0*random()-1.0)
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
#        for atom in self.coords:
#            if fabs(atom[1]) > 3.0:
#                return False
#            if fabs(atom[2]) > 3.0:
#                return False
#            if fabs(atom[3]) > 3.0:
#                return False
        for iObj, jObj in combinations(self.coords, 2):
            rx = iObj[1] - jObj[1]
            ry = iObj[2] - jObj[2]
            rz = iObj[3] - jObj[3]
            rsq = rx*rx + ry*ry + rz*rz
            if rsq < 1.0:
                return False

        cluster = clustercriteria(self)
        if not cluster:
            return False


        return True

    #----------------------------------------------------
    def setscore(self, score):
        self.score = score
    #----------------------------------------------------
    def getscore(self):
        return self.score
   #----------------------------------------------------
    def computescore(self):
#        rx = self.coords[0][1] - self.coords[1][1]    
#        ry = self.coords[0][2] - self.coords[1][2]    
#        rz = self.coords[0][3] - self.coords[1][3]    
#        r = sqrt(rx*rx + ry*ry + rz*rz)

        score, eng = objFunc(self)
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
#    def dumpfeature(self, outfile):


        

   #----------------------------------------------------
    def findgroup(self):
        nNei = 0
        qsum = []


        for m in range(0, 2*qNVal+1):
            qsum.append(complex(0.0, 0.0))

        for iObj, jObj in combinations(self.coords, 2):
            rx = jObj[1] - iObj[1]
            ry = jObj[2] - iObj[2]
            rz = jObj[3] - iObj[3]
            r = sqrt(rx*rx + ry*ry + rz*rz)
            if r < 1.5:
                nNei += 1
                phi = atan2(ry,rx)
                theta = acos(rz/r)   
                for m in range(0,2*qNVal+1):
                    q = sph_harm(m-qNVal, qNVal, phi, theta)
                    qsum[m] += q

        if nNei > 0:
            qtotal = 0.0
            for m in range(0, 2*qNVal+1):
                qtotal += qsum[m].real**2 + qsum[m].imag**2
            q = qtotal * qconst
            q = sqrt(q)/float(nNei)
        else: 
            q = 1.2
#        print q
        groupID = floor(self.dq*q)/self.dq
        return groupID
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
#    PyLmps.run(1, "pre no post no")
    eng = PyLmps.eval("pe")
#    val = exp(-eng/(1.987e-3*300))
    val = exp(-2*eng)
#    sim.command("quit ")
    return val, eng

#============================================================
def objFunc(obj):
    coords = obj.getfeature()
    eng = 0.0
    for iObj, jObj in combinations(coords, 2):
        rx = iObj[1] - jObj[1]
        ry = iObj[2] - jObj[2]
        rz = iObj[3] - jObj[3]
        rsq = rx*rx + ry*ry + rz*rz
        LJ = 1.0/rsq
        LJ = LJ*LJ*LJ
        eng += 4.0*LJ*(LJ-1.0)
    val = exp(-(eng+10.0)/0.3)
    return val, eng
#============================================================
def clustercriteria(obj):
    coords = obj.getfeature()
    topolist = []
    for item in coords:
        topolist.append([False for x in coords])

    for i, j in combinations(range(len(coords)), 2):
        rx = coords[i][1] - coords[j][1]
        ry = coords[i][2] - coords[j][2]
        rz = coords[i][3] - coords[j][3]
        rsq = rx*rx + ry*ry + rz*rz
        if rsq < 1.5**2:
            topolist[i][j] = True
            topolist[j][i] = True
#    for item in topolist:
#        print(item)
#    print
    nextlist = [0] 
    memberlist = [False for x in coords]
    memberlist[0] = True
    for item in coords:
        nextlist2 = []
        nNew = 0
        for obj in nextlist:
            for j, item in enumerate(coords):
                if not memberlist[j]:
                    if topolist[obj][j]:
                        nextlist2.append(j)
                        memberlist[j] = True
                        nNew += 1
        if nNew == 0:
            break
        nextlist = copy.copy(nextlist2)


    for member in memberlist:
        if not member:
#            print "Member List:", memberlist
            return False
    return True


