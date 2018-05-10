from random import random, choice, randint
from math import fabs


class MultiPool(object):
    #----------------------------------------------------
    def __init__(self):
        self.members = []
        self.maxmem = 5000
        self.famineTries = 3
        self.nObj = 1
        self.tol = 0.05
    #----------------------------------------------------
    def __str__(self):

#        self.members = sorted(self.members, key=lambda x: x.getscore(), reverse=True)
        printStr = "Current State of the Pool: \n"
        outlist = []
        outlist = sorted(outlist, key=lambda x: x[1], reverse=True)

        for i,obj in enumerate(outlist):
            printStr = printStr + 'Tribe %s has %s members with a total score of %s.  Best memeber score: %s  \n' % (obj[0], obj[1], obj[2], obj[3])
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
        child.computescore()
        self.members.append(child)

    #----------------------------------------------------
    def Mate(self):
        listSize = len(self.members)
        if listSize < 2:
            return
        if listSize >= self.maxmem:
            return
        problist = []
        norm = 0.0
        for item in self.members:
            score = item.getscore()
            norm += score
            problist.append(score)

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
                sumInt += problist[obj2]
                obj2 += 1

        child = self.members[obj1].Mate(self.members[obj2])
        child.computescore()
        groupID = child.findgroup()
        if groupID in self.group:
            self.group[groupID].append(child)
        else:
            self.group[groupID] = [child]
        self.members.append(child)
        
    #----------------------------------------------------
    def CivilWar(self, logfile):
        canidates = range(0,len(self.members))
        canSize = len(canidates)
        #Choose which objective will be the
        if canSize < 2:
            return
        compType = randint(0, len(self.nObj))
        topdog = -1
        topscore = 1e50
        for obj in canidates:
            score = self.members[obj].getscore()
            if score < topscore:
                topdog = obj
                topscore = score

        remList = []
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
                loser = indx1
                remList.append(obj1)
            else:
                loser = indx2
                remList.append(obj2)

            #Winner stays on. Loser exits the pool.
            canidates.remove(loser)

        #Kick out all the losers.
        remList = sorted(remList)
        remList.reverse()
        for item in remList:
            self.members.remove(item)
            self.RemoveMember(item, logfile)

    #----------------------------------------------------
    def MemberFight(self, mem1, mem2, topscore, compType):
        score1 = mem1.getscore()[compType]
        score2 = mem2.getscore()[compType]

        #Not a typo. Prob1 is based on Object 2's score.
        #It is designed so that if either side is the top-dog
        #it automatically wins. 
        prob1 = fabs(topscore-score2)
        prob2 = fabs(topscore-score1)


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
