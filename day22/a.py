#! /usr/bin/env python3
import sys
import math

sys.setrecursionlimit(1500000)
f = open("/Users/jameshook/dev/aoc2023/day22/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

DEBUG=False

def debug( msg ):
    if DEBUG:
        print(f'[DEBUG] {msg}')

class ZBuffer:

    def __init__(self):
        self.buffer={}

    def aerial_view(self):
        x_vals=[ x[0] for x in self.buffer ]
        y_vals=[ x[1] for x in self.buffer ]
        print("top")
        for x in range( min(x_vals) ,max(x_vals) + 1 ):
            for y in range( min(y_vals) ,max(y_vals) + 1 ):
                if (x,y) in self.buffer:
                    print(f'{self.buffer[(x,y)][0]}',end='')
                else:
                    print('.',end='')
            print()
        print("height")
        for x in range( min(x_vals) ,max(x_vals) + 1 ):
            for y in range( min(y_vals) ,max(y_vals) + 1 ):
                    print(f'{self.get_height((x,y))}',end='')
            print()
        
    def get_height( self , coord ):
        if not coord in self.buffer:
            return 0
        else:
            return self.buffer[coord][1]

    def get_object_at( self , coord ):
        if not coord in self.buffer:
            return None
        else:
            return self.buffer[coord][0]

    def drop_brick( self , brick , bricks):
        debug(f'DROP BRICK {brick.index}')
        max_height=0
        brick_dict={}

        for x in brick.XRange:
            for y in brick.YRange:
                coord=(x,y)
                h=self.get_height(coord)
                o=self.get_object_at(coord)
                if not h in brick_dict:
                    brick_dict[h]=set([o])
                else:
                    brick_dict[h].add(o)
                max_height=max(h,max_height)

        bricks[brick.index].supportedBy = brick_dict[max_height]
        debug(f'brick={brick.index} supportedBy={brick_dict[max_height]}')
        for brk_idx in brick_dict[max_height]:
            if not brk_idx is None:
                debug(f' - adding {brick.index} to {brk_idx} [{bricks[brk_idx].supporting}]')
                bricks[brk_idx].supporting.add(brick.index)
                debug(f' - added {brick.index} to {brk_idx} [{bricks[brk_idx].supporting}]')
        brick.settled_height=max_height
        for x in brick.XRange:
            for y in brick.YRange:
                self.buffer[(x,y)]=(brick.index,max_height + brick.height() )


class Brick:
    def __init__( self , ln , idx ):
        ends=ln.split("~")
        e1=[ int(v) for v in ends[0].split(",") ]
        e2=[ int(v) for v in ends[1].split(",") ]

        self.index=idx
        self.supporting=set([])
        self.supportedBy=set([])

        self.XRange = self.range(e1,e2,0)
        self.YRange = self.range(e1,e2,1)
        self.ZRange = self.range(e1,e2,2)

    def __lt__(self,other):
        return list(self.ZRange)[0] < list(other.ZRange)[0]

    def range(self, e1 , e2 , d ):
        return range( min(e1[d],e2[d]) , max(e1[d],e2[d]) + 1)

    def height(self):
        return len(list(self.ZRange))
    
    def can_be_removed(self,bricks):
        for brk_id in self.supporting:
            if len(bricks[brk_id].supportedBy) in [0,1]:
                return False
        return True
    
    def count_of_dependent_bricks(self, bricks, removed):
        for sup_brk in self.supporting:
            new_supported_by=[ brk for brk in bricks[sup_brk].supportedBy if brk not in removed  ]
            if len(new_supported_by) == 0:
                removed.add(sup_brk)

        for brk in self.supporting:
            removed = bricks[brk].count_of_dependent_bricks(bricks, removed)
        return removed


def get_bricks( lines ):
    return [ Brick( b,idx ) for idx, b in enumerate(lines) ]

def get_bricks_apart_from( lines , l):
    return [ Brick( b,idx ) if idx != l else Brick("-1,-1,-1~-1,-1,-1",idx) for idx, b in enumerate(lines)  ]

def index_hgt_dict( brks ):
    return { brk.index: brk.settled_height for brk in brks }
    

bricks=sorted(get_bricks(lines))
ZB=ZBuffer()    
for br in bricks:
    ZB.drop_brick(br,bricks)
can_be_removed=[  b for b in bricks if  b.can_be_removed(bricks) ]
print(len(can_be_removed))
master=index_hgt_dict(bricks)
print(master)
print()
tot=0
for idx in range(len(lines)):
    brks = get_bricks_apart_from( lines , idx )
    srted_bricks=sorted(brks)
    ZB=ZBuffer()
    for brin in srted_bricks:
        ZB.drop_brick(brin,srted_bricks)
    h_dict=index_hgt_dict( srted_bricks )

    diffs=len( [  b.index for b in srted_bricks if h_dict[b.index] != master[b.index]   and b.index != idx ])
    tot+=diffs
    
print(tot)









