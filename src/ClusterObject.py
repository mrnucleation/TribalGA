from random import random, randint
from math import exp, sqrt, floor, acos, atan2, pi, fabs
from scipy.special import sph_harm
from scipy.optimize import minimize
from itertools import combinations
import copy
#from lammps import lammps

temperature = 0.8
qNVal = 6
qconst = 4.0*pi/(2.0*qNVal+1.0)
class MolObject(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.score = 0.0
        self.eng = 0.0
        self.groupID = 0
        self.ID = 0
        self.ffFile = ""
        self.coords = []
        self.dq = 100.0/1.0
        self.r = 0.0
        self.objfunc = objFunc
    
    #----------------------------------------------------
    def __str__(self):
        return '%s %s' %(self.score, self.eng)
    #----------------------------------------------------
    def setForcefield(self, filename):
        self.ffFile = str(filename)

    #----------------------------------------------------
    def Mutate(self):
#        ranNum = random()
        newObj = self.Mutate_AllMove()
#        if ranNum < 0.5:
#            newObj = self.Mutate_SingleMove()
#        else:
#            newObj = self.Mutate_AllMove()
        return newObj

    # ----------------------------------------------------
    def Mutate_SingleMove(self):
#        import copy
        nPart = len(self.coords)
        nSel = int(floor(random()*nPart))
        dx = 1.5*(2.0*random()-1.0)
        dy = 1.5*(2.0*random()-1.0)
        dz = 1.5*(2.0*random()-1.0)
        newCoords = copy.deepcopy(self.coords)
        newCoords[nSel][1] += dx
        newCoords[nSel][2] += dy
        newCoords[nSel][3] += dz
        newObj = MolObject()
        newObj.setfeature(newCoords=newCoords)
        newObj.computescore()
#        if random() < 0.05:
#            newObj.optimize()
        return newObj

    # ----------------------------------------------------
    def Mutate_AllMove(self):
        from math import floor
#        import copy
        newCoords = copy.deepcopy(self.coords)
        newCoords[0][1] = 0.0
        newCoords[0][2] = 0.0
        newCoords[0][3] = 0.0

        for n, atom in enumerate(newCoords[1:]):
            i = n + 1
            loop = True
            while loop:
#                r = (1.5-1.0)*random()+1.0
                r = (random()*(1.5**3 - 1.0) + 1.0)**(1.0/3.0)
                dx, dy, dz = unitsphere()
                dx *= r
                dy *= r
                dz *= r
#                print dx, dy, dz
#                print i
                if i > 1:
                    growfrom = randint(0, i-1)
                else:
                    growfrom = 0
                newCoords[i][1] = newCoords[growfrom][1] + dx
                newCoords[i][2] = newCoords[growfrom][2] + dy
                newCoords[i][3] = newCoords[growfrom][3] + dz
                if i > 1:
                    for j, atom2 in enumerate(newCoords[0:i-2]):
                        rx = newCoords[i][1] - newCoords[j][1]
                        ry = newCoords[i][2] - newCoords[j][2]
                        rz = newCoords[i][3] - newCoords[j][3]
                        rsq = rx*rx + ry*ry + rz*rz
                        if rsq < 1.0:
#                            print i,j,rsq
                            break
                    else:
                        loop = False
                else:
                    loop = False
#            print "Success!"


        newObj = MolObject()
        newObj.setfeature(newCoords=newCoords)
        newObj.computescore()
#        if random() < 0.05:
#            newObj.optimize()
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
        topolist = []
        for item in self.coords:
            topolist.append([False for x in self.coords])

        for i, j in combinations(range(len(self.coords)), 2):
            rx = self.coords[i][1] - self.coords[j][1]
            ry = self.coords[i][2] - self.coords[j][2]
            rz = self.coords[i][3] - self.coords[j][3]
            rsq = rx*rx + ry*ry + rz*rz
            if rsq < 1.5**2:
                if rsq < 0.5**2:
                    return False
                topolist[i][j] = True
                topolist[j][i] = True
        cluster = clustercriteria(self, topolist)
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

        score, eng = self.objfunc(self)
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
    def setID(self, ID):
        self.ID = ID
    #----------------------------------------------------
    def getID(self):
        return self.ID 
    #----------------------------------------------------
    def radialscore(self):
        return self.score


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
        groupID = floor(self.dq*q)/self.dq
        return groupID
   #----------------------------------------------------
    def optimize(self, logfile=None):
#        x0 = self.coords
        if logfile != None:
            logfile.write("Optimizing object %s...\n"%(self.getID()))
        x0 = []
#        print("Initial Score: %s \n"%(self.score ))
        for item in self.coords:
            x0.append(item[1])
            x0.append(item[2])
            x0.append(item[3])

        def simplify(parIn, *args):
            tempcoords = []
            cnt = 0
            for x,y,z in grouper(3, parIn):
                tempcoords.append([self.coords[cnt][0], x, y, z])
                cnt += 1
            
            newObj = MolObject()
            newObj.setfeature(tempcoords)
            result = newObj.safetycheck()
            if result:
                scores, eng = self.objfunc(newObj)
                return -scores
            else:
                return 1e30
        results = minimize(simplify, x0=x0, method='Nelder-Mead', options={'maxiter':5000, 'adaptive':True} )
        finalcoords = []
        cnt = 0
        for x,y,z in grouper(3, results.x):
            finalcoords.append([self.coords[cnt][0], x, y, z])
            cnt += 1
        self.setfeature(finalcoords)
#        self.dumpfeature()
        self.computescore()
#        print("Final Score: %s \n"%(self.score))
        
  #----------------------------------------------------
    def dumpfeature(self):
        with open( "Object%s.xyz" % (self.ID), "w" ) as outfile: 
            outfile.write("%s \n"%(len(self.coords)))
            outfile.write("\n")
            for atom in self.coords:
                outlist = [str(x) for x in atom] + ["\n"]
                outfile.write(' '.join(outlist))

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
    val = exp(-eng/temperature)
    return val, eng
#============================================================
def clustercriteria(obj, topolist):
    coords = obj.getfeature()
#    topolist = []
#    for item in coords:
#        topolist.append([False for x in coords])

#    for i, j in combinations(range(len(coords)), 2):
#        rx = coords[i][1] - coords[j][1]
#        ry = coords[i][2] - coords[j][2]
#        rz = coords[i][3] - coords[j][3]
#        rsq = rx*rx + ry*ry + rz*rz
#        if rsq < 1.5**2:
#            topolist[i][j] = True
#            topolist[j][i] = True
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
#            for i, atom in enumerate(memberlist):
#                print i, atom

#            print "Neigh List:"
#            for i, row in enumerate(topolist):
#                for j, col in enumerate(row):
#                    if col:
#                        print i,j,col
#            quit()
            return False
    return True

#==================================================================
from itertools import izip_longest
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


#==================================================================
def unitsphere():
    u_12_sq = 2.0
    while u_12_sq >= 1.0:
        u1 = 2.0 * random() - 1.0
        u2 = 2.0 * random() - 1.0
        u_12_sq = u1 * u1 + u2 * u2
    x = 2.0 * u1 * sqrt(1.0 - u_12_sq)
    y = 2.0 * u2 * sqrt(1.0 - u_12_sq)
    z = (1.0 - 2.0 * u_12_sq)
    return x,y,z
  
#==================================================================

