from random import random, choice, randint
from math import fabs, exp
from itertools import combinations
from copy import copy

class MultiPool(object):
    #----------------------------------------------------
    def __init__(self, nParameters=1, nObj=1):
        self.members = []
        self.maxmem = 20
        self.famineTries = 40
        self.nAllowedLoses = 9
        self.nPar = nParameters
        self.nObj = nObj
        self.tol = 0.05
        self.curID = 0
        self.weights = [1.0 for x in range(nObj)]
        self.logfile = None

    #----------------------------------------------------
    def __str__(self):

#        self.members = sorted(self.members, key=lambda x: x.getscore(), reverse=True)
        printStr = "Current State of the Pool: \n"
#        outlist = []
        outlist = sorted(self.members, key=lambda x: x.radialscore(), reverse=False)

        for i,obj in enumerate(outlist):
            printStr = printStr + 'Object %s, %s, has a total score of %s and radial of %s. \n' % (obj.getID(),obj.getfeature(), obj.getscore(), obj.radialscore())
#            printStr = printStr + 'Object %s Score %s: %s \n' % (i, score, str(obj))
        printStr = printStr + "--------------------------------\n"
        return printStr

    #----------------------------------------------------
    def Mutate(self):
        from math import fabs
        listSize = len(self.members)
        if listSize >= self.maxmem:
            return
        obj1 = randint(0,listSize-1)
        child = self.members[obj1].Mutate()
        self.curID += 1
        child.setID(self.curID)
        degen = self.degencheck(child)
        if not degen:
            child.computescore()
            self.members.append(child)



    #----------------------------------------------------
    def Mate(self):
        listSize = len(self.members)
        if listSize < 2:
            return
        if listSize >= self.maxmem:
            return

#        compType = randint(0, self.nObj)-1
        compType = 0
        topscore = 1e50
      

#        outlist = sorted(self.members, key=lambda x: x.getscore()[compType], reverse=False)
#        scorelist = sorted([x.getscore() for x in self.members])

        for obj in self.members:
#            score = obj.getscore()
            score = obj.radialscore()
            if score < topscore:
#                topdog = obj
                topscore = score


        problist = []
        norm = 0.0
        for item in self.members:
#            score = item.getscore()[compType]
            score = item.radialscore()
            prob = exp(-score)

            norm += prob
            problist.append(prob)

        if norm == 0.0:
            return

        for indx, item in enumerate(problist):
            problist[indx] = problist[indx]/norm

        ranNum = random()
        sumInt = 0.0
        obj1 = 0
        while sumInt < ranNum and obj1 < listSize-1:
            sumInt += problist[obj1]
            obj1 += 1
        
        obj2 = obj1
        while obj1 == obj2:
            ranNum = random()
            sumInt = 0.0
            obj2 = 0
            while sumInt < ranNum and obj2 < listSize-1:
#                print sumInt, obj2
                sumInt += problist[obj2]
                obj2 += 1
       
        child = self.members[obj1].Mate(self.members[obj2], compType)
        self.curID += 1
        child.setID(self.curID)
        degen = self.degencheck(child)
        if not degen:
            child.computescore()
            self.members.append(child)
        
    #----------------------------------------------------
    def CivilWar(self, logfile):
        canidates = range(0,len(self.members))
#        print canidates
        canSize = len(canidates)
        #Choose which objective will be the
        if canSize < 2:
            return
        ranNum = random()
        sumInt = 0.0
        compType = 0
        while sumInt < ranNum and compType < self.nObj-1:
            sumInt += self.weights[compType]
            compType += 1

#        compType = randint(0, self.nObj)-1
        topdog = -1
        topscore = 1e50
        for obj in canidates:
            score = self.members[obj].getscore()
            if score[compType] < topscore:
                topdog = obj
                topscore = score[compType]

        remList = []
        hitpoints = []
        for i in range(canSize):
            hitpoints.append(self.nAllowedLoses+0)
        # Loop
        for iTries in xrange(self.famineTries):
            #Ensure there are at least two competators remaining
            canSize = len(canidates)
            if canSize < 2:
                break
            #Pick two competators.
            indx1 = randint(0,canSize-1)
            indx2 = randint(0,canSize-1)
            while indx1 == indx2:
                indx2 = randint(0,canSize-1)
            obj1 = self.members[canidates[indx1]]
            obj2 = self.members[canidates[indx2]]

            #Round 1, FIGHT! (Insert Ryu music)
            loser = self.MemberFight(obj1, obj2, topscore, compType)
            if loser == 1:
                loser = canidates[indx1]
                loserIndx = indx1
                loserObj = obj1
            else:
                loser = canidates[indx2]
                loserIndx = indx2
                loserObj = obj2
               
            #Winner stays on. Loser takes a hit. If Loser's HP hits 0 they get kicked from pool.
            if hitpoints[loserIndx] > 1:
                hitpoints[loserIndx] -= 1
            else:
                remList.append(loserObj)
                canidates.remove(loser)


        #Kick out all the losers.
        remList = sorted(remList)
#        print remList
        remList.reverse()
        for item in remList:
            self.members.remove(item)
#            del self.members[item]
#            self.RemoveMember(item, logfile)

    #----------------------------------------------------
    def MemberFight(self, mem1, mem2, topscore, compType):
        score1 = mem1.getscore()[compType]
        score2 = mem2.getscore()[compType]


        #Not a typo. Prob1 is based on Object 2's score.
        #It is designed so that if either side is the top-dog
        #it automatically wins. 
        prob1 = fabs(topscore-score2)**2
        prob2 = fabs(topscore-score1)**2

        if prob1==0.0 and prob2==0.0:
            p1 = 0.5
        else:
            p1 = prob1/(prob1+prob2)
        if random() < p1:
            loser = 2
        else:
            loser = 1
        return loser
    #----------------------------------------------------
    def AddMember(self, obj):
        self.members.append(obj)
        obj.computescore()
    #----------------------------------------------------
    def degencheck(self, newobj):
        for obj in self.members:
            set1 = newobj.getfeature()
            set2 = obj.getfeature()
            delta = 0.0
            for iPar, jPar in zip(set1,set2):
                diff = fabs(iPar - jPar)
                delta += diff
            if delta < 0.05**2:
                return True
        else:
            return False



    #----------------------------------------------------
    def getscores(self):
        scorelist = []
        for item in self.members:
            score = item.getscore()
            scorelist.append(score)
        return scorelist
    #----------------------------------------------------
    def getfeatures(self):
        featlist = []
        for item in self.members:
            feat = list(item.getfeature())
#            print feat
            featlist.append(feat)
        return featlist

    #----------------------------------------------------
    def setweights(self, newWeights):
        normweights = []
        norm = 0.0
        for weight in newWeights:
            norm += weight
        for weight in newWeights:
            normweights.append(weight/norm)
        self.weights = normweights
    #----------------------------------------------------
    def setlogfile(self, logfile):
        self.logfile = logfile
    #----------------------------------------------------
