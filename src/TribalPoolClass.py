from random import random, choice, randint
from math import fabs, floor, sqrt, log

class TribePool(object):
    #----------------------------------------------------
    def __init__(self):
        self.members = []
        self.maxmem = 5000
        self.nMinimize = 1
        self.groups = {}
        self.famineTries = int(round(self.maxmem/1.2))
        self.warTries = 50
        self.tol = 0.05
        self.curID = 1
        self.filename = "Config_%s.xyz"
    #----------------------------------------------------
    def __str__(self):

#        self.members = sorted(self.members, key=lambda x: x.getscore(), reverse=True)
        printStr = "Current State of the Pool: \n"
        outlist = []
#        for key, item in self.groups.iteritems():
        for key, item in self.groups.items():

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
    def Mutate(self, logfile=None):
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
        child.setID(self.curID)
        self.curID += 1

        #Check to see if the child satisfies all constraints.
        result = child.safetycheck()
        if not result:
#            child.dumpfeature()
            if logfile != None:
                logfile.write("Child (%s) of object %s failed safety check. \n"%(child.getID(), self.members[obj1].getID()))
                logfile.flush()
            return


        #Figure out which tribe the new member belongs to and add them to it.
        child.computescore()
        groupID = child.findgroup()
        if groupID in self.groups:
            self.groups[groupID].append(child)
        else:
            self.groups[groupID] = [child]
        if logfile != None:
            logfile.write("Adding object %s to %s. (Score: %s) \n"%(child.getID(), groupID, child.getscore()))
            logfile.flush()


        self.members.append(child)
    '''
    #----------------------------------------------------
    def Mate(self, logfile=None):
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
        child.setID(self.curID)
        self.curID += 1

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
    '''

    #-----------------------------------
    def Mate(self, logfile=None): 
        listSize = len(self.members)
        if listSize < 2:
            return
        if listSize >= self.maxmem:
            return

        topscore = 0.0
        for obj in self.members:
            score = obj.radialscore()
            if score > topscore:
                topscore = score


        rawproblist = []
        problist = []
        norm = 0.0
        for item in self.members:
#            score = item.getscore()
            score = item.radialscore()
            try:
#               prob = 1.0/sqrt(score)
                if score > 1.0:
                    prob = log(score)
                else:
                    prob = 0.0
            except ZeroDivisionError:
#                    print score
                prob = 0.0

            norm += prob
            rawproblist.append(prob)

        if norm == 0.0:
            return

        problist = [x/norm for x in rawproblist]

        ranNum = random()
        sumInt = 0.0
        obj1 = -1
        while sumInt < ranNum and obj1 < listSize:
            obj1 += 1
            sumInt += problist[obj1]
        
        problist = []
        norm = 0.0
        for i, prob in enumerate(rawproblist):
            if i != obj1:
                norm += prob

        if norm == 0.0:
            return
        for i, prob in enumerate(rawproblist):
            if i != obj1:
                problist.append(prob/norm)
        cnt = 0
        obj2 = obj1
        while obj1 == obj2:
#            obj2 = randint(0, listSize-1)
            ranNum = random()
            sumInt = 0.0
            obj2 = -1
            while sumInt < ranNum and obj2 < listSize:
                obj2 += 1
                sumInt += problist[obj2]
#            ranNum = random()
#            sumInt = 0.0
#            obj2 = 0
#            while sumInt < ranNum and obj2 < listSize-1:
#                sumInt += problist[obj2]
#                obj2 += 1

            cnt += 1
            if cnt > 1000:
                return
        ID1 = self.members[obj1].getID()
        ID2 = self.members[obj2].getID()
        if logfile != None:
            logfile.write("Crossing Object %s with Object %s \n" % (ID1, ID2))
        child = self.members[obj1].Mate(self.members[obj2])
        child.setID(self.curID)
        self.curID += 1

        #Check to see if the child satisfies all constraints.
        result = child.safetycheck()
        if not result:
            if logfile != None:
                logfile.write( "Child %s failed safety check. \n"%(child.getID()) )
                logfile.flush()
            return


        #Figure out which tribe the new member belongs to and add them to it.
        child.computescore()
        groupID = child.findgroup()
        if groupID in self.groups:
            self.groups[groupID].append(child)
        else:
            self.groups[groupID] = [child]
        if logfile != None:
            logfile.write("Adding object %s to %s. (Score: %s) \n"%(child.getID(), groupID, child.getscore()))
            logfile.flush()
        self.members.append(child)

    #----------------------------------------------------
    def CivilWar(self, logfile=None):
        canidates = sorted(list(self.groups.keys()))
        canSize = len(canidates)
        if canSize < 2:
            return

        if logfile != None:
            logfile.write("Starting Civil War. \n")
            logfile.flush()
