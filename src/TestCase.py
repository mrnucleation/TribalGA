from PoolClass import Pool
from SimpleObject import RadialObj
from random import random, seed
from datetime import datetime
from math import floor
#===========================================
def main():
#    tribelist = []
#    tribelist.append(Tribe())
    seed(datetime.now())

    tribeTest = Pool()
    for i in range(30):
        tribeTest.AddMember(RadialObj(initial=True))
    dummy = 0
#    hist = []
#    dr = 7.0/1000.0
#    for i in range(1000):
#        hist.append(0.0)

    for i in range(int(2e9)):
        ranNum = random()
        if ranNum < 0.00001:
            tribeTest.CivilWar(dummy)
            scorelist = tribeTest.getfeatures()
#        elif ranNum < 0.1:
#            tribeTest.Mate()
        else:
            tribeTest.Mutate()
        if i%100000 == 0:
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

