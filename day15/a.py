#! /iusr/bin/env python
import sys
from collections import OrderedDict
f = open("/Users/jameshook/dev/aoc2023/day15/input.txt","r")
line = [ l.strip() for l in f.readlines() ][0]

steps=line.split(",")


def hash_for_step( step, idx , curr  ):
    if idx == len(step):
        return curr
    acode=ord(step[idx])
    new_val = ( ( curr + acode ) * 17 ) % 256  
    return hash_for_step( step, idx + 1 , new_val)

def process_step( step, boxes ):
    if step.endswith("-"):
        id=step[0:-1]
        hash=hash_for_step(id,0,0)
        if id in boxes[hash]:
            boxes[hash].pop(id)
    else:
        parts=step.split("=")
        if len(parts) != 2:
            print(parts)
            raise "ooops"
        else:
            hash=hash_for_step(step[0:-2],0,0)
            boxes[hash][parts[0]]=int(parts[1])
            #print(f'= {hash_for_step(step[0:-2],0,0)}')


    


boxes = [ OrderedDict() for x in range(256)]
hashes = [ process_step(step, boxes) for step in steps ]

# print(sum(hashes))
total=0
for bidx in range(256):
    if len(boxes[bidx]) > 0:
        for lidx, x in enumerate(boxes[bidx]):
            print(f'{x} {bidx} {lidx} {boxes[bidx][x]}')
            total += (bidx + 1) * (lidx + 1) * boxes[bidx][x]
    
print(total)