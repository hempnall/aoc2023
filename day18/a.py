#! /usr/bin/env python3
import sys
sys.setrecursionlimit(95000)

f = open("/Users/jameshook/dev/aoc2023/day18/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]
EDGE_LOCS=set([])

INSTRUCTIONS = [ l.split(" ") for l in lines ]
DIRS={
    "R": (1,0),
    "L": (-1,0),
    "U": (0,-1),
    "D": (0,1)
}

DIRS={
    "0": (1,0),
    "2": (-1,0),
    "3": (0,-1),
    "1": (0,1)
}

CUR_LOC=(0,0)
EDGE_LOCS_ARR=[CUR_LOC]
LEN_BORDER=1

def add_vec( v1 , v2 ):
    return ( v1[0] + v2[0] , v1[1] + v2[1])

def mult_vec( v1, k ):
    return ( v1[0] * k , v1[1] * k )

def top_left( sqs ):
    r = min([  cn[0] for cn in sqs ]) - 1
    c = min([  cn[1] for cn in sqs ]) - 1
    return (r,c)

def bottom_right( sqs ):
    r = max([  cn[0] for cn in sqs ]) + 1
    c = max([  cn[1] for cn in sqs ]) + 1
    return (r,c)

def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def explode_xy(xy):
    xl=[]
    yl=[]
    for i in range(len(xy)):
        xl.append(xy[i][0])
        yl.append(xy[i][1])
    return xl,yl

def shoelace_area(x_list,y_list):
    a1,a2=0,0
    x_list.append(x_list[0])
    y_list.append(y_list[0])
    for j in range(len(x_list)-1):
        a1 += x_list[j]*y_list[j+1]
        a2 += y_list[j]*x_list[j+1]
    l=abs(a1-a2)/2
    return l

def flood_fill( fill, loc , top_l , bottom_r ):
    if loc[0] < top_l[0]:
        return
    if loc[0] > bottom_r[0]:
        return
    if loc[1] < top_l[1]:
        return
    if loc[1] > bottom_r[1]:
        return   
    if loc in fill:
        return
    if loc in EDGE_LOCS:
        return
    fill.add(loc)
    for d in DIRS:
        new_loc = add_vec(loc , DIRS[d])
        flood_fill( fill, new_loc, top_l, bottom_r)

def area( tl , br ):
    return (1 + br[0] - tl[0] ) * (1 + br[1] - tl[1] )

for INST in INSTRUCTIONS:
    STEP_DIR=DIRS[INST[2][-2]]
    LENGTH=int(INST[2][2:-2],16)
    LEN_BORDER += LENGTH
    CUR_LOC = add_vec( CUR_LOC , mult_vec( STEP_DIR, LENGTH ))
    EDGE_LOCS_ARR.append(CUR_LOC)


print(len(EDGE_LOCS_ARR))
tl = top_left(EDGE_LOCS_ARR)
br= bottom_right(EDGE_LOCS_ARR)
print(f'{tl} {br}')
FILL=set([])
a = PolygonArea( EDGE_LOCS_ARR)
xy_e=explode_xy(EDGE_LOCS_ARR)

A=shoelace_area(xy_e[0],xy_e[1])

print(f'area={a} {A} {A+( LEN_BORDER / 2)}')
