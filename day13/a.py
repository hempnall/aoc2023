#! /iusr/bin/env python
import copy
f = open("/Users/jameshook/dev/aoc2023/day13/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def parse_boxes(): 
    boxes=[]
    cur_box=[]
    for idx , line in enumerate(lines):
        if line == '':
            boxes.append(cur_box)
            cur_box=[]
        else:
            cur_box.append(line)
    return boxes

def rotate_box( box):
    cols=[]
    for idx in range(len(box[0])):
        col=''
        for row in box:
            col += row[idx]
        cols.append(col)
    return cols

both_ways=[ ( box , rotate_box(box) ) for box in parse_boxes() ]

def find_symmetry( box ,fact):
    # check for horizontal symmetry
    len_of_box=len(box)
    for idx in range( len_of_box -1 ):
        if box[idx] == box[idx+1]:
            top=box[0:idx+1][::-1]#.reverse()
            bottom=box[idx+1:]
            min_len=min(len(top),len(bottom))
            if top[0:min_len] == bottom[0:min_len]:
                return fact * (idx + 1)
    return 0
            
def check_for_symmetry( box , row ):
    reflect_size=min( row + 1 , len(box) - row -1)
    for idx in range(reflect_size):
        if box[row - idx] != box[row + 1 + idx]:
            return False
    return True

def xor_set( a,b):
    return [ idx for idx in range(len(a)) if a[idx] != b[idx]  ]

def xor_score( a , b ):
    return len(xor_set(a,b))

def xor_set_for_box( box ):
    ret=set([])
    for idx_a in range(len(box)):
        for idx_b in range(idx_a+1, len(box)):
            if xor_score(box[idx_a],box[idx_b]) == 1:
                if abs( idx_b - idx_a) % 2 > 0:
                    ret.add((idx_a,idx_b))
    return ret

def score_for_box( box ):
    return find_symmetry( box[0], 100) + find_symmetry(box[1],1)

def flipped_box( box , swap_lines ):
    new_box = [ r for r in box]
    xor_s=xor_set(new_box[swap_lines[0]],new_box[swap_lines[1]])
    print(xor_s)
    containing_line=new_box[swap_lines[0]]
    if containing_line[xor_s[0]] == '#':
        new_char = '.'
    else:
        new_char = '#'
    new_box[swap_lines[0]] = containing_line[:xor_s[0]]+new_char+containing_line[xor_s[0]+1:]
    return new_box

scores = [ score_for_box(box) for box in both_ways ]

print(scores)
print(sum(scores))

def box_score( box , fact ):
    xor_set_a=xor_set_for_box(box)
    print(xor_set_a)
    if len(xor_set_a)>0:
        for s in xor_set_a:
            print(s)
            new_box = flipped_box( box, s)
            row= s[0] + int( (s[1] - s[0] - 1 )/2)
            is_sym=check_for_symmetry(new_box, row )
            if is_sym:
                return (row + 1) * fact
    return 0
            
def partb_score( box1 , box2 ):
    return box_score(box1,100) + box_score(box2,1)

partb_scores = [ partb_score(b[0],b[1]) for b in both_ways ]

print(partb_scores)
print(sum(partb_scores))