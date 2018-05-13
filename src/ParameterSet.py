from random import random
from math import exp, sqrt, floor
import copy

class ParameterObj(object):
    #----------------------------------------------------
    def __init__(self, initial=False, nPara=1):
        self.nPara = nPara
        self.score = []
        self.parameters = []
        self.pmax = []
        self.pmin = []
    
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
        nSel = int(floor(random()*nPar))
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        parRange = 0.1*parRange
        dPar = parRange*(2.0*random()-1.0)
        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] += dPar
        newObj = MolObject()
        newObj.setfeature(newParm=newParm)
        newObj.computescore()
        return newObj

    # ----------------------------------------------------
    def Mutate_BigMove(self):
        nPar = len(self.parameters)
        nSel = int(floor(random()*nPar))
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        dPar = parRange*random() + self.pmin[nSel]
        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] = dPar
        newObj = MolObject()
        newObj.setfeature(newParm=newParm)
        newObj.computescore()

        return newObj

     #----------------------------------------------------
    def Mate(self, partner):
        score1 = partner.getscore()
        score2 = partner.getscore()

        newObj = RadialObj()
        newObj.setfeature(x=xn, y=yn)
        newObj.computescore()
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
    def setfeature(self, newset):
        self.parameters = newset
    #----------------------------------------------------
    def copyfeature(self, copyobj):
        x,y,r = copyobj.getfeature()
        self.setfeature(x=x, y=y)

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
        return self.x
  #----------------------------------------------------
#============================================================
def objFunc(obj):
    par = obj.getfeature()
    score1 = -(par[0] - par[1])
    score2 = par[0]**2 + (par[0] - par[1])

    return 


