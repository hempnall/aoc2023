#! /usr/bin/env python3
import sys
import math

sys.setrecursionlimit(15000)
f = open("/Users/jameshook/dev/aoc2023/day21/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

MAXSTEPS=26501365
LASTBLOCK=202300
HALFLAST= int(LASTBLOCK / 2)
PENBLOCK=202299
LASTLEG=66
FIRSTLEG=65

STEPSTOTOP=FIRSTLEG + (PENBLOCK * 131) + 1
STEPSTOA= STEPSTOTOP + LASTLEG
STEPSTOB = STEPSTOA - 131



def count_of_dots( lines ):
    return sum([len([  ds for ds in line if ds != "#"] )  for line in lines ])

def width():
    return len(lines[0])

def height():
    return len(lines)

def half_width():
    return math.floor( width() / 2 )

def half_height():
    return math.floor( height() / 2 )

def in_bounds( pos ):
    if pos[0] < 0 or pos[0] >= width():
        return False
    if pos[1] < 0 or pos[1] >= height():
        return False
    return True

def parse_island( lines ):
    ROCKS=set([])
    STARTPOS=None
    for ridx, ln in enumerate(lines):
        for cidx, c in enumerate(ln):
            if c == "S":
                STARTPOS=(cidx,ridx)
            if c == "#":
                ROCKS.add((cidx,ridx))
    return STARTPOS,ROCKS

def add_vec( v1 , v2 ):
    return ( v1[0] + v2[0], v1[1] + v2[1])

s,ROCKS = parse_island( lines )

def count_of_odd_even_blocks( n ):
    H=n ** 2
    L = (n-1 ) ** 2
    if n % 2 != 0:
        return H , L
    else:
        return L, H


def flood_fill( pos , odds , evens , rocks , iseven ):
    if pos in rocks:
        return
    if not in_bounds(pos):
        return
    if iseven:
        if pos in evens:
            return
        evens.add(pos)
    else:
        if pos in odds:
            return
        odds.add(pos)   
    for D in DIRS:
        flood_fill( add_vec(pos , D),odds,evens,rocks,not iseven)

def mod_pos( pos ):
    return ( pos[0] % len(lines[0]), pos[1] % len(lines) )

def count_odds_and_evens( lines ):
    odds=set([])
    evens=set([])
    for ridx, ln in enumerate(lines):
        if ridx == 0:
            for cidx , _ in enumerate(ln):
                if cidx % 2 == 0:
                    evens.add((cidx,ridx))
                else:
                    odds.add((cidx,ridx))
        else:
            for cidx , c in enumerate(ln):
                if c == "#":
                    continue
                prev=(cidx,ridx-1)
                coord=(cidx,ridx)
                if prev in evens:
                    odds.add(coord)
                if prev in odds:
                    evens.add(coord)
                if coord in odds and coord in evens:
                    raise "whoops"
    return len(odds),len(evens)

DIRS=[(0,1),(1,0),(-1,0),(0,-1)]

def disp_stats():
    ODDS=set([])
    EVENS=set([])
    flood_fill(s,ODDS,EVENS,ROCKS,True)
    leno=len(ODDS)
    lene=len(EVENS)
    lenr=len(ROCKS)
    size=width() ** 2
    return leno,lene

def calc_diamond(start,maxs):
    print(f'{start} {maxs}')
    SEEN=set([])
    PATHS=[(start,0)]
    MAX_STEPS=maxs
    FINAL_DESTS=set([])

    while PATHS:
        cur_step=PATHS.pop(0)
        if cur_step in SEEN:
            continue
        if cur_step[1] == MAX_STEPS:
            FINAL_DESTS.add(cur_step[0])
            continue
        SEEN.add(cur_step)
        for D in DIRS:
            new_pos=add_vec(cur_step[0],D)
            if not in_bounds(new_pos) or new_pos in ROCKS:
                continue
            else:
                PATHS.append((new_pos,cur_step[1]+1))
    print(len(FINAL_DESTS))
    return len(FINAL_DESTS)



def cs(n):
    O,E = count_of_odd_even_blocks(n)
    print(f'O={O} E={E}')

cs(1)
cs(2)
cs(3)
cs(LASTBLOCK)



TOP = calc_diamond((65,height()-1),MAXSTEPS - STEPSTOTOP)
TOPLA = calc_diamond((width()-1,height()-1),MAXSTEPS - STEPSTOA)
TOPLB = calc_diamond((width()-1,height()-1),MAXSTEPS - STEPSTOB)
LEFT=calc_diamond((width()-1,65),MAXSTEPS - STEPSTOTOP)
BOTLA = calc_diamond((width()-1,0),MAXSTEPS - STEPSTOA)
BOTLB = calc_diamond((width()-1,0),MAXSTEPS - STEPSTOB)
BOT = calc_diamond((65,0),MAXSTEPS - STEPSTOTOP)
BOTRA = calc_diamond((0,0),MAXSTEPS - STEPSTOA)
BOTRB = calc_diamond((0,0),MAXSTEPS - STEPSTOB)
RIGHT = calc_diamond((0,65),MAXSTEPS - STEPSTOTOP)
TOPRA = calc_diamond((0,height()-1),MAXSTEPS - STEPSTOA)
TOPRB = calc_diamond((0,height()-1),MAXSTEPS - STEPSTOB)

EDGES_TL = ( LASTBLOCK * TOPLA ) + (PENBLOCK * TOPLB)
EDGES_BL = ( LASTBLOCK * BOTLA ) + (PENBLOCK * BOTLB)
EDGES_BR = ( LASTBLOCK * BOTRA ) + (PENBLOCK * BOTRB)
EDGES_TR = ( LASTBLOCK * TOPRA ) + (PENBLOCK * TOPRB)
ENDS = TOP + LEFT + RIGHT + BOT
EDGES = EDGES_BL + EDGES_BR + EDGES_TL + EDGES_TR + ENDS
o,e = disp_stats()
print(f'{o} {e}')

CO, CE = count_of_odd_even_blocks( LASTBLOCK)
TOTAL = EDGES + (CO * o) + (CE * e)
print(TOTAL)
