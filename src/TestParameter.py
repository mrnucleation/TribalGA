#from PoolClass import Pool
#from TribalPoolClass import TribePool
from MultiObjPoolClass import MultiPool
#from SimpleObject import RadialObj
#from MoleculeObject import MolObject
from ParameterSet import ParameterObj
from random import random, seed
from datetime import datetime
from math import floor
#===========================================
def main():
    seed(datetime.now())

    tribeTest = MultiPool(nParameters=1, nObj=3)
    tribeTest.setweights([1.0, 1.0, 100.0])
    init = ParameterObj(nParameters=1, nObj=3)
#    coords = [ 1.0 , 2.0]
    coords = [ 0.0 ]
    init.setfeature(coords)
#    init.setmax([5.0, 5.0])
#    init.setmin([0.0, 0.0])

    init.setmin([0.0])
    init.setmax([5.0])
    init.computescore()
    tribeTest.AddMember(init)


    dummy = 0
    print "Start Simulation"
    print tribeTest
    for i in range(int(2e5)):
        ranNum = random()
        if ranNum < 0.01:
            tribeTest.CivilWar(dummy)
        elif ranNum < 0.3:
            tribeTest.Mate()
        else:
            tribeTest.Mutate()
        if i%int(1e3) == 0:
            print tribeTest
       
    print tribeTest
#    norm = 0.0
#    for i, item in enumerate(hist):
#        norm += item
#    outfile = open("Hist.dat", "w")
#    for i, item in enumerate(hist):
#        outfile.write(' '.join(str(x) for x in [i*dr, item/(dr*norm), "\n"]))
#        print i*dr, item/norm



if __name__ == "__main__":
    main()

