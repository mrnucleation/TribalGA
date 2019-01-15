#from PoolClass import Pool
from TribalPoolClass import TribePool
#from SimpleObject import RadialObj
from MultiObjPoolClass import MultiPool
from MoleculeObject import MolObject
from ClusterObject import MolObject
from random import random, seed
from datetime import datetime
from math import floor
#===========================================
def main():
#    tribelist = []
#    tribelist.append(Tribe())
    seed(datetime.now())

    tribeTest = MultiPool(nParameters=1, nObj=1)
    tribeTest.setweights([1.0])


    init = MolObject()
    coords = []
    with open("incoords.dat", "r") as infile:
        for line in infile:
            try:
                col = line.split()
                col = [int(col[0])] + [float(x) for x in col[1:]]
            except:
                continue
            coords.append(col)


    init.setfeature(coords)
    init.computescore()
    result = init.safetycheck()
    if not result:
        print("Initial State not valid")
        quit()
    print("Computed Score")
    tribeTest.AddMember(init)
#    quit()

    tribeTest.dumpfeatures()
#    quit()
#    for i in range(30):
#        tribeTest.AddMember(RadialObj(initial=True))

    outfile = open("log.out", "w")

    dummy = 0
#    hist = []
#    dr = 7.0/1000.0
#    for i in range(1000):
#        hist.append(0.0)
    print("Start Simulation")
    for i in range(int(5e9)):
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
            elif ranNum < 0.101:
                tribeTest.Famine(logfile=outfile)
            elif ranNum < 0.1011:
                tribeTest.CivilWar(logfile=outfile)
            else:
                tribeTest.Mutate(logfile=outfile)

        if i%int(1e3) == 0:
            print(tribeTest)
            tribeTest.dumpranks(i,5)
            if i%int(1e4) == 0:
#                tribeTest.Minimize(logfile=outfile)
                print("Coordinates Dummped")
                tribeTest.dumpfeatures()

    tribeTest.dumpfeatures()

#    norm = 0.0
#    for i, item in enumerate(hist):
#        norm += item
#    outfile = open("Hist.dat", "w")
#    for i, item in enumerate(hist):
#        outfile.write(' '.join(str(x) for x in [i*dr, item/(dr*norm), "\n"]))
#        print i*dr, item/norm



if __name__ == "__main__":
    main()

