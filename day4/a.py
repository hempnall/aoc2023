#! /usr/bin/env python
f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def parse_nums( ln ):
    return set([
        wn.strip() for wn in ln.strip().split(" ") if wn != ""
    ])

def scratch_card_from_line( line ):
    comps = line.split(":")
    if len(comps) != 2:
        raise "invalid line"
    num_arr=comps[1].split("|")
    if len(num_arr) != 2:
        raise "invalid line"
    win_nums=parse_nums( num_arr[0] )
    my_nums=parse_nums( num_arr[1])
    return (win_nums,my_nums)

def scratch_card_score( sc ):
    intersection = sc[0].intersection(sc[1])
    if len(intersection) == 0:
        return 0
    else:
        return 2 ** (len(intersection)-1)

def scratch_card_overlap( sc ):
    intersection = sc[0].intersection(sc[1])
    return len(intersection)

scratchcards = [
    scratch_card_from_line( line ) for line in lines
]

scratch_card_scores = [
    scratch_card_score( sc ) for sc in scratchcards
]

print(scratchcards)
print(scratch_card_scores)
print(sum(scratch_card_scores))

scratch_card_counts = [
    1 for l in lines
]

for card_no, card in enumerate(scratchcards):
    score = scratch_card_overlap(card)
    for idx in range(0,score):
        scratch_card_counts[card_no + idx + 1] += scratch_card_counts[card_no]

print(sum(scratch_card_counts))

