f = open("/Users/jameshook/dev/aoc2023/day9/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]


def is_all_zeros( seq ):
    return not any(seq)

def get_next_sequence( line ):
    print(line)
    if is_all_zeros(line):
        return 0
    new_arr = [ line[idx+1] - line[idx] for idx in range(0,len(line)-1) ]
    next_num = get_next_sequence( new_arr )
    return line[0] -  next_num 

next_vals = [
    get_next_sequence( [ int(num) for num  in ln.split(" ")  ] ) for ln in lines
]

print(sum(next_vals))
