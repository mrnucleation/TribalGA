from random import random
from math import exp, sqrt, floor
import copy

class ParameterObj(object):
    #----------------------------------------------------
    def __init__(self, initial=False, nParameters=1):
        self.nPara = nParameters
        self.scores = []
        self.pmax = []
        self.pmin = []
        self.parameters = []
        for i in xrange(nParameters):
            self.pmax.append(0.0)
            self.pmin.append(0.0)
    
    #----------------------------------------------------
    def __str__(self):
        return ' '.join(self.parameters)
    #----------------------------------------------------
    def Mutate(self):
        ranNum = random()
        if ranNum < 0.9:
            newObj = self.Mutate_SmallMove()
        else:
            newObj = self.Mutate_BigMove()
        return newObj
    # ----------------------------------------------------
    def Mutate_SmallMove(self):
        nPar = len(self.parameters)
        nSel = int(floor(random()*nPar)-1)
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        parRange = 0.1*parRange
        while True:
            dPar = parRange*(2.0*random()-1.0)
            if (self.parameters[nSel]+dPar <= self.pmax[nSel]) and (self.parameters[nSel]+dPar >= self.pmin[nSel]):
                break

        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] += dPar
        newObj = ParameterObj(nParameters=self.nPara)
        newObj.setfeature(newPar)
        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
        newObj.computescore()
        return newObj

    # ----------------------------------------------------
    def Mutate_BigMove(self):
        nPar = len(self.parameters)
        nSel = int(floor(random()*nPar)-1)
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        dPar = parRange*random() + self.pmin[nSel]

        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] = dPar

        newObj = ParameterObj(nParameters=self.nPara)
        newObj.setfeature(newPar)

        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
        newObj.computescore()

        return newObj

     #----------------------------------------------------
    def Mate(self, partner):
        score1 = partner.getscore()
        score2 = partner.getscore()

        newObj = ParameterObj(nParameters=self.nPara)
        newObj.setfeature(newParm=newParm)
        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
        newObj.computescore()
        return newObj

    #----------------------------------------------------
    def setscore(self, score):
        self.scores = score
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
    def computescore(self):
        scores = objFunc(self)
        self.scores = scores
    #----------------------------------------------------
    def geteng(self):
        return self.scores
    #----------------------------------------------------
    def setfeature(self, newset):
        self.parameters = newset
    #----------------------------------------------------
    def copyfeature(self, copyobj):
        x,y,r = copyobj.getfeature()
        self.setfeature(x=x, y=y)
    #----------------------------------------------------
    def radialscore(self):
        r = 0.0
        for score in self.scores:
            r += score**2
        r = sqrt(r)


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
#============================================================
def objFunc(obj):
    par = obj.getfeature()
#    score1 = 3-(par[0] - par[1])
#    score2 = 3+par[0]**2 + (par[0] - par[1])

    score1 = 3 - par[0]
    score2 = 3 - par[1]
    return [score1, score2]


