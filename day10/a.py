#! /usr/bin/env python
import sys
sys.setrecursionlimit(15000)
f = open("/Users/jameshook/dev/aoc2023/day10/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]
LEFTS=set([])
RIGHTS=set([])
PATH=[]


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

NORTH=(0,-1)
SOUTH=(0,1)
EAST=(1,0)
WEST=(-1,0)

PIPE_SQUARES=set([])
PIPE_SQUARES_DIR={
    NORTH: set([]),
    EAST: set([]),
    WEST: set([]),
    SOUTH: set([])
}

ALL_DIRS=[NORTH,SOUTH,EAST,WEST]

dirs={
    "|": [NORTH,SOUTH],
    "-": [EAST,WEST],
    "L": [NORTH,EAST],
    "J": [NORTH,WEST],
    "7": [SOUTH,WEST],
    "F": [SOUTH,EAST],
}

new_dirs={
    (NORTH,"|"): NORTH,
    (NORTH,"7"): WEST,
    (NORTH,"F"): EAST,
    (EAST,"-"):EAST,
    (EAST,"J"):NORTH,
    (EAST,"7"):SOUTH,
    (SOUTH,"|"):SOUTH,
    (SOUTH,"L"):EAST,
    (SOUTH,"J"):WEST,
    (WEST,"-"):WEST,
    (WEST,"L"):NORTH,
    (WEST,"F"):SOUTH
}

CORNERS={
    ("F",WEST): [SOUTH,WEST],
    ("F", NORTH): [EAST,NORTH],
    ("L",SOUTH):[EAST,SOUTH],
    ("L",WEST):[NORTH,WEST],
    ("J",EAST):[NORTH,EAST],
    ("J",SOUTH):[SOUTH,WEST],
    ("7",EAST):[EAST,SOUTH],
    ("7",NORTH):[NORTH, WEST],
    ("-",EAST):[EAST],
    ("-",WEST):[WEST],
    ("|",NORTH): [NORTH],
    ("|",SOUTH): [SOUTH]
}


OPP_DIRS={
    NORTH: SOUTH,
    EAST: WEST,
    WEST: EAST,
    SOUTH: NORTH
}

def add_tuple( f , s):
    return (f[0]+s[0],f[1]+s[1])

def find_start( lines ):
    for row, ln in enumerate(lines):
        pos = ln.find("S")
        if pos != -1:
            return (pos,row)
        
def find_first_steps( start_pos ):
    poss_steps=[]
    for dir in ALL_DIRS:
        new_coord=add_tuple(start_pos,dir)
        char_at_adj=lines[new_coord[1]][new_coord[0]]
        if (dir,char_at_adj) in new_dirs:
            poss_steps.append(dir)
    return poss_steps

def step( pos , dir , start, count ):
    new_coord=add_tuple(pos,dir)
    char_at_adj=lines[new_coord[1]][new_coord[0]]
    if char_at_adj == 'S' and count> 1:
        pass
    else:
        PATH.append(new_coord)
        PIPE_SQUARES.add(new_coord)
        ORIENT=CORNERS[(char_at_adj,dir)]
        for ort in ORIENT:
            PIPE_SQUARES_DIR[ort].add(new_coord)
        
        next_dir=new_dirs[(dir,char_at_adj)]    
        step( new_coord ,next_dir ,start, count+1 )

START=find_start(lines)
PIPE_SQUARES.add(START)
PATH.append(START)
get_first_step=find_first_steps(START)
step(START, get_first_step[0], START, 1)

def flood_fill( INSIDE_OUTSIDE , OUTSIDE_INSIDE, start ):
    if start[0] in [-1, len(lines[0])] or start[1] in [-1, len(lines)]:
        return
    if start in INSIDE_OUTSIDE:
        return
    if start in OUTSIDE_INSIDE:
        raise "ooooooooops"
    if start in PIPE_SQUARES:
        return
    INSIDE_OUTSIDE.add(start)
    for dir in ALL_DIRS:
        flood_fill( INSIDE_OUTSIDE , OUTSIDE_INSIDE, add_tuple(start,dir))

for idx in range(0, len(PATH)):
    location=PATH[idx]
    if location in PIPE_SQUARES_DIR[NORTH]:
        flood_fill( LEFTS , RIGHTS, add_tuple(location,WEST))
        flood_fill( RIGHTS , LEFTS , add_tuple(location,EAST))
    elif location in PIPE_SQUARES_DIR[SOUTH]:
        flood_fill( RIGHTS , LEFTS, add_tuple(location,WEST))
        flood_fill( LEFTS , RIGHTS, add_tuple(location,EAST))
    elif location in PIPE_SQUARES_DIR[EAST]:
        flood_fill( RIGHTS , LEFTS, add_tuple(location,SOUTH))
        flood_fill( LEFTS , RIGHTS, add_tuple(location,NORTH))
    elif location in PIPE_SQUARES_DIR[WEST]:
        flood_fill( LEFTS , RIGHTS, add_tuple(location,SOUTH))
        flood_fill( RIGHTS , LEFTS, add_tuple(location,NORTH))

print( len(LEFTS))
print( len(RIGHTS))
print( len(PIPE_SQUARES))

print( len(LEFTS) + len(RIGHTS) + len(PIPE_SQUARES))
print( 140 ** 2)

for row_idx in range(0,len(lines)):
    for col_idx in range(0,len(lines[row_idx])):
        if (col_idx,row_idx) in LEFTS:
            print("L",end = '')
        elif (col_idx,row_idx) in RIGHTS:
            print("R",end = '')
        elif (col_idx,row_idx) in PIPE_SQUARES:
            print(".",end = '')
        else:
            print("*",end = '')

    print()


