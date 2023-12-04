#! /usr/bin/env python
f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

numbers= dict()
symbols=set()
gears=set()

in_number=False
accum=0
start=None
end=None

for row in range(0,len(lines)):
    for idx in range(0,len(lines[row])):
        cur_char=lines[row][idx]
        if in_number:
            if cur_char.isdigit():
                accum = (10 * accum ) + int(cur_char)
                end=(idx-1,row)
            else:
                in_number=False
                end=(idx-1,row)
                numbers[(start,end)]=accum
        else:
            if cur_char.isdigit():
                accum=int(cur_char)
                in_number=True
                start=(idx,row)
            else:
                pass

        if not cur_char.isdigit() and not cur_char == '.':
            symbols.add((idx,row))

        if cur_char == '*':
            gears.add((idx,row))

        


    if in_number:
        numbers[(start,end)]=accum

print(symbols)
print(numbers)

def is_symbol_next_to_number( s , n ):
    return (n[0][0]-1) <= s[0] <= (n[1][0]+1) and (n[0][1]-1) <= s[1] <= (n[1][1]+1)

tot = 0
for n in numbers:
    for s in symbols:
        if is_symbol_next_to_number( s , n ):
            tot += numbers[n]
            break


gear_ratios_accum=0
for g in gears:
    nums=[]
    for n in numbers:
        if is_symbol_next_to_number(g,n):
            nums.append(numbers[n])
    if len(nums) == 2:
        gear_ratios_accum += (nums[0] * nums[1])

print(tot)
print(gear_ratios_accum)