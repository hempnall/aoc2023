#! /usr/bin/env python
import sys
sys.setrecursionlimit(15000)
f = open("/Users/jameshook/dev/aoc2023/day16/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

VERTICALS=set([])
HORIZONTALS=set([])
BACKSLASHES=set([])
FORWSLASHES=set([])
PATHITEMS=set([])

OUTCOMES={
    ((0,1),'-'):[ (1,0),(-1,0)],
    ((0,-1),'-'): [(1,0),(-1,0)],
    ((1,0),'-'): [(1,0)],
    ((-1,0),'-'): [(-1,0)],
    ((0,1),'|'): [(0,1)],
    ((0,-1),'|'): [(0,-1)],
    ((1,0),'|'):[ (0,1),(0,-1)],
    ((-1,0),'|'):[ (0,1),(0,-1)],
    ((0,1),'/'):[ (-1,0)],
    ((0,-1),'/'): [(1,0)],
    ((1,0),'/'):[ (0,-1)],
    ((-1,0),'/'): [(0,1)],
    ((1,0),'\\'):[ (0,1)],
    ((-1,0),'\\'):[ (0,-1)],
    ((0,1),'\\'):[ (1,0)],
    ((0,-1),'\\'):[ (-1,0)]        
}

def in_bounds( loc):
    if loc[0]<0 or loc[0]>=len(lines[0]):
        return False
    if loc[1]<0 or loc[1]>=len(lines):
        return False
    return True

def parse_input( lines ):
    for ridx, line in enumerate(lines):
        for cidx , c in enumerate(line):
            CELL=(cidx,ridx)
            if c == '-':
                HORIZONTALS.add(CELL)
            elif c == '|':
                VERTICALS.add(CELL)
            elif c=='/':
                FORWSLASHES.add(CELL)
            elif c=='\\':
                BACKSLASHES.add(CELL)
            else:
                pass

def add_vec( vec1, vec2):
    return ( vec1[0] + vec2[0] , vec1[1] + vec2[1])


def PATHLOCS():
    return set([ k[0] for k in PATHITEMS ])

def show_paths():
    keys = PATHLOCS()
    for row_idx in range(len(lines)):
        for col_idx in range(len(lines[0])):
            if (col_idx,row_idx) in keys:
                print('#',end='')
            else:
                print('.',end='')
        print()

def start_path( loc , dir ):
   
    if (loc,dir) in PATHITEMS:
        return 
    if not in_bounds(loc):
        return
    
    PATHITEMS.add((loc,dir))
    
    new_dirs=[dir]
    if loc in HORIZONTALS:
        new_dirs=OUTCOMES[(dir,'-')]
    elif loc in VERTICALS:
        new_dirs=OUTCOMES[(dir,'|')]
    elif loc in BACKSLASHES:
        new_dirs=OUTCOMES[(dir,'\\')]
    elif loc in FORWSLASHES:
        new_dirs=OUTCOMES[(dir,'/')]


    for beam_dir in new_dirs:
        new_loc=add_vec(loc,beam_dir)   
        start_path(new_loc,beam_dir)


parse_input(lines)
start_path((0,0),(1,0))
print(len(PATHLOCS()))

energies=[]
for idx in range(len(lines[0])):
    PATHITEMS=set([])
    start_path((idx,0),(0,1))
    energies.append(len(PATHLOCS()))
    PATHITEMS=set([])
    start_path((idx,len(lines)-1),(0,-1))
    energies.append(len(PATHLOCS()))

for idx in range(len(lines)):
    PATHITEMS=set([])
    start_path((idx,len(lines[0])-1),(-1,0))
    energies.append(len(PATHLOCS()))
    PATHITEMS=set([])
    start_path((idx,0),(1,0))
    energies.append(len(PATHLOCS()))

print(max(energies))