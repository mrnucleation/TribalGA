from random import random, gauss
from math import exp, sqrt, floor, fabs, log
from MultiObjPoolClass import ObjectiveMismatch
from scipy.optimize import minimize
import copy

#class ObjectiveMismatch(Exception):
#    pass

class LatticeObject(object):
    #----------------------------------------------------
    def __init__(self, initial=False, nLat=1, nObj=1, nTypes=2):
        self.ID = 0
        self.nPara = nParameters
        self.nObj = nObj
        self.scores = []

        self.lattice = ''.join(['1' for x in range(nLat)])
        self.maxatoms = []
        self.objFunc = trialObj
        self.safetyFunc = []
   
    #----------------------------------------------------
    def __str__(self):
        return ' '.join([str(x) for x in self.parameters])
    #----------------------------------------------------
    def Mutate(self):
#        ranNum = random()
#        if ranNum < 0.5:
#            newObj = self.Mutate_SmallAllMove()
        newObj.setobjective(self.objFunc)
        return newObj
    # ----------------------------------------------------
    def Mutate_SmallMove(self):
        nPar = len(self.parameters)
        nSel = int(floor(random()*nPar)-1)
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        sigma = parRange/4.0
        while True:
#            dPar = parRange*(2.0*random()-1.0)
            dPar = gauss(0.0, sigma)
            if (self.parameters[nSel]+dPar <= self.pmax[nSel]) and (self.parameters[nSel]+dPar >= self.pmin[nSel]):
                break

        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] += dPar
        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
        return newObj

     #----------------------------------------------------
    def Mate(self, partner, compType):
        p1 = random()

        set1 = self.getfeature()
        set2 = partner.getfeature()

        newPar = []
        for i, par in enumerate(set1):
            pNew = p1 *set1[i] + (1.0-p1)*set2[i]
            newPar.append(pNew)

        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
        newObj.setobjective(self.objFunc)
#        newObj.computescore()


        return newObj

    #----------------------------------------------------
    def setID(self, ID):
        self.ID = ID
    #----------------------------------------------------
    def getID(self):
        return self.ID 

    #----------------------------------------------------
    def getscore(self):
        return self.scores
    #----------------------------------------------------
    def setscore(self, scores):
        if len(scores) == self.nObj:
            self.scores = scores
        else:
            raise "Error! Score list size does not match the expected number of objectives"

   #----------------------------------------------------
    def computescore(self):
        try:
            scores = self.objFunc(self)
            self.scores = scores
            if len(scores) != self.nObj:
                print(scores)
                raise ObjectiveMismatch("An unexpected number of objectives have been returned by the objective calculator.")

        except ObjectiveMismatch:
            print("MISMATCH!")
            print("Expcted:", self.nObj)
            print("Got:", len(scores))
            print("Results:", scores )
            raise ObjectiveMismatch
        return True
    #----------------------------------------------------
    def geteng(self):
        return self.scores
    #----------------------------------------------------
    def setfeature(self, newset):
        self.parameters = newset
    #----------------------------------------------------
    def copyfeature(self, copyobj):
        copyfeature = copyobj.getfeature()
        self.setfeature(copyfeature)
    #----------------------------------------------------
    def radialscore(self):
        r = 0.0
        for score in self.scores:
            r += score**2
        r = sqrt(r)
        return r

    #----------------------------------------------------
    def safetycheck(self):
        return True
   #----------------------------------------------------
    def getfeature(self):
        return self.parameters
   #----------------------------------------------------
    def setobjective(self, objFunction):
#        print(objFunction)
        self.objFunc = objFunction
   #----------------------------------------------------
    def addsafety(self, safety):
        self.safetyFunc.append(safety)
   #----------------------------------------------------
    def setsafety(self, safelist):
        self.safetyFunc = safelist
   #----------------------------------------------------
    def optimize(self, logfile=None):
        x0 = self.parameters
        def simplify(parIn, *args):
            newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
            newObj.setfeature(parIn)
            scores = self.objFunc(newObj)
            return scores[-1]
        results = minimize(simplify, x0=x0, method='Nelder-Mead' )
#        print(results)
#        print(results.x)
        self.setfeature(results.x)
        self.computescore()
#        quit()


  #----------------------------------------------------

