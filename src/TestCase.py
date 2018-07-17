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
    coords = [
            [1, 0.0, 0.0, 0.0],
            [1, 1.0, 1.0, 0.0],
            [1, 1.0, 2.0, 0.0],
            [1, 1.0, 3.0, 0.0],
            [1, 1.0, 4.0, 0.0],
            [1, 2.0, 0.0, 0.0],
            [1, 2.0, 1.0, 0.0],
            [1, 2.0, 2.0, 0.0],
            [1, 2.0, 3.0, 0.0],
            [1, 3.0, 0.0, 0.0],
            [1, 3.0, 1.0, 0.0],
            [1, 3.0, 2.0, 0.0],
            [1, 3.0, 3.0, 0.0]
            ]
    init.setfeature(coords)
    init.computescore()
    result = init.safetycheck()
    if not result:
        quit()
    print "Computed Score"
    tribeTest.AddMember(init)
#    quit()

#    tribeTest.dumpfeatures()
#    quit()
#    for i in range(30):
#        tribeTest.AddMember(RadialObj(initial=True))

    dummy = 0
#    hist = []
#    dr = 7.0/1000.0
#    for i in range(1000):
#        hist.append(0.0)
    print "Start Simulation"
    for i in range(int(5e7)):
        ranNum = random()
        if len(tribeTest.members) >= tribeTest.maxmem:
            if len(tribeTest.groups.keys()) == 1:
                tribeTest.Famine(dummy)
            else:
                if random() > 0.8:
                    tribeTest.Famine(dummy)
                else:
                    tribeTest.CivilWar(dummy)

        else:
            tribeTest.Mutate()
#            if ranNum < 1e-6:
#                tribeTest.CivilWar(dummy)
#                scorelist = tribeTest.getfeatures()
#            else:
#                tribeTest.Mutate()
        if i%int(1e3) == 0:
            print tribeTest

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

