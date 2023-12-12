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

def call_with_cache( words , word_idx, start, cumul,next_char,lens,len_idx,poss_lens):
    # all_combs_of_word2( words, word_idx, start,cumul,next_char,lens,len_idx,poss_lens)
    cache_key=(word_idx,cumul,next_char,len_idx)
    if cache_key in answer_cache:
        poss_lens += answer_cache[cache_key]
        #print(f'hit - {cache_key} {answer_cache[cache_key]} {poss_lens}')
    else:
        #print("miss")
        empty_arr=[]
        all_combs_of_word2( words, word_idx, start,cumul,next_char,lens,len_idx,empty_arr)
        answer_cache[cache_key]=empty_arr
        poss_lens += empty_arr


def all_combs_of_word2( words, word_idx , start , cumul , next_char, lens, len_idx, poss_lens ):
    word=words[word_idx]
    
    if len(cumul) > 0 and cumul[-1] == '#' and next_char =='.':
        arr = [ len(r) for r in cumul.split(".") if r !='' ]
        len_arr = len(arr)
        for idx in range(len_arr):
            lens_idx = idx + len_idx
            if lens_idx >= len(lens) or arr[idx] != lens[ lens_idx ]:
                return

        # if len_idx + len_arr < len(lens):
        #     remaining=lens[(len_idx + len_arr):]
        #     #print(remaining)
        #     remaining_hashes=sum(remaining) + len(remaining) - 1
        #     #print(f'{remaining_hashes + start + 1} {len(word)}')
        #     if remaining_hashes + start + 1 > len(word):
        #         print("cancel")
        #         return
        # elif '#' in word[(start+1):]:
        #     return


    cumul += next_char
    if start == len(word):
        arr = [ len(r) for r in cumul.split(".") if r !='' ]
        for idx in range(len(arr)):
            lens_idx = idx + len_idx
            if lens_idx >= len(lens) or arr[idx] != lens[ lens_idx ]:
                return
        poss_lens.append(arr)
        return

    if word[start] == '?':

        call_with_cache( words, word_idx, start + 1, cumul , '#', lens, len_idx, poss_lens)
        call_with_cache( words, word_idx, start + 1, cumul , '.', lens, len_idx, poss_lens)
        
    elif word[start] == '#':
        call_with_cache( words, word_idx, start + 1, cumul , '#', lens, len_idx, poss_lens )

def all_combs_of_line( words, word_idx, lens, len_idx, tot ):

    if word_idx == len(words):
        if len_idx != len(lens):
            return
        else:
            tot[0] += 1
            return 
    else:
        poss_lens = []
        word_cache={}

        all_combs_of_word2(words, word_idx,0,'', '', lens,len_idx, poss_lens)

        for poss in poss_lens:
            word_cache_key=len_idx + len(poss)
            if word_cache_key in word_cache:
                tot[0] += word_cache[word_cache_key]
            else:
                tmp_tot=[0]
            
                all_combs_of_line( words , word_idx + 1, lens, len_idx + len(poss), tmp_tot)
                word_cache[word_cache_key]= tmp_tot[0]
                tot[0] += word_cache[word_cache_key]

def get_count_for_line( num , ln ):
    print(f'{num} {ln}')
    global answer_cache, global_line_cache
    answer_cache={}
    total=[0]
    all_combs_of_line( ln[0] , 0, ln[1], 0, total )
    return total[0]


#print(get_count_for_line( plines[0]))
cnts = [ get_count_for_line( num, ln ) for num, ln in enumerate(plines) if not num in [] ]

print(sum(cnts))