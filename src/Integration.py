from scipy import integrate
from numpy import inf
from math import sin, pi, exp, log

def probFunc(r, temp):
    return r * exp(-engFunc(r)/temp)

def engFunc(r):
#    return 20.0*((r-1.0)**2 * (r-5.0)**2 + 0.2*(r-1.0)**2)
    return 4.0*(1.0/r**12 - 1.0/r**6)

def main():
    nbin = 50
    dx = 5.0/nbin
    prob = []
    temp = 0.8
    args = temp
    norm, blah = integrate.quad(probFunc, 0, 7.0, args=args)
    for i in range(nbin):
        x1 = i*dx
        x2 = (i+1)*dx
        area, blah = integrate.quad(probFunc, x1, x2, args=args)
#        print x1, x2, area/norm
        if area > 0.0:
            prob.append([x1,-log(area/norm)])
    outfile = open("exact.dat", "w")
    for item in prob:
        outfile.write(' '.join([str(x) for x in item] + ["\n"]))




if __name__ == "__main__":
    main()
