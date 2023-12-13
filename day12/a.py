#! /usr/bin/env python
import sys
import copy
sys.setrecursionlimit(15000)
f = open("/Users/jameshook/dev/aoc2023/day12/sample3.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def parse_line1( line ):
    parts=line.split(" ")
    nums=[ int(n) for n in parts[1].split(",") ]
    grps=[ grp for grp in parts[0].split(".") if grp != '' ]
    return (grps,nums)

def parse_line2( line ):
    parts=line.split(" ")
    nums=[ int(n) for n in parts[1].split(",") ]
    new_line="?".join([parts[0] for i in range(5)])
    new_nums=[*nums,*nums,*nums,*nums,*nums]
    grps=[ grp for grp in new_line.split(".") if grp != '' ]
    return (grps,new_nums)

plines=[ parse_line1(ln) for ln in lines]

answer_cache={}

def all_combs_of_line( line , start , grps, gidx, tot, cumul = '' ):
    if start == len(line) or gidx == len(grps):
        print(f'{line} {start} {gidx} {grps} {cumul}')
        if "#" in line[start:]:
            print(f'{line[start:]}')
            return tot
        if gidx < len(grps) :
            return tot
        print("=")
        return tot + 1

    cur_grp_len=grps[gidx]
    len_word=len(line) - start
    min_required_space=sum(grps[gidx:]) + (len(grps[gidx:]) -1)
    if line[start]=='?':
        if start + min_required_space > len(line):
            return tot
        # if line[start+cur_grp_len] == '#':
        #     return tot
        sub_line=line[start:start+cur_grp_len]
        if "." in sub_line:
            return tot        
        
        if start + cur_grp_len == len(line):
            tot = all_combs_of_line( line , start + cur_grp_len , grps, gidx + 1 , tot, cumul + ('#' * cur_grp_len) )
        else:
            tot = all_combs_of_line( line , start + cur_grp_len + 1, grps, gidx + 1 , tot, cumul + ('#' * cur_grp_len) + '.')
        return all_combs_of_line( line , start + 1, grps, gidx , tot, cumul + '.')
    elif line[start]=='#':
        sub_line=line[start:start+cur_grp_len]
        if "." in sub_line:
            return tot
        if start + cur_grp_len < len(line) and line[start+cur_grp_len] == '#':
            return tot
        
        return all_combs_of_line( line , start + cur_grp_len + 1, grps, gidx + 1 , tot ,cumul + ('#' * cur_grp_len) + '.')
    elif line[start]=='.':

        return all_combs_of_line( line , start + 1 , grps ,gidx  , tot , cumul + '.')
    else: 
        raise "oooops"

def get_count_for_line( num , ln ):
    return all_combs_of_line( ".".join(ln[0]) , 0, ln[1] ,0,0)

#print(get_count_for_line( plines[0]))
#cnts = [ get_count_for_line( num, ln ) for num, ln in enumerate(plines) ]
cnts= [ get_count_for_line( num, ln ) for num, ln in enumerate(plines) ]
print(cnts)
print(sum(cnts))

# all_combs_of_word2(["??#"],0,0,'','',[2],0,[])