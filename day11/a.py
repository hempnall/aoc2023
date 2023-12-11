#! /usr/bin/env python
f = open("/Users/jameshook/dev/aoc2023/day11/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def empty_rows( lines ):
    return [  idx for idx, row in enumerate(lines) if not '#' in row ]

def empty_cols( lines ):
    cols=[]
    for idx in range(0,len(lines[0])):
        col=[ ln[idx] for ln in lines ]
        if not '#' in col:
            cols.append(idx)
    return cols

def galaxies(lines):
    galaxs=[]
    for row_idx, row in enumerate(lines):
        for col_idx in range(0,len(row)):
            if row[col_idx] == '#':
                galaxs.append((col_idx,row_idx))
    return galaxs

def manhatten_dist( start , end , empty_r, empty_c,exp_fact):
    x_range_min=min(start[0],end[0])
    x_range_max=max(start[0],end[0])
    y_range_min=min(start[1],end[1])
    y_range_max=max(start[1],end[1])
    x_expansions=len([ col for col in empty_c if  x_range_min < col < x_range_max ])
    y_expansions=len([ row for row in empty_r if  y_range_min < row < y_range_max ])
    return (x_range_max - x_range_min) + (exp_fact * x_expansions) + (y_range_max - y_range_min) + (exp_fact * y_expansions)

empt_r=empty_rows(lines)
print(empt_r)
empt_c=empty_cols(lines)
print(empt_c)
galaxes=galaxies(lines)
print(galaxes)

accum=0
for idx in range(len(galaxes)):
    for sub_idx in range(idx+1,len(galaxes)):
        dist=manhatten_dist(galaxes[idx],galaxes[sub_idx],empt_r,empt_c,1000000 - 1)
        accum+=dist

print(accum)