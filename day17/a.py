#! /usr/bin/env python3
import sys
from heapq import heappop, heappush
f = open("/Users/jameshook/dev/aoc2023/day17/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

path_heap=[]


def block_val( blk ):
    return int( lines[blk[1]][blk[0] ])

def in_bounds( pos ):
    if pos[0] < 0 or pos[0] >= len(lines[0]):
        return False
    if pos[1] < 0 or pos[1] >= len(lines):
        return False
    return True

def add_vec( vec1 , vec2):
    return ( vec1[0] + vec2[0], vec1[1] + vec2[1])

def mult_vec( vec, mult):
    return ( vec[0] * mult, vec[1] * mult)

def end_point():
    return ( len(lines[0]) - 1  , len(lines) - 1 )

def is_end_point( loc ):
    return loc == end_point()

POSS_DIRS=[(1,0),(0,1),(-1,0),(0,-1)]
VISITED=set()

PATH_HEAP=[ (0,(0,0),(0,0),0) ]

while PATH_HEAP:
    hl , pos, dir, streak = heappop(PATH_HEAP)

    if is_end_point(pos):
        print(hl)
        break

    if (pos, dir, streak) in VISITED:
        continue

    VISITED.add((pos,dir,streak))

    if streak < 9 and dir != (0,0):
        next_pos = add_vec(pos,dir)
        if in_bounds(next_pos):
            heappush(PATH_HEAP,(hl + block_val(next_pos), next_pos, dir , streak + 1 ))

    if streak >= 3 or dir == (0,0):
        for ndir in POSS_DIRS:
            if ndir != dir and ndir != ( -dir[0],-dir[1]):
                min_dist = mult_vec( ndir , 3)
                if not in_bounds( add_vec( pos, min_dist) ):
                    continue
                next_pos = add_vec(pos,ndir)
                if in_bounds(next_pos):
                    heappush(PATH_HEAP,(hl + block_val(next_pos), next_pos, ndir , 0))
    


