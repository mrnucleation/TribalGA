#from PoolClass import Pool
from TribalPoolClass import TribePool
#from SimpleObject import RadialObj
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

    tribeTest = TribePool()

    init = MolObject()
    '''
    coords = [
            [1, 1.0, 0.0, 6e-2],
            [1, 1.0, 1.0, 5e-2],
            [1, 1.0, 2.0, 4e-2],
            [1, 1.0, 3.0, 3e-2],
            [1, 1.0, 4.0, 2e-2],
            [1, 2.0, 0.0, 1e-1],
            [1, 2.0, 1.0, 1e-11],
            [1, 2.0, 2.0, 1e-10],
            [1, 2.0, 3.0, 1e-9],
            [1, 3.0, 0.0, 1e-7],
            [1, 3.0, 1.0, 1e-6],
            [1, 3.0, 2.0, 1e-5],
            [1, 3.0, 3.0, 1e-3]
            ]
    coords = [
            [1, 0.0, 0.0, 0.0],
            [1, 1.0, 0.0, 0.0],
            [1, 2.0, 0.0, 0.0],
            ]

    '''
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
            elif ranNum < 0.15:
                tribeTest.Famine(logfile=outfile)
            elif ranNum < 0.20:
                tribeTest.CivilWar(logfile=outfile)
            else:
                tribeTest.Mutate(logfile=outfile)

        if i%int(1e3) == 0:
            print(tribeTest)
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