#        avgSize = 0.0
#        nCount = 0.0
#        for groupID in canidates:
#            nCount += 1.0
#            avgSize += len(self.groups[groupID])
#        avgSize = avgSize/(3.0*nCount)
#        if avgSize < 1.0:
#            self.famineTries = 1
#        else:
#            self.famineTries = int(floor(avgSize))




        canSize = len(canidates)
        oldCanSize = len(canidates)-1
#        for iTries in xrange(self.warTries):
        for iTries in range(self.warTries):
            canSize = len(canidates)
            
            if canSize < 2:
                break

            #In the event that one of the canidates were removed from competition
            #the probability list needs to be recalculated. 
            if oldCanSize != canSize:
                problist = []
                norm = 0.0
                for groupID in canidates:
                    prob = 0.0
                    for obj in self.groups[groupID]:
                        prob += obj.getscore()
#                    prob = len(self.groups[groupID])
                    norm += prob
                    problist.append(prob)

                #Normalize
                try:
                    for indx, item in enumerate(problist):
                        problist[indx] = problist[indx]/norm
                except ZeroDivisionError:
                    problist = [1.0/float(len(problist)) for x in problist]
#                    print("Normalization ERROR!")
#                    print(problist)
      

#                    raise ZeroDivisionError
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
                prob = 0.0
                for obj in self.groups[groupID]:
                    prob += obj.getscore()
#                prob = len(self.groups[groupID])
                norm += prob
                problist2.append(prob)
            try:
                for indx, item in enumerate(problist):
                    problist2[indx] = problist2[indx]/norm
            except ZeroDivisionError:
                problist2 = [1.0/float(len(problist)-1.0) for x in problist]
                problist2[indx1] = 0.0
#                print( "Normalization ERROR!")
#                print( problist2)
#                return
#                raise ZeroDivisionError


            cnt = 0
            while True:
                ranNum = random()
                sumInt = 0.0
                indx2 = -1
                while sumInt < ranNum and indx2 < listSize:
                    indx2 += 1
                    sumInt += problist2[indx2]
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
                print( indx1, indx2, len(canidates))
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
#                print "Group %s eliminated"%(loser)
                del self.groups[loser]
                if logfile != None:
                    logfile.write("Group %s has been wiped out.\n"%(loser))
                    logfile.flush()


#                remList.append(loser)
            else:
                try:
                    remMemb = self.RIP(self.groups[loser])
                except ZeroDivisionError:
                    remMemb = 1
                yorick = self.groups[loser][remMemb]
                if logfile != None:
                    logfile.write("Object %s has been removed from the pool. \n"%(yorick.getID()) )
                    logfile.flush()

                self.groups[loser].remove(yorick)
                self.members.remove(yorick)

            oldCanSize = canSize
        if logfile != None:
            logfile.write("Civil War Over. \n")
            logfile.flush()

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
    def Famine(self, logfile=None):
        if len(self.members) < 2:
            return

        canidates = sorted(list(self.groups.keys()))
        canSize = len(canidates)
        problist = []
        norm = 0.0
        for groupID in canidates:
#                    total = 0.0
#                    for obj in self.groups[groupID]:
#                        total += obj.getscore()
            prob = len(self.groups[groupID])
            norm += prob
            problist.append(prob)


        #Construct the Probability Table such that larger groups have a higher chance
        #of being chosen. 
        # Loop
        canSize = len(canidates)
        oldCanSize = len(canidates)-1
        for iTries in range(self.famineTries):
            canSize = len(canidates)
            if len(self.members) < int(round(self.maxmem/2.0)):
                if logfile != None:
                    logfile.write("Famine has ended. \n")
                    logfile.flush()
                break


            #In the event that one of the canidates were removed from competition
            #the probability list needs to be recalculated. 
            if oldCanSize != canSize:
                problist = []
                norm = 0.0
                for groupID in canidates:
