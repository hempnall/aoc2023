#! /usr/bin/env python
from functools import cmp_to_key

f = open("/Users/jameshook/dev/aoc2023/day5/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

types=["seed","soil","fertilizer","water","light","temperature","humidity","location"]
seeds=[]
seed_ranges=[]
maps={}
in_map=False

def compare_mappings( map1 , map2 ):
    return map1[1] - map2[1]

for line_no in range(0, len(lines)):
    current_line=lines[line_no]
    if not in_map:
        if current_line.startswith("seeds: "):
            seeds = [ int(seed) for seed in current_line[7::].split(" ") ]
            seed_range_count=int(len(seeds)/2)
            for idx in range(0, seed_range_count):
                seed_ranges.append([int(seeds[2 * idx]), int(seeds[2 * idx + 1])])
        if current_line.endswith(" map:"):
            map_types = current_line[:-5].split("-")
            if len(map_types)!=3:
                raise "invalid map type"
            in_map=True
            map_type=(map_types[0],map_types[2])
    else:
        if current_line == "":
            in_map=False
        else:
            map_components=[ int(mc) for mc in current_line.split(" ")]
            if len(map_components)!=3:
                raise "invalid map row"
            if not map_type in maps:
                maps[ map_type ] = [ map_components ]
            else:
                maps[ map_type ].append( map_components)
                maps[ map_type ]=sorted( maps[map_type], key=cmp_to_key(compare_mappings))


def range_overlaps( range1 , range2 ):
    return not (( range1[0] + range1[1] -1 ) < range2[0]  or range1[0] > ( range2[0] + range2[1]) -1)

def range_overlap( range1 , range2 ):
    return [ max(range1[0], range2[0]) , min(range1[1] + range1[0] , range2[1] + range2[0] ) - max(range1[0], range2[0]) ]

def process_map( src,dst, loc):
    map=maps[(src,dst)]
    for range in map:
        if range[1] <= loc < (range[1] + range[2]):
            return  range[0] + (loc - range[1])
    return loc

def process_seed( seed_loc ):
    new_seed_loc=seed_loc
    for idx in range(0, len(types)-1):
        new_seed_loc=process_map(types[idx],types[idx+1],new_seed_loc)
    return new_seed_loc

def pprocess_seed_range( r , s , d):
    print(f'{r} {s} {d}')

def identity( range ):
    return range

def transform( map, range):
    new_range=[map[0] + range[0]-map[1],range[1]]
    return new_range

def get_ranges( range, mappings  ):
    new_ranges=[]
    range_low=range[0]
    range_high=range_low+range[1]-1
    for map in mappings:
        map_low=map[1]
        map_high=map[1]+map[2]-1
        if map_high < range_low or map_low > range_high:
            continue
        elif map_low > range_low:
            size=map_low-range_low
            new_ranges.append(identity([range_low,size]))
            range_low+=size
            size=min(map[2],range_high-range_low+1)
            new_ranges.append(transform(map,[range_low,size]))
            range_low+=size
        elif map_low <= range_low:
            size=min(map[2],1 + min(range_high,map_high)  - range_low)
            new_ranges.append(transform(map,[max(map_low,range_low),size]))
            range_low += size
        else:
            raise "NOOOOOOO!!!!"
        
    if range_low <= range_high:
        new_ranges.append(identity([range_low,range_high-range_low + 1]))

    return new_ranges

def process_seed_ranges( ranges , idx ):
    source_stage=types[idx]
    dest_stage=types[idx+1]
    mapping=maps[(source_stage,dest_stage)]
    seed_ranges=[ get_ranges( rng , mapping) for rng in ranges]
    return [ seed_range for seed_range_arr  in seed_ranges for seed_range in seed_range_arr ]

#seed_ranges=[[74,14]]
for idx in range(0,len(types)-1):
    seed_ranges = process_seed_ranges(seed_ranges,idx)
    
print(min([a[0] for a in seed_ranges]))