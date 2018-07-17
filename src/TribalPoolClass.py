from random import random, choice, randint
from math import fabs, floor

class TribePool(object):
    #----------------------------------------------------
    def __init__(self):
        self.members = []
        self.maxmem = 1000
        self.groups = {}
        self.famineTries = 20
        self.tol = 0.05
        self.filename = "Config_%s.xyz"
    #----------------------------------------------------
    def __str__(self):

#        self.members = sorted(self.members, key=lambda x: x.getscore(), reverse=True)
        printStr = "Current State of the Pool: \n"
        outlist = []
        for key, item in self.groups.iteritems():

            total = 0.0
            best = -1e50
            nMemb = len(item)
            for member in item:
                score = member.getscore()
                if score > best:
                    best = score
                total += score
            outlist.append([key, nMemb, total, best])

        outlist = sorted(outlist, key=lambda x: x[2], reverse=True)

        for i,obj in enumerate(outlist):
            printStr = printStr + 'Tribe %s has %s members with a total score of %s.  Best memeber score: %s  \n' % (obj[0], obj[1], obj[2], obj[3])
#            printStr = printStr + 'Object %s Score %s: %s \n' % (i, score, str(obj))
        printStr = printStr + "--------------------------------\n"
        return printStr

    #----------------------------------------------------
    def Mutate(self):
        '''
         This function creates a new structure by performing a small modification of an existing structure.
         
        '''
        #Check to make sure we haven't hit the maximum number of objects yet.
        listSize = len(self.members)
        if listSize >= self.maxmem:
            return

        #Choose a parent
        obj1 = randint(0,listSize-1)

        #Create a mutated structure. 
        child = self.members[obj1].Mutate()

        #Check to see if the child satisfies all constraints.
        result = child.safetycheck()
        if not result:
            return


        #Figure out which tribe the new member belongs to and add them to it.
        child.computescore()
        groupID = child.findgroup()
        if groupID in self.groups:
            self.groups[groupID].append(child)
        else:
            self.groups[groupID] = [child]
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
        obj1 = -1
        while sumInt < ranNum and obj1 < listSize-1:
            sumInt += problist[obj1]
            obj1 += 1
        
        obj2 = obj1
        while obj1 == obj2:
            ranNum = random()
            sumInt = 0.0
            obj2 = -1
            while sumInt < ranNum and obj2 < listSize-1:
                sumInt += problist[obj2]
                obj2 += 1

        child = self.members[obj1].Mate(self.members[obj2])

        #Check to see if the child satisfies all constraints.
        result = child.safetycheck()
        if not result:
            return

        child.computescore()
        groupID = child.findgroup()
        if groupID in self.group:
            self.group[groupID].append(child)
        else:
            self.group[groupID] = [child]
        self.members.append(child)
        
    #----------------------------------------------------
    def CivilWar(self, logfile):
        canidates = sorted(list(self.groups.keys()))
        canSize = len(canidates)
        if canSize < 2:
            return
        
        avgSize = 0.0
        nCount = 0.0
        for groupID in canidates:
            nCount += 1.0
            avgSize += len(self.groups[groupID])
        avgSize = avgSize/(3.0*nCount)
        if avgSize < 1.0:
            self.famineTries = 1
        else:
            self.famineTries = int(floor(avgSize))




        canSize = len(canidates)
        oldCanSize = len(canidates)-1
        for iTries in xrange(self.famineTries):
            canSize = len(canidates)
            
            if canSize < 2:
                break

            #In the event that one of the canidates were removed from competition
            #the probability list needs to be recalculated. 
            if oldCanSize != canSize:
                problist = []
                norm = 0.0
                for groupID in canidates:
                    total = 0.0
                    for obj in self.groups[groupID]:
                        total += obj.getscore()
                    norm += total
                    problist.append(total)

                #Normalize
                try:
                    for indx, item in enumerate(problist):
                        problist[indx] = problist[indx]/norm
                except ZeroDivisionError:
                    print "Normalization ERROR!"
                    print problist
                    raise ZeroDivisionError
#                print problist


            ranNum = random()
            sumInt = 0.0
            indx1 = -1
            listSize = len(problist)
            while sumInt < ranNum and indx1 < listSize:
                indx1 += 1
                sumInt += problist[indx1]
#            print problist[indx1], indx1
#            indx1 -= 1
#            print problist[indx1], indx1
#            print ' '.join([str(x) for x in problist])
#            print indx1, ranNum, sumInt

            problist2 = []
            norm = 0.0
            for indx, groupID in enumerate(canidates):
                if indx == indx1:
                    problist2.append(0.0)
                    continue
                total = 0.0
                for obj in self.groups[groupID]:
                    total += obj.getscore()
                norm += total
                problist2.append(total)
            try:
                for indx, item in enumerate(problist):
                    problist2[indx] = problist2[indx]/norm
            except ZeroDivisionError:
                print "Normalization ERROR!"
                print problist2
                raise ZeroDivisionError


            cnt = 0
            while True:
                ranNum = random()
                sumInt = 0.0
                indx2 = -1
                while sumInt < ranNum and indx2 < listSize-1:
                    sumInt += problist2[indx2]
                    indx2 += 1
                indx2 -= 1
                if indx1 != indx2:
                    break
                cnt += 1
                if cnt > 4:
                    while True:
                        indx2 = randint(0, listSize-1)
                        if indx1 != indx2:
                            break

                    break
            try:
                group1 = canidates[indx1]
                group2 = canidates[indx2]
            except:
                print indx1, indx2, len(canidates)
                raise "Blah"
