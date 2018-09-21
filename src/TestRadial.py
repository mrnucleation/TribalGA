#from PoolClass import Pool
from TribalPoolClass import TribePool
from SimpleObject import RadialObj
#from MoleculeObject import MolObject
#from ClusterObject import MolObject
from random import random, seed
from datetime import datetime
from math import floor
#===========================================
def main():
#    tribelist = []
#    tribelist.append(Tribe())
    seed(datetime.now())

    tribeTest = TribePool()
    init = RadialObj()

#    init.setfeature(coords)
    init.computescore()
    result = init.safetycheck()
    if not result:
        print("Initial State not valid")
        quit()
    print("Computed Score")
    tribeTest.AddMember(init)
#    tribeTest.dumpfeatures()
    outfile = open("log.out", "w")

    dummy = 0
#    hist = []
#    dr = 7.0/1000.0
#    for i in range(1000):
#        hist.append(0.0)
    print("Start Simulation")
    for i in range(int(5e6)):
        ranNum = random()
        if len(tribeTest.members) >= tribeTest.maxmem:
            if len(tribeTest.groups.keys()) == 1:
                tribeTest.Famine(logfile=outfile)
            else:
                tribeTest.CivilWar(logfile=outfile)

        else:
#            tribeTest.Mutate(logfile=outfile)
            if ranNum < 0.1:
                tribeTest.Mate(logfile=outfile)
            elif ranNum < 0.11:
                tribeTest.Famine(logfile=outfile)
            elif ranNum < 0.12:
                tribeTest.CivilWar(logfile=outfile)
            else:
                tribeTest.Mutate(logfile=outfile)

        if i%int(1e3) == 0:
            print(tribeTest)
            if i%int(1e4) == 0:
#                tribeTest.Minimize(logfile=outfile)
                print("Coordinates Dummped")
#                tribeTest.dumpfeatures()

#    tribeTest.dumpfeatures()

#    norm = 0.0
#    for i, item in enumerate(hist):
#        norm += item
#    outfile = open("Hist.dat", "w")
#    for i, item in enumerate(hist):
#        outfile.write(' '.join(str(x) for x in [i*dr, item/(dr*norm), "\n"]))
#        print i*dr, item/norm



if __name__ == "__main__":
    main()