#                    total = 0.0
#                    for obj in self.groups[groupID]:
#                        total += obj.getscore()
                    prob = len(self.groups[groupID])
                    norm += prob
                    problist.append(prob)

                #Normalize
                try:
                    for indx, item in enumerate(problist):
                        problist[indx] = problist[indx]/norm
                except ZeroDivisionError:
                    problist = [1.0/float(len(problist)) for x in problist]
#                    print( "Normalization ERROR!")
#                    print( problist)
#                    raise ZeroDivisionError


            ranNum = random()
            sumInt = 0.0
            indx1 = -1
            listSize = len(problist)
            while sumInt < ranNum and indx1 < listSize:
                indx1 += 1
                sumInt += problist[indx1]

#            print problist
#            print indx1, ranNum, sumInt
            
            group1 = canidates[indx1]
            if len(self.groups[group1]) < 20:
                continue


            if len(self.groups[group1]) == 1:
                canidates.remove(group1)
                for item in self.groups[group1]:
                    self.members.remove(item)
                del self.groups[group1]
                if logfile != None:
                    logfile.write("Group %s has been wiped out.\n"%(group1))
                    logfile.flush()
#                remList.append(group1)
            else:
                try:
                    remMemb = self.RIP(self.groups[group1])
                except ZeroDivisionError:
                    remMemb = 1
                yorick = self.groups[group1][remMemb]
                self.groups[group1].remove(yorick)
                self.members.remove(yorick)
                if logfile != None:
                    logfile.write("Object %s has been removed from the pool. \n"%(yorick.getID()) )
                    logfile.flush()

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
#            print score
            if score > topscore:
                topscore = score


        shiftconst = 0.0
        for item in group:
            score = item.getscore()
            norm += topscore-score+shiftconst
            problist.append(topscore-score+shiftconst)

#        print topscore
#        print problist
        try:
            for indx, item in enumerate(problist):
                problist[indx] = problist[indx]/norm
        except ZeroDivisionError:
            problist = [1.0/float(len(problist)) for x in problist]
#            print( problist)
#            raise ZeroDivisionError
#        print problist
#        print 
            
            

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
#        for key, group in self.groups.iteritems():
        for key, group in self.groups.items():
            with open( self.filename % (str(key)), "w" ) as outfile: 
                sortlist = sorted(group, key=lambda x: x.getscore(), reverse=True)
                for item in sortlist:
                    score = item.getscore()
                    eng = item.geteng()
                    feature = item.getfeature()
#                    print(feature)
                    outfile.write("%s \n"%(len(feature)))
                    outfile.write("%s %s \n"%(score, eng))
                    for atom in feature:
                        outlist = [str(x) for x in atom] + ["\n"]
                        outfile.write(' '.join(outlist))
    #----------------------------------------------------
    def dumpranks(self, loopnum, limit):
        outlist = []
#        for key, item in self.groups.iteritems():
        for key, item in self.groups.items():
            total = 0.0
            for member in item:
                score = member.getscore()
                total += score
            outlist.append([key, total])
        sortlist = sorted(outlist, key=lambda x: x[1], reverse=True)

        for i, key in enumerate(sortlist[:limit]):
            with open( "rank%s.dat" % (str(key[0])), "a" ) as outfile: 
                outfile.write("%s %s\n"%(loopnum*1e-4,i+1))

        for i, key in enumerate(sortlist):
            with open( "score%s.dat" % (str(key[0])), "a" ) as outfile: 
                outfile.write("%s %s\n"%(loopnum*1e-4,key[1]))

    #----------------------------------------------------
    def Minimize(self, logfile=None):
#        sortList = sorted(self.members, key=lambda x: x.radialscore(), reverse=False)
#        cnt = 0
#        for i, obj in enumerate(sortList):
#            if cnt < self.nMinimize:
#                score = obj.optimize()
#                cnt += 1
#        if len(sortList) < self.nMinimize*2:
#            return
        
        sortList = sorted(self.members, key=lambda x: x.radialscore(), reverse=True)
        cnt = 0
        for i, obj in enumerate(sortList):
            if cnt < self.nMinimize:
                
                groupID = obj.findgroup()
                self.groups[groupID].remove(obj)
                score = obj.optimize(logfile=logfile)
                groupID = obj.findgroup()
                if groupID in self.groups:
                    self.groups[groupID].append(obj)
                else:
                    self.groups[groupID] = [obj]

                cnt += 1

    #----------------------------------------------------
