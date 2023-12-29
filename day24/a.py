#! /usr/bin/env python3
import numpy as np
from math import lcm, gcd
from itertools import combinations

f = open("/Users/jameshook/dev/aoc2023/day24/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]


MIN_POS=7
MAX_POS=27
MIN_POS=200000000000000
MAX_POS=400000000000000

def parse_hailstone( ln ):
    ln_parts = ln.split("@")
    pos=[ int( lp.strip() ) for lp in ln_parts[0].split(",") ]
    vel=[ int( lp.strip() ) for lp in ln_parts[1].split(",") ]
    return {
        "x": pos[0],
        "y": pos[1],
        "z": pos[2],
        "dx": vel[0],
        "dy": vel[1],
        "dz": vel[2]
    }

def anal_4( hs , axis):
    print(f'==== {axis} ==== ')
    for h in hs:
        print(h[axis], h[f'd{axis}'])
    print()
    pos_v=set([])
    combs=list(combinations(hs,2))

    dd = hs[1][f'd{axis}'] 
    mults=[ (h[1][axis], h[0][axis]) for h in combs ]
    RANGE_BOUNDS=6
    for m in mults:
        vel_range=range( -RANGE_BOUNDS , RANGE_BOUNDS )
        (x1, x2) = (m[0],m[1])

        for idx in vel_range:
            if idx ==0 :
                continue

            denom = dd - idx
            numer = x2 - x1

            if denom == 0:
                continue

            # if denom > 0 and numer < 0:
            #     continue

            # if numer > 0 and denom < 0:
            #     continue

            if numer % denom == 0:
                print("OK",numer, denom, idx, (numer / denom))
            else:
                print("REJECT",numer, denom, idx)

    return pos_v

    # xpos = [ h["x"] for h in hs if h["dx"]==sp ]
    # print(xpos)
    # sxpos = sorted(xpos)
    # print(sxpos)
    # if len(sxpos) > 1:
    #     print(  sxpos[1] - sxpos[0] )

def analyse_hailstones( hs , axis ):
    hist={}
    hist_hs={    }
    for h in hs:
        scoord=(h[f'd{axis}'])
        if not scoord in hist:
            hist[scoord]=1
            hist_hs[scoord]=[h]
        else:
            hist[scoord]+=1
            hist_hs[scoord].append(h)

    p = set(list(range(-10,10)))
    for h in hist:
        if hist[h] > 1:
            print(".")
            print(hist_hs[h])
            print(".")
            p = p.intersection(anal_4(hist_hs[h],axis))
    print(p)

def get_vectors( hs ):
    return np.array( [ hs["x"], hs["y"],hs["z"]]  ),np.array( [ hs["dx"], hs["dy"],hs["dz"]]  )

def get_pos_at_time( hs , t ):
    return ( hs["x"] + t * hs["dx"] , hs["y"] + t * hs["dy"] , hs["z"] + t * hs["dz"] )

def get_times( hs1, hs2 ):
    a = np.array([ [hs1["dx"], -hs2["dx"] ], [ hs1["dy"], -hs2["dy"]  ]])
    det=np.linalg.det(a)
    if det == 0:
        return None
    b = np.array([ hs2["x"] - hs1["x"] , hs2["y"] - hs1["y"] ])
    c=np.linalg.solve(a,b)
    return c

hailstones = [ parse_hailstone(ln) for ln in lines ]


COLLISIONS=0


def solve_p2( hs , a1 , a2 ):
    dax1=f'd{a1}'
    dax2=f'd{a2}'
    rows = [  [h[dax2] , -h[dax1] , -h[a2] ,h[a1],1 ]  for h in hs] 
    c = [  h[a1] * h[dax2] - h[a2] * h[dax1] for h in hs  ]
    a = np.array(rows)
    b = np.array(c)
    np.set_printoptions(suppress=False,formatter = {'float_kind':'{:f}'.format})
    c=np.linalg.solve(a,b)
    return c

for idx1 , hs1 in enumerate(hailstones):
    for idx2 in range(idx1+1, len(hailstones)):
        hs2=hailstones[idx2]
        #print(f'{hailstones[idx1]} {hailstones[idx2]}')
        times = get_times(hs1, hs2)
        if not times is None:
            if times[0] < 0 or times[1] < 0:
                pass
            else:
                the_pos = get_pos_at_time(hs1,times[0])
                if MIN_POS <= the_pos[0] <= MAX_POS and MIN_POS <= the_pos[1] <= MAX_POS:
                    COLLISIONS += 1


        # else:
        #     print(f'NONE {idx1} {idx2} ')
        #     x1,dx1 = get_vectors(hs1) 
        #     x2,dx2 = get_vectors(hs2) 

        #     print(f'{dx1} {dx2}')
        #     ratio1 = np.divide( dx1 , dx2 )
        #     ratio2 = np.divide( dx2 , dx1 )
        #     print( f'{ratio1} {ratio2}' ) 
        #     print()

# 3220230837239196647973802508966400
print(COLLISIONS)

only5hs=hailstones[10:15]

xtot=0
ytot=0
ztot=0
num=0
for x in range(len(hailstones)-5):
    only5hs=hailstones[x:x+5]
    arr_xy = solve_p2(only5hs,'x','y')
    arr_xz = solve_p2(only5hs,'x','z')
    arr_yz = solve_p2(only5hs,'y','z')
    xtot += (arr_xy[0] + arr_xz[0])
    ytot += (arr_xy[1] + arr_yz[0])
    ztot += (arr_xz[1] + arr_yz[1])
    num+=2
    print(  xtot / num , ytot / num , ztot / num )
            

print( 131633231355646 + 371683716481156 + 238674624073734 )

    