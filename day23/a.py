#! /usr/bin/env python3
import sys

sys.setrecursionlimit(1500000)
f = open("/Users/jameshook/dev/aoc2023/day23/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]
DIRS=[(1,0),(-1,0),(0,1),(0,-1)]
SLOPE_SYMBOLS=["<",">","v","^"]
SLOPE_DIRS={
    "<": (-1,0),
    "^": (0,-1),
    ">": (1,0),
    "v": (0,1)
}
DEBUG=True

def debug(msg=''):
    if DEBUG:
        print(msg)

def add_vec( v1 , v2 ):
    return ( v1[0] + v2[0] , v1[1] + v2[1])

def mult_vec( v1 , K ):
    return ( v1[0] * K , v1[1] * K )

def parse_map( lines ):
    PATHS=set([])
    FOREST=set([])
    SLOPES={ }
    START=None
    END=None
    for ridx, ln in enumerate(lines):
        for cidx , c in enumerate(ln):
            coord=(cidx,ridx)
            if c == "#":
                FOREST.add(coord)
            elif c == ".":
                PATHS.add(coord)
                if ridx == 0:
                    START=coord
                if ridx == (len(lines) - 1):
                    END=coord
            elif c in SLOPE_SYMBOLS:
                pass
                #SLOPES[coord]=c

        
    return PATHS,FOREST,SLOPES,START,END

def in_bounds( loc ):
    return 0 <= loc[0] < len(lines[0]) and 0 <= loc[1] < len(lines)

def display_forest( PATH ,spec_loc):
    for ridx in range( len(lines)):
        for cidx in range( len(lines[0])):
            coord=(cidx,ridx)
            if coord == spec_loc:
                print("X",end='')
            elif coord in FORESTS:
                print("#",end='')
            elif coord in SLOPES:
                print( SLOPES[coord], end='' )
            elif coord in PATH:
                print("O",end='')
            else:
                print(".",end='')

        print()


PATHS,FORESTS,SLOPES,START,END = parse_map(lines)



CURRENT_PATH_ARR=[ ]
DIST_TO_END=[]
MX_DST=0
FIND_EDGE_DICT={}

def find_edge(E_START,init_dir):
    if not (E_START,init_dir) in FIND_EDGE_DICT:
        RES=find_edge_raw(E_START,init_dir)
        FIND_EDGE_DICT[(E_START,init_dir)]=RES
        return RES
    else:
        return FIND_EDGE_DICT[(E_START,init_dir)]

def find_edge_raw(E_START,init_dir):

    STATE=(E_START,init_dir,0)
    STACK=[STATE]   
    STEPS=set([])

    while STACK:
        cur_state=STACK.pop(0)

        cur_loc=cur_state[0]
        cur_dir=cur_state[1]
        cur_steps=cur_state[2]

        if cur_loc != E_START:
            STEPS.add(cur_loc)

        if cur_loc in SLOPES:
            debug(f'next dir is slope {SLOPES[cur_loc]} -> {SLOPE_DIRS[ SLOPES[cur_loc] ]} ')
            next_dir =  SLOPE_DIRS[ SLOPES[cur_loc] ]
            new_loc = add_vec( cur_loc , next_dir)
            STACK.append(( new_loc , next_dir, cur_steps + 1) )
            continue

        OPTIONS=[]
        BACKTRACK_AT_END=None

        if cur_loc == END:
            return (END,STEPS,[])

        else:
            for D in DIRS:
                if cur_steps == 0 and not D == cur_dir:
                    if not cur_dir == (0,0):
                        continue

                next_pos = add_vec( cur_loc , D )

                if D == mult_vec( cur_dir , -1 ):
                    BACKTRACK_AT_END=(next_pos, D , cur_steps + 1)
                    continue

                if next_pos in FORESTS:
                    continue

                if not in_bounds( next_pos ):
                    continue

                OPTIONS.append(( next_pos , D , cur_steps + 1 ) )

        if len(OPTIONS )==1:
            STACK.insert(0,OPTIONS[0])

        elif len(OPTIONS)>1:
            #print(f'from {E_START} found junction {cur_loc} after {cur_steps} steps')
            next_options=[ *OPTIONS , BACKTRACK_AT_END ]

            if START == E_START:
                # for opt in OPTIONS:
                #     print(opt)
                return (cur_loc,STEPS,OPTIONS)
            else:
                # for opt in next_options:
                #     print(opt)
                return (cur_loc,STEPS,next_options )
        
        else:
            return None

GRAPH_NODES={}
SEEN=set([])

def add_edge_to_graph( S, E, dist):
    #print(f'add {S} -> {E} = {dist}')
    if not S in GRAPH_NODES:
        GRAPH_NODES[S]={E:dist}
    else:
        if E in GRAPH_NODES[S]:
            if dist > GRAPH_NODES[S][E]:
                GRAPH_NODES[S][E]=dist
        else:
            GRAPH_NODES[S][E]=dist



def disp_edges( dict ):
    for k in dict:
        for v in dict[k]:
            print(f'{k} -> {v} is {dict[k][v]}')
        print()



def make_graph(S , INIT_DIR):
    #print(f'make_graph {S} {INIT_DIR}')
    if (S,INIT_DIR) in SEEN:
        #print("seen")
        return
    SEEN.add((S,INIT_DIR))
    next_node=find_edge(S,INIT_DIR)
    if next_node is None:
        return
    else:
        add_edge_to_graph(S,next_node[0],len(next_node[1]))
        add_edge_to_graph(next_node[0],S,len(next_node[1]))
        for opt in next_node[2]:
            #print(f' from {S}  recursing {next_node[0]} {opt[1]}')
            make_graph(next_node[0],opt[1])

def analyse_graph(LSTART,SEEN,LEND,tot):
    global MX_DST
    if LSTART == LEND:
        if tot > MX_DST:
            MX_DST = tot
        return
    NEXT_NODES=GRAPH_NODES[LSTART]
    for next_node in NEXT_NODES:
        if next_node in SEEN:
            continue
        else:
            SEEN.append(next_node)
            analyse_graph(next_node, SEEN,LEND, tot + NEXT_NODES[next_node])
            SEEN.pop()

# tests= [
#     # ( START , (0,0)),
#     # ( (1,1) , (1,0)),
#     # ( (5,3) , (0,-1)),
#     # ( (1,1) , (0,1)),
#     ( (5,3) , (0,1))
#  ] 

# results = [
#     # ((1,1),1,[((2, 1), (1, 0), 2), ((1, 2), (0, 1), 2)]),
#     # ((5,3),6,[((4, 3), (-1, 0), 7), ((5, 4), (0, 1), 7), ((5, 2), (0, -1), 7)]),
#     # ((1,1),8,[((2, 1), (1, 0), 9), ((1, 0), (0, -1), 9), ((1, 2), (0, 1), 9)]),
#     # ((5,3),6,[((4, 3), (-1, 0), 7), ((5, 4), (0, 1), 7), ((5, 2), (0, -1), 7)]),
#     (END,3, 0)

# ]

# for idx, t in enumerate(tests):
#     res=find_edge(*t)
#     if res[0] == results[idx][0] and len(res[1]) == results[idx][1] and res[2]== results[idx][2]:
#         print("PASS")
#     else:
#         print(res)
#         print("FAIL")

make_graph(START,(0,0))
seen=[ ]
disp_edges(GRAPH_NODES)
max_dist=analyse_graph(START,seen,END,0)

print(MX_DST)



