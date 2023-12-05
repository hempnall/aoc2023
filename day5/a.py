#! /usr/bin/env python
f = open("sample.txt","r")
lines = [ l.strip() for l in f.readlines() ]

types=["seed","soil","fertilizer","water","light","temperature","humidity","location"]
seeds=[]
seed_ranges=[]
maps={}
in_map=False

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

new_seed_locs=[]
for seed_range in seed_ranges:
    for idx in range( seed_range[0], seed_range[0] + seed_range[1]):
        new_seed_locs.append( process_seed(idx))

#new_seed_locs=[ process_seed( sl ) for sl in seeds ]
print(new_seed_locs)
print(min(new_seed_locs))
    

