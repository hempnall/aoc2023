#! /usr/bin/env python
from functools import cmp_to_key

maps = [
    [ 50, 98, 2],
    [ 52, 50, 48]
]

ranges = [
    [ 0 , 100 ],
    [ 79 , 14 ],
    [ 55 , 13 ],
    [130,10],
    [25,50],
    [25,200],
    [98,1],
    [99,1],
    [60,10]
]

def dump_range( range ):
    print(f'start={range[0]} size={range[1]} end={range[0] + range[1] -1}')

def identity( range ):
    print(f'identity {range}')
    return range

def transform( map, range):
    new_range=[map[0] + range[0]-map[1],range[1]]
    print(f'map {map} {range} -> {new_range}')
    return new_range

def get_ranges( range, mappings  ):
    new_ranges=[]
    range_low=range[0]
    range_high=range_low+range[1]-1
    for map in mappings:
        map_low=map[1]
        map_high=map[1]+map[2]-1
        if map_high < range_low or map_low > range_high:
            print("no")
            continue
        elif map_low > range_low:
            size=map_low-range_low
            new_ranges.append(identity([range_low,size]))
            range_low+=size
            size=min(map[2],range_high-range_low+1)
            new_ranges.append(transform(map,[range_low,size]))
            range_low+=size
        elif map_low <= range_low:
            size=min(map[2],range_high-range_low+1)
            new_ranges.append(transform(map,[max(map_low,range_low),size]))
            range_low += size
        else:
            raise "NOOOOOOO!!!!"
        
    if range_low <= range_high:
        new_ranges.append(identity([range_low,range_high-range_low + 1]))

    return new_ranges

def compare_mappings( map1 , map2 ):
    return map1[1] - map2[1]
smaps=sorted( maps, key=cmp_to_key(compare_mappings))
print(smaps)
for range in ranges:
    print("======")
    print(range)
    new_ranges=get_ranges(range,smaps)
    print(new_ranges)
