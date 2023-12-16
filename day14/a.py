#! /iusr/bin/env python
f = open("/Users/jameshook/dev/aoc2023/day14/sample.txt","r")
lines = [ l.strip() for l in f.readlines() ]

NORTH=(0,-1)
SOUTH=(0,1)
EAST=(-1,0)
WEST=(1,0)
ITERAIONS=1_000_000_000
LOOK_FOR_CYCLES=100

def rock_locs( rock_type ):
    rocks=[ ( col, len(lines) - row - 1) for row,ln in enumerate(lines) for col, r in enumerate(lines[row]) if r == rock_type  ]
    return set(rocks)

def load( round_rocks_locs ):
    return sum( [ loc[1]+1 for loc in round_rocks_locs ] )

def add_edges( square_rocks ):
    for idx in range(len(lines[0])):
        square_rocks.add((idx,len(lines)) )
        square_rocks.add((idx,-1))
    for idx in range(len(lines)):
        square_rocks.add((-1,idx))
        square_rocks.add((len(lines[0]),idx))
    return square_rocks



def print_rocks(squares,rounds):
    for row_idx in range(len(lines)-1,-1,-1):
        for col_idx in range(0,len(lines[0])):
            if (col_idx,row_idx) in squares:
                print('#', end='')
            elif (col_idx,row_idx) in rounds:
                print('O',end='')
            else:
                print('.',end='')
        print()
    print("-")


def roll_north( square_rocks, round_rocks):
    new_pos_round_rocks=set([])
    for sq in square_rocks:
        search_pos=1
        count_of_rolling_stone=0
        current_loc=(sq[0],sq[1]-search_pos)
        print("current sq is " + sq)
        while not current_loc in square_rocks and (sq[1] - search_pos) > 0:
            print(current_loc)
            if current_loc in round_rocks:
                print("is round rock")
                count_of_rolling_stone += 1
            search_pos += 1
            current_loc=(sq[0],sq[1]-search_pos)

        for rock_no in range(count_of_rolling_stone):

            new_pos_round_rocks.add((sq[0],sq[1] - (1 + rock_no)))
    return new_pos_round_rocks

def add_vec( vec1, addvec, fact=1):
    return ( vec1[0] + (addvec[0] * fact ), vec1[1] + (addvec[1] * fact) )

def in_bounds( vec ):
    return vec[0] <= len(lines[0])  and \
            vec[0] >= -1 and \
            vec[1] <= len(lines) and \
            vec[1] >= -1

def debug( msg ):
    pass #rint(msg)

def roll_in_dir( square_rocks, round_rocks , dir ):
    new_pos_round_rocks=set([])
    for sq in square_rocks:
        count_of_rolling_stone=0
        current_loc=add_vec(sq,dir)
        debug(f'current square = {sq}')
        while not current_loc in square_rocks and in_bounds(current_loc):
            debug(f'current_loc = {current_loc}')
            if current_loc in round_rocks:
                debug("is O")
                count_of_rolling_stone += 1
            current_loc=add_vec(current_loc,dir,1)
        debug("--")
        for rock_no in range(count_of_rolling_stone):
            debug(f'adding {add_vec(sq,dir,rock_no + 1)}')
            new_pos_round_rocks.add(add_vec(sq,dir,1 + rock_no))

    return new_pos_round_rocks, load(new_pos_round_rocks)


def rotate_once( square_rocks , round_rocks  ):
    round_rocks_n , l_n = roll_in_dir(square_rocks,round_rocks, NORTH)
    round_rocks_w , l_w = roll_in_dir(square_rocks,round_rocks_n, WEST)
    round_rocks_s , l_s  = roll_in_dir(square_rocks,round_rocks_w, SOUTH)
    round_socks_e  , l_e =  roll_in_dir( square_rocks , round_rocks_s,EAST)
    load_key = (l_n,l_w,l_s,l_e)
    return round_socks_e , load_key

square_rocks = rock_locs('#')
round_rocks = rock_locs('O')
square_rocks= add_edges(square_rocks)


CYCLES_MAP={}
for idx in range(0,30):
    round_rocks, key = rotate_once(square_rocks,round_rocks)
    print_rocks(square_rocks,round_rocks)
    if not key in CYCLES_MAP:
        CYCLES_MAP[key] = [ idx ]
    else:
        CYCLES_MAP[key].append(idx)

print(CYCLES_MAP)
print(load(round_rocks))