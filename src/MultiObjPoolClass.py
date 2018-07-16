from random import random, choice, randint
from math import fabs, exp, sqrt
from itertools import combinations
from copy import copy

class ObjectiveMismatch(Exception):
    pass

class MultiPool(object):
    #----------------------------------------------------
    def __init__(self, nParameters=1, nObj=1):
        self.members = []
        self.maxmem = 75
        self.famineTries = 20
        self.nAllowedLoses = 5
        self.nPar = nParameters
        self.nObj = nObj
        self.tol = 0.05
        self.curID = 1
        self.weights = [1.0 for x in range(nObj)]
        self.logfile = None

    #----------------------------------------------------
    def __str__(self):

#        self.members = sorted(self.members, key=lambda x: x.getscore(), reverse=True)
        printStr = "Current State of the Pool: \n"
#        outlist = []
        outlist = sorted(self.members, key=lambda x: x.radialscore(), reverse=False)

        for i,obj in enumerate(outlist):
#            printStr = printStr + 'Object %s, has a total score of %s and radial of %s. \n' % (obj.getID(), obj.getscore(), obj.radialscore())
            printStr = printStr + 'Object %s, has a radial of %s. \n' % (obj.getID(), obj.radialscore())
#            printStr = printStr + 'Object %s Score %s: %s \n' % (i, score, str(obj))
        printStr = printStr + "--------------------------------\n"
        return printStr

    #----------------------------------------------------
    def Mutate(self):
        from math import fabs
        listSize = len(self.members)
        if listSize >= self.maxmem:
            return
        #Randomly select an object.  Probaiblity is based on the radial score.
        topscore = 1e50
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
#            prob = exp(-(score-topscore))
            if topscore-score > 1e7:
                prob = 0.0
            else:
#                prob = exp((topscore-score))
                prob = 1.0/score**(1.0/3.0)

            norm += prob
            problist.append(prob)

        if norm == 0.0:
            print("Norm problem")
            return

        for indx, item in enumerate(problist):
            problist[indx] = problist[indx]/norm

        ranNum = random()
        sumInt = 0.0
        obj1 = 0
        while sumInt < ranNum and obj1 < listSize-1:
            sumInt += problist[obj1]
            obj1 += 1
#        print obj1
#        print(problist)
#        obj1 = randint(0,listSize-1)
        child = self.members[obj1].Mutate()
        self.curID += 1
        child.setID(self.curID)
        degen = self.degencheck(child)
        if not degen:
            success = child.computescore()
            if success:
                print("Adding object %s to the pool"%(self.curID))
                self.members.append(child)
        else:
            print("Object %s too similar to existing object."%(self.curID))



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
            if topscore-score > 1e7:
                prob = 0.0
            else:
#                prob = exp((topscore-score))
                prob = 1.0/sqrt(score)


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
        
        cnt = 0
        obj2 = obj1
        while obj1 == obj2:
            obj2 = randint(0,listSize-1)
#            ranNum = random()
#            sumInt = 0.0
#            obj2 = 0
#            while sumInt < ranNum and obj2 < listSize-1:
#                print sumInt, obj2
#                sumInt += problist[obj2]
#                obj2 += 1

            cnt += 1
            if cnt > 1000:
                return
        ID1 = self.members[obj1].getID()
        ID2 = self.members[obj2].getID()
        print("Crossing Object %s with Object %s" % (ID1, ID2))
        child = self.members[obj1].Mate(self.members[obj2], compType)
        self.curID += 1
        child.setID(self.curID)
        degen = self.degencheck(child)
        if not degen:

            success = child.computescore()
            if success:
                print("Adding object %s to the pool"%(self.curID))
                self.members.append(child)
        else:
            print("Object %s too similar to existing object."%(self.curID))
        
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
        try:
            for obj in canidates:
                score = self.members[obj].getscore()
                if score[compType] < topscore:
                    topdog = obj
                    topscore = score[compType]
        except IndexError:
            print(compType)
            raise IndexError

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
#        obj.computescore()
    #----------------------------------------------------
    def degencheck(self, newobj):
        if len(self.members) < 2:
            return False
        for obj in self.members:
            set1 = newobj.getfeature()
            set2 = obj.getfeature()
            delta = 1e7
            nPar = 0
            for iPar, jPar in zip(set1,set2):
                diff = fabs(iPar - jPar)/jPar
                delta = max(delta, diff)
#                nPar += 1.0
#            delta = delta/nPar
            if delta < 0.05:
                return True
        else:
            return False
    #----------------------------------------------------
    def getnummembers(self):
        return self.members

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
        if len(newWeights) != self.nObj:
            raise ObjectiveMismatch("Number of weights passed does not match the number of objectives")
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
