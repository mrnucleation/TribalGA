from random import random, gauss
from math import exp, sqrt, floor, fabs, log
from MultiObjPoolClass import ObjectiveMismatch
from scipy.optimize import minimize
import copy

#class ObjectiveMismatch(Exception):
#    pass

class ParameterObj(object):
    #----------------------------------------------------
    def __init__(self, initial=False, nParameters=1, nObj=1):
        self.ID = 0
        self.nPara = nParameters
        self.nObj = nObj
        self.scores = []
        self.pmax = []
        self.pmin = []
        self.parameters = []
        self.objFunc = trialObj
        self.safetyFunc = []
        for i in xrange(nParameters):
            self.pmax.append(0.0)
            self.pmin.append(0.0)
    
    #----------------------------------------------------
    def __str__(self):
        return ' '.join([str(x) for x in self.parameters])
    #----------------------------------------------------
    def Mutate(self):
        ranNum = random()
        if ranNum < 0.5:
#            newObj = self.Mutate_SmallMove()
#        if ranNum < 0.2:
            newObj = self.Mutate_SmallAllMove()
#        if ranNum < 0.60:
#            newObj = self.Mutate_BigMove()
        else:
            newObj = self.Mutate_AllMove()
        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
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
#        newObj.computescore()
        return newObj
    # ----------------------------------------------------
    def Mutate_SmallAllMove(self):
        newPar = copy.deepcopy(self.parameters)
        for i in range(self.nPara):
            parRange = self.pmax[i] - self.pmin[i]
#            parRange = 0.05*parRange
            sigma = parRange/4.0
            while True:
                dPar = gauss(0.0, sigma)
#                dPar = parRange*(2.0*random()-1.0)
                if (self.parameters[i]+dPar <= self.pmax[i]) and (self.parameters[i]+dPar >= self.pmin[i]):
                    break
            newPar[i] += dPar


        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
#        newObj.setmax(self.pmax)
#        newObj.setmin(self.pmin)
#        newObj.setobjective(self.objFunc)
#        newObj.computescore()
        return newObj

     # ----------------------------------------------------
    def Mutate_LogMove(self):
        nPar = len(self.parameters)
        nSel = int(floor(random()*nPar)-1)
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        accept = False

        while not accept:
            dPar = parRange*random() + self.pmin[nSel]
#            if

        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] = dPar

        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
        return newObj

    # ----------------------------------------------------
    def Mutate_BigMove(self):
        nPar = len(self.parameters)
        nSel = int(floor(random()*nPar)-1)
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        dPar = parRange*random() + self.pmin[nSel]

        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] = dPar

        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
        return newObj
    # ----------------------------------------------------
    def Mutate_AllMove(self):
        newPar = [] 
#        print("ALLMOVE")
        for i in range(self.nPara):
            parRange = self.pmax[i] - self.pmin[i]
            dPar = parRange*random() + self.pmin[i]
            newPar.append(dPar)
        
        print(self.parameters)
        print(newPar)

        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
        return newObj


     #----------------------------------------------------
    def Mate(self, partner, compType):
#        score1 = self.getscore()[compType]
#        score2 = partner.getscore()[compType]
#        score1 = self.radialscore()
#        score2 = partner.radialscore()

#        p1 = score1/(score1+score2)
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
    def setmax(self, maxvals):
        for i,val in enumerate(maxvals):
            self.pmax[i] = val
    #----------------------------------------------------
    def setmin(self, minvals):
        for i,val in enumerate(minvals):
            self.pmin[i] = val

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
        for i, par in enumerate(self.parameters):
            if par > self.pmax[i]:
                return False
            if par < self.pmin[i]:
                return False
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
#============================================================
def trialObj(obj):
    par = obj.getfeature()
    score1 = par[0]**2
    score2 = (par[0]-2)**2
    rad = score1**2 + score2**2
    rad = sqrt(rad)
#    scores = []
    scores = [score1, score2, rad]
#    for item in par:
#      score = fabs(3 - item)
#      scores.append(score)

    return scores


