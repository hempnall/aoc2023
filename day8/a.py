#! /usr/bin/env python
from math import lcm

f = open("/Users/jameshook/dev/aoc2023/day8/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

lr_inst=lines[0]
map_lines=lines[2:]
lr_ptr=0 
cur_loc="AAA"
step_count=0

map = {
    ln[0:3]: {
        "L": ln[7:10],
        "R": ln[12:15]
    } for ln in map_lines
}

def next_lr_ptr( cur_ptr ):
    return (cur_ptr + 1) % len(lr_inst)

def next_loc( cur_ptr , loc ):
    global lr_ptr
    dir=lr_inst[cur_ptr]
    lr_ptr=next_lr_ptr(cur_ptr)
    return map[loc][dir]

def next_loc_with_dir( cur_ptr , loc ):
    dir=lr_inst[cur_ptr]
    return map[loc][dir]

nodes_ending_in_a=[
    nd for nd in map.keys() if nd[2] == "A"
]

def step_count( start_loc  ):
    step_count=0
    cur_ptr=0
    while start_loc[2] != "Z":
        start_loc = next_loc(cur_ptr,start_loc)
        cur_ptr=next_lr_ptr(cur_ptr)
        step_count +=1
    return step_count

step_counts = [
    step_count( nd ) for nd in nodes_ending_in_a
]

print(step_counts)
print(lcm(*step_counts))