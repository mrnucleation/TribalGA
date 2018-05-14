from random import random
from math import exp, sqrt, floor, fabs
import copy

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
        for i in xrange(nParameters):
            self.pmax.append(0.0)
            self.pmin.append(0.0)
    
    #----------------------------------------------------
    def __str__(self):
        return ' '.join(self.parameters)
    #----------------------------------------------------
    def Mutate(self):
        ranNum = random()
        if ranNum < 0.3:
            newObj = self.Mutate_SmallMove()
        elif ranNum < 0.66:
            newObj = self.Mutate_BigMove()
        else:
            newObj = self.Mutate_AllMove()
        return newObj
    # ----------------------------------------------------
    def Mutate_SmallMove(self):
        nPar = len(self.parameters)
        nSel = int(floor(random()*nPar)-1)
        parRange = self.pmax[nSel] - self.pmin[nSel] 
        parRange = 0.3*parRange
        while True:
            dPar = parRange*(2.0*random()-1.0)
            if (self.parameters[nSel]+dPar <= self.pmax[nSel]) and (self.parameters[nSel]+dPar >= self.pmin[nSel]):
                break

        newPar = copy.deepcopy(self.parameters)
        newPar[nSel] += dPar
        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
#        newObj.computescore()
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
        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
#        newObj.computescore()

        return newObj
    # ----------------------------------------------------
    def Mutate_AllMove(self):
        newPar = []        
        for i in range(self.nPara):
            parRange = self.pmax[i] - self.pmin[i]
            dPar = parRange*random() + self.pmin[i]
            newPar.append(dPar)

        newObj = ParameterObj(nParameters=self.nPara, nObj=self.nObj)
        newObj.setfeature(newPar)
        newObj.setmax(self.pmax)
        newObj.setmin(self.pmin)
#        newObj.computescore()

        return newObj


     #----------------------------------------------------
    def Mate(self, partner, compType):
        score1 = self.getscore()[compType]
        score2 = partner.getscore()[compType]

        p1 = score1/(score1+score2)

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
#        newObj.computescore()


        return newObj

    #----------------------------------------------------
    def setscore(self, score):
        self.scores = score
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
    def computescore(self):
        scores = self.objFunc(self)
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
    def setobjective(self, objFunc):
        self.objFunc = objFunc

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


