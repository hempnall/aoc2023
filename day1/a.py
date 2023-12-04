#! /usr/bin/env python
f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

num_map = {
    "one":'1',
    "two":'2',
    "three":'3',
    "four":'4',
    "five":'5',
    "six":'6',
    "seven":'7',
    "eight":'8',
    "nine":'9'
}

def text_to_number( txt ):
    for k in num_map:
        txt = txt.replace(k,k+num_map[k]+k)
    return txt

just_numbers = [
  [ c for c in text_to_number( l ) if c.isdigit() ] for l in lines 
]
print(lines)
print(just_numbers)

sums = [
    int( a[0] + a[-1] ) for a in just_numbers
]

print(sum(sums))