#            print "Probability: %s vs %s"%(problist[, group2)
#            print "%s vs %s"%(group1, group2)
#            print listSize, obj1, obj2
#            for i,obj in enumerate(self.members):
#                print i,obj
            loser = self.MemberFight(self.groups[group1], self.groups[group2])
            if loser == 1:
                loser = group1
                loserindx = indx1
            else:
                loser = group2
                loserindx = indx2

            if len(self.groups[loser]) == 1:
                canidates.remove(loser)
                for item in self.groups[loser]:
                    self.members.remove(item)
                del self.groups[loser]
#                remList.append(loser)
            else:
                try:
                    remMemb = self.RIP(self.groups[loser])
                except ZeroDivisionError:
                    remMemb = 1
                yorick = self.groups[loser][remMemb]
                self.groups[loser].remove(yorick)
                self.members.remove(yorick)

            oldCanSize = canSize

#        remList = sorted(remList)
#        remList.reverse()
#        print remList
#        for i, item in enumerate(self.members):
#            print i, item
#        for item in remList:
#            self.members.remove(item)
#            self.RemoveMember(item, logfile)
#        print remList
#        for i, item in enumerate(self.members):
#            print i, item

#        print "---------------------------------------"
    #----------------------------------------------------
    def Famine(self, logfile):
        if len(self.members) < 2:
            return

        avgSize = 0.0
        nCount = 0.0
        for groupID in self.groups.keys():
            nCount += 1.0
            avgSize += len(self.groups[groupID])
        avgSize = avgSize/(3.0*nCount)
        if avgSize < 1.0:
            self.famineTries = 1
        else:
            self.famineTries = int(floor(avgSize))


        canidates = sorted(list(self.groups.keys()))
        canSize = len(canidates)
        #Construct the Probability Table such that larger groups have a higher chance
        #of being chosen. 
        # Loop
        canSize = len(canidates)
        oldCanSize = len(canidates)-1
        for iTries in xrange(self.famineTries):
            canSize = len(canidates)

            #In the event that one of the canidates were removed from competition
            #the probability list needs to be recalculated. 
            if oldCanSize != canSize:
                problist = []
                norm = 0.0
                for groupID in canidates:
                    total = 0.0
                    for obj in self.groups[groupID]:
                        total += obj.getscore()
                    norm += total**5
                    problist.append(total**5)

                #Normalize
                try:
                    for indx, item in enumerate(problist):
                        problist[indx] = problist[indx]/norm
                except ZeroDivisionError:
                    print "Normalization ERROR!"
                    print problist
                    raise ZeroDivisionError

            ranNum = random()
            sumInt = 0.0
            indx1 = -1
            listSize = len(problist)
            while sumInt < ranNum and indx1 < listSize-1:
                sumInt += problist[indx1]
                indx1 += 1
            indx1 -= 1
#            print problist
#            print indx1, ranNum, sumInt
            

            group1 = canidates[indx1]

            if len(self.groups[group1]) == 1:
                canidates.remove(group1)
                for item in self.groups[group1]:
                    self.members.remove(item)
                del self.groups[group1]
#                remList.append(group1)
            else:
                try:
                    remMemb = self.RIP(self.groups[group1])
                except ZeroDivisionError:
                    remMemb = 1
                yorick = self.groups[group1][remMemb]
                self.groups[group1].remove(yorick)
                self.members.remove(yorick)

            oldCanSize = canSize

#        remList = sorted(remList)
#        remList.reverse()
#        print remList
#        for i, item in enumerate(self.members):
#            print i, item
#        for item in remList:
#            self.members.remove(item)
#            self.RemoveMember(item, logfile)
#        print remList
#        for i, item in enumerate(self.members):
#            print i, item

#        print "---------------------------------------"

    #----------------------------------------------------
    def MemberFight(self, group1, group2):
        score1 = 0.0
        for item in group1:
            score1 += item.getscore()

        score2 = 0.0
        for item in group2:
            score2 += item.getscore()

        p1 = score1/(score1+score2)
        if random() < p1:
            loser = 2
        else:
            loser = 1
        return loser
    #----------------------------------------------------
    #This function picks the group member which must be removed from the pool after the group has lost a competition.
    def RIP(self, group):
        #Construct probabity list
        if len(group) == 1:
            return 1

        problist = []
        norm = 0.0
        topscore = 0.0

        for item in group:
            score = item.getscore()
            if score > topscore:
                topscore = score


        for item in group:
            score = item.getscore()
            norm += topscore-score
            problist.append(topscore-score)

        try:
            for indx, item in enumerate(problist):
                problist[indx] = problist[indx]/norm
        except ZeroDivisionError:
            print problist
            raise ZeroDivisionError
            
            

        ranNum = random()
        sumInt = 0.0
        yorick = -1
        listSize = len(problist)
        while sumInt < ranNum and yorick < listSize:
            yorick += 1
            sumInt += problist[yorick]
            
        #Alas poor Yorick, We knew him well.
        return yorick

    #----------------------------------------------------
    def AddMember(self, obj):
        self.members.append(obj)
        obj.computescore()
        groupID = obj.findgroup()
        if groupID in self.groups:
            self.groups[groupID].append(obj)
        else:
            self.groups[groupID] = [obj]


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
    def dumpfeatures(self):
        for key, group in self.groups.iteritems():
            with open( self.filename % (str(key)), "w" ) as outfile: 
                for item in group:
                    score = item.getscore()
                    outfile.write("13 \n")
                    outfile.write("\n")
                    feature = item.getfeature()
                    for atom in feature:
                        outlist = [str(x) for x in atom] + [str(score), "\n"]
                        outfile.write(' '.join(outlist))

    #----------------------------------------------------
