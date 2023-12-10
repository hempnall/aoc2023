#! /usr/bin/env python
import sys
sys.setrecursionlimit(15000)
f = open("/Users/jameshook/dev/aoc2023/day10/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

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
    print(count)
    new_coord=add_tuple(pos,dir)
    char_at_adj=lines[new_coord[1]][new_coord[0]]
    if char_at_adj == 'S' and count> 1:
        print(f'------back {count}')
        print(count/2)
    else:
        next_dir=new_dirs[(dir,char_at_adj)]    
        step( new_coord ,next_dir ,start, count+1 )

START=find_start(lines)
get_first_step=find_first_steps(START)
print(START)
print(get_first_step)
step(START, get_first_step[0], START, 1)
step(START, get_first_step[1], START, 1)

