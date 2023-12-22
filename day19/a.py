#! /usr/bin/env python3
import copy
f = open("/Users/jameshook/dev/aoc2023/day19/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

ACCEPTED=[]

def parse_instruction( inst ):
    inst_comp = inst.split(":")
    if len(inst_comp) == 1:
        return ("=","",0,inst_comp[0])
    elif len(inst_comp) == 2:
        if ">" in inst_comp[0]:
            exp = inst_comp[0].split(">")
            return (">",exp[0],int(exp[1]),inst_comp[1])
        elif "<" in inst_comp[0]:
            exp = inst_comp[0].split("<")
            return ("<",exp[0],int(exp[1]),inst_comp[1])
        else:
            raise "woops"
 
def parse_workflow( ln ) :
    name_idx=ln.index("{")
    name=ln[0:name_idx]
    csv=ln[name_idx+1:-1]
    
    return name, [ parse_instruction( i ) for i in  csv.split(",") ]

def parse_item( ln):
    strip_braces=ln[1:-1]
    assgn=strip_braces.split(",")
    r={}
    for a in assgn:
        bits=a.split("=")
        r[bits[0]]=int(bits[1])
    return r

def parse_input( ls ):
    if not "" in ls:
        raise "woops"
    idx = ls.index("")
    return [ parse_workflow( ln ) for ln in ls[0:idx] ], [ parse_item( ln) for ln in ls[idx+1:] ]

def process_inst( item, exp ):
    if exp[0] == "<":
        if item[exp[1]] < exp[2]:
            return True
        else:
            return False
    elif exp[0] == ">":
        if item[exp[1]] > exp[2]:
            return True   
        else:
            return False
    elif exp[0] == "=":
        return True
    print(f'ERROR {exp[1]}={item[exp[1]]} {exp[0]} {exp[2]}')
    return False      

def process_item( nm, it , acc, workflows ):
    wf = workflows[nm]
    for exp in wf:
        if process_inst( it, exp):
            next_wf=exp[3]
            if next_wf == "A":
                acc.append( it )
                return "A"
            elif next_wf == "R":
                return "R"
            else:
                return process_item( next_wf, it , acc, workflows )
    return "E"

def sum_accepted( acc ):
    scores = [ a["x"] + a["m"] + a["s"] + a["a"] for a in acc]
    return sum(scores)

def size_of_let_range( let , range ):
    return max(0, 1 + range[let][1] - range[let][0])

def size_of_range( ranges ):
    
    return size_of_let_range( "x", ranges) \
        * size_of_let_range( "m", ranges) \
        * size_of_let_range( "a", ranges) \
        * size_of_let_range( "s", ranges) 

def bump_range_for_true( ranges, inst ):
    new_range=dict(ranges)
    if inst[0] == "<":
        new_range[inst[1]][1]=min(inst[2]-1,ranges[inst[1]][1])
    elif inst[0] == ">":
        new_range[inst[1]][0]=max(inst[2]+1,ranges[inst[1]][0])
    else:
        raise "whoops"
    return new_range

def bump_range_for_false( ranges, inst ):
    new_range=dict(ranges)
    if inst[0] == "<":
        new_range[inst[1]][0]=max(inst[2],ranges[inst[1]][0])
    elif inst[0] == ">":
        new_range[inst[1]][1]=min(inst[2],ranges[inst[1]][1])
    else:
        raise "whoops"
    return new_range

def build_tree( nd,  combo_count , ranges ):
    if nd == "A":
        return combo_count + size_of_range( ranges )
    elif nd == "R":
        return combo_count
    
    wfs = workflows[nd]
    for inst in wfs:
        op = inst[0]
        
        if op == "=":
            return build_tree( inst[3], combo_count, ranges)
        elif op in ["<",">"]:
            # print(f'INSTRUCTION={inst[1]}{inst[0]}{inst[2]}')
            # print(f'FALSE: {bump_range_for_false(copy.deepcopy(ranges),inst)}')
            # print(f'TRUE: {bump_range_for_true(copy.deepcopy(ranges),inst)}')
            # print("===")
            combo_count += build_tree( inst[3], 0, bump_range_for_true(copy.deepcopy(ranges),inst))
            ranges = bump_range_for_false(  copy.deepcopy(ranges), inst )
        else:
            raise "whoops"
        
wfs, items = parse_input(lines)
workflows={ wf[0]: wf[1] for wf in wfs }

for item in items:
    res=process_item( "in" , item, ACCEPTED,workflows)

print(sum_accepted(ACCEPTED))

max_range={"x": [1,4000], "m": [1,4000], "a": [1,4000], "s": [1,4000]}

print(size_of_let_range("x",max_range))

com = build_tree("in",0,max_range)
print(com)