#! /usr/bin/env python
from functools import cmp_to_key

f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def hand_type( hand ):
    hand_hist={}
    for c in hand:
        if not c in hand_hist:
            hand_hist[c]=1
        else:
            hand_hist[c] += 1

    s_hand_hist=sorted(hand_hist.items(), key=lambda x:x[1],reverse=True)
    if "J" in hand_hist:
        cnt=hand_hist["J"]
        if cnt == 5:
            pass
        else:
            print("========")
            print(hand)
            print(s_hand_hist)
            hand_hist["J"] -= cnt
            highest=s_hand_hist[0][0]
            if highest=="J":
                hand_hist[s_hand_hist[1][0]] += cnt
            else:
                hand_hist[s_hand_hist[0][0]] += cnt
            s_hand_hist=sorted(hand_hist.items(), key=lambda x:x[1],reverse=True)
            print(s_hand_hist)

    if s_hand_hist[0][1] ==5:
        return 7
    elif s_hand_hist[0][1] ==4:
        return 6
    elif s_hand_hist[0][1] ==3:
        if s_hand_hist[1][1]==2:
            return 5
        else:
            return 4
    elif s_hand_hist[0][1] ==2:
        if s_hand_hist[1][1]==2:
            return 3
        else:
            return 2
    else:
        return 1
        
def cards_to_number_arr( hand ):
    return hand.replace("A","E").replace("J","1") \
                .replace("K","D") \
                .replace("Q","C") \
                .replace("T","A") \

def compare_hands( hand1 , hand2 ):
    diff = hand1[2] - hand2[2]
    if diff != 0:
        return diff
    else:
        if hand1[3] > hand2[3]:
            return 1
        else:
            return -1

def get_hand(line):
    ln=line.split(' ')
    return [
        ln[0],
        int(ln[1]),
        hand_type(ln[0]),
        cards_to_number_arr(ln[0])
    ]

hands = [ get_hand(ln) for ln in lines ]

sorted_hands = sorted( hands, key=cmp_to_key(compare_hands))

scores = [ (rank + 1) * prize[1] for rank,prize in enumerate(sorted_hands)]

print(sum(scores))

