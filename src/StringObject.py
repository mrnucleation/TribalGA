from random import random, shuffle
from math import exp, fabs

#Binary String Object.  By default the constraint applies to the number of 0s allowed
#Example Object = "01000100100001110000"
class StringObj(object):
    #----------------------------------------------------
    def __init__(self, initial=False):
        self.ID = 0
        self.string = ""
        self.maxLength = 0
        self.constraints = None
        self.score = 0.0
        self.eng = 0.0
        self.objFunc = objFunc
    
    #----------------------------------------------------
    def __str__(self):
        return self.string
    #----------------------------------------------------
    def Mutate(self):
        if random() < 0.1:
            newStr = self.Mutate_Scatter()
        else:
            newStr = self.Mutate_Swap()

#        newStr = self.Mutate_Scatter()
        newObj = StringObj()
        newObj.setfeature(newStr)
        newObj.setconstraint(self.constraints)
        newObj.set
        newObj.computescore()
        return newObj
     #----------------------------------------------------
    def Mutate_Swap(self):
        #This moves exchanges a single 1 with a single 0.
        newStr = ''.join(self.string)
        zeros = []
        ones = []
        for i, char in enumerate(self.string):
            if char == "0":
                zeros.append(i)
            else:
                ones.append(i)
        shuffle(zeros)
        shuffle(ones)
        site1 = ones[0]
        site0 = zeros[0]
        newStr = newStr[:site1] + "0" + newStr[site1+1:]
        newStr = newStr[:site0] + "1" + newStr[site0+1:]
        return newStr   
    #----------------------------------------------------
    def Mutate_Scatter(self):
        #This move completely scrambles the string
        newStr = ''.join(["1" for x in range(self.maxLength)])
        newSites = range(0, self.maxLength)
        shuffle(newSites)
        for site in newSites[0:self.constraints]:
            newStr = newStr[:site] + "0" + newStr[site+1:]
        return newStr


     #----------------------------------------------------
    def Mate(self, partner, compType=None):
        partnerStr = partner.getfeature()
        newStr = ""
        for iChar, jChar in zip(self.string, partnerStr):
            if iChar == jChar:
                newStr = newStr + iChar
            else:
                if random() < 0.5:
                    newStr = newStr + iChar
                else:
                    newStr = newStr + jChar

        # Enforce the constraints by swapping out 
        if self.constraints is not None:
            zeros = []
            ones = []
            for i, char in enumerate(newStr):
                if char == "0":
                    zeros.append(i)
                else:
                    ones.append(i)

            nZeros = len(zeros)
            diff = int(round(fabs(nZeros - self.constraints)))
            if nZeros > self.constraints: 
                shuffle(zeros)
                for position in zeros[0:diff]:
                    newStr = newStr[:position] + "1" + newStr[position+1:]

            elif nZeros < self.constraints:
                shuffle(ones)
                for position in ones[0:diff]:
                    newStr = newStr[:position] + "0" + newStr[position+1:]


        newObj = StringObj()
        newObj.setfeature(newStr)
        newObj.setconstraint(self.constraints)
        newObj.computescore()
#        newObj.findgroup
        return newObj

    #----------------------------------------------------
    def fight(self, opponent):
        if self.score <= 0.0:
           loser = 1
           return
        if opponent.score <= 0.0:
           loser = 2
           return
        
        winprob = self.score/(opponent.score+self.score)
        if random() < winprob:
            loser = 2
        else:
            loser = 1
        return loser

    #----------------------------------------------------
    def setscore(self, score):
        self.score = score
    #----------------------------------------------------
    def getscore(self):
        return self.score
   #----------------------------------------------------
    def computescore(self):
        score, eng = self.objFunc(self)
        self.score = [score]
        self.eng = eng
        return True
    #----------------------------------------------------
    def geteng(self):
        return self.eng
    #----------------------------------------------------
    def setfeature(self, instr):
        self.maxLength = len(instr)
        self.string = instr
    #----------------------------------------------------
    def copyfeature(self, copyobj):
        outstr = copyobj.getfeature()

        self.setfeature(outstr)
   #----------------------------------------------------
    def getfeature(self):
        return self.string

    #----------------------------------------------------
    def safetycheck(self):
        return True
   #----------------------------------------------------
    def findgroup(self):
        groupID = 0
        return groupID
    #----------------------------------------------------
    def setObjective(self, objective):
        self.objFunc = objective

    #----------------------------------------------------
    def setID(self, ID):
        self.ID = ID
    #----------------------------------------------------
    def getID(self):
        return self.ID 
    #----------------------------------------------------
    def getconstraint(self):
        return self.constraint

    #----------------------------------------------------
    def setconstraint(self, maxzeros):
        self.constraints = maxzeros
    #----------------------------------------------------
    def radialscore(self):
        return self.score[0]

   #----------------------------------------------------
#============================================================
def objFunc(obj):
    atomstring = obj.getfeature()
    eng = 0.0
    nAtoms = len(atomstring)
    for i, char in enumerate(atomstring):
        if char == "1":
            continue
        prevVal = (i-1)%nAtoms
        nextVal = (i+1)%nAtoms
        if atomstring[prevVal] == "0":
            eng += -1.0

        if atomstring[nextVal] == "0":
            eng += -1.0
    val = exp(eng)
    return val, eng


