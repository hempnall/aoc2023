#! /usr/bin/env python
import sys
import copy
sys.setrecursionlimit(15000)
f = open("/Users/jameshook/dev/aoc2023/day12/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]


def parse_line1( line ):
    parts=line.split(" ")
    nums=[ int(n) for n in parts[1].split(",") ]
    grps=[ grp for grp in parts[0].split(".") if grp != '' ]
    if len(parts) == 2:
        return (grps,nums)
    else:
        return (grps,nums,int(parts[2]))

def parse_line2( line ):
    parts=line.split(" ")
    nums=[ int(n) for n in parts[1].split(",") ]
    new_line="?".join([parts[0] for i in range(5)])
    new_nums=[*nums,*nums,*nums,*nums,*nums]
    grps=[ grp for grp in new_line.split(".") if grp != '' ]
    return (grps,new_nums)

plines=[ parse_line2(ln) for ln in lines]

answer_cache={}
use_cache=True
def debug( msg ):
    pass #print(msg)

def all_combs_of_line( line , start , grps , gidx, tot, cumul = '', debug_s=''):
    if not use_cache:
        return all_combs_of_line_uncached(line,start,grps,gidx,tot,cumul,debug_s)
    cache_key=(start,gidx)
    debug(answer_cache)
    if cache_key in answer_cache:
        new_tot = answer_cache[cache_key]
        if new_tot > 0:
            debug(f'  CACHE {cumul} {new_tot} {cache_key}')
        return tot + answer_cache[cache_key]
    new_tot=all_combs_of_line_uncached(line,start,grps,gidx,0,cumul,debug_s)
    debug(new_tot)
    if new_tot > 0:
        debug(f'NOCACHE {cumul} {new_tot} {cache_key}')
    answer_cache[cache_key]=new_tot 
    return new_tot + tot

def all_combs_of_line_uncached( line , start , grps, gidx, tot, cumul = '' ,debug_s=''):

    if gidx == len(grps):
        if start < len(line):
            if '#' in line[start:]:
                return tot
        if start > len(line):
            return tot
        debug("++++R   " + line)
        debug("+++++   " + cumul)
        debug("++++D   " + debug_s)
        debug("")
        return tot + 1
        
    elif start >= len(line):

        if gidx < (len(grps)):
            return tot

    cur_grp_len=grps[gidx]
    min_required_space=sum(grps[gidx:]) + (len(grps[gidx:]) - 1)
    sub_line=line[start:start+cur_grp_len]
    
    dotInGroup = "." in sub_line
    grpFitsInLine = start + cur_grp_len < len(line)
    hashAfterGroup=grpFitsInLine and line[start+cur_grp_len] == '#'
    loc_of_dot=sub_line.index(".") if dotInGroup else -1
    hashInGroup = "#" in sub_line[0:loc_of_dot]
    grpIsEndOfLine = start + cur_grp_len == len(line)
    grpOverShootsLine= start + cur_grp_len > len(line)
    #debug(f'{line} {start}')
    if line[start]=='?':
        
        if grpOverShootsLine:
            return tot
        if dotInGroup:
            if hashInGroup :
                return tot
            resumeAt=start + loc_of_dot + 1
            return all_combs_of_line( line , resumeAt , grps, gidx  , tot, cumul + '.' * (loc_of_dot  ) + '|',debug_s + '1' * (loc_of_dot + 1) )        
        if hashAfterGroup:
            resumeAt = start + 1
            return all_combs_of_line( line , resumeAt , grps, gidx  , tot, cumul + '.' , debug_s + '2' )
        if grpIsEndOfLine:
            return all_combs_of_line( line , start + cur_grp_len , grps, gidx + 1 , tot, cumul + ('#' * cur_grp_len) , debug_s + '3' * cur_grp_len)
        else:
            # do both
            tot = all_combs_of_line( line , start + cur_grp_len + 1, grps, gidx + 1 , tot, cumul + ('#' * cur_grp_len) + '.', debug_s + '4' * (cur_grp_len + 1))
            return all_combs_of_line( line , start + 1, grps, gidx , tot, cumul + '.', debug_s + '5')
    
    elif line[start]=='#':
        if "." in sub_line:
            return tot

        if start + cur_grp_len == len(line):
            # start next group now
            tot = all_combs_of_line( line , start + cur_grp_len , grps, gidx + 1 , tot, cumul + ('#' * cur_grp_len) ,debug_s + '6' * cur_grp_len)

        elif hashAfterGroup:
            return tot #all_combs_of_line( line , start +  1 , grps, gidx  , tot, cumul + '.'  )
        
        return all_combs_of_line( line , start + cur_grp_len + 1, grps, gidx + 1 , tot ,cumul + ('#' * cur_grp_len) + '.' , debug_s + '7' * (cur_grp_len + 1))
    
    elif line[start]=='.':
        return all_combs_of_line( line , start + 1 , grps ,gidx  , tot , cumul + '|', debug_s + '8')
    
    else: 
        raise "oooops"

def get_count_for_line( num , ln):
    debug("======")
    debug(f'{num} {ln}')
    global answer_cache
    answer_cache={}
    if len(ln) == 2:
        res = all_combs_of_line( ".".join(ln[0]) , 0, ln[1] ,0,0)

        return res
    else:
        res = all_combs_of_line( ".".join(ln[0]) , 0, ln[1] ,0,0)
        if res != ln[2]:
            print(f'FAIL {num} {ln} expected={ln[2]} result={res}')
        else:
            print(f'PASS {num} {ln} result={res}')
        return res


cnts= [ get_count_for_line( num, ln ) for num, ln in enumerate(plines) ]

print(sum(cnts))