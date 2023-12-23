#! /usr/bin/env python3
import copy
import sys
f = open("/Users/jameshook/dev/aoc2023/day20/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]

def parse_line( l ):
    if l.startswith("broadcaster"):
        nodes=[ n.strip() for n in l[14:].split(",") ]
        return "broadcaster", {
            "type": "B",
            "nodes": nodes,
            "isOn": False
        }
    elif l.startswith("%") or l.startswith("&"):
        fs=l.index(" ")
        ndname=l[1:fs]
        nodes=[ n.strip() for n in l[(fs+4):].split(",") ]
        return ndname, {
            "type": l[0],
            "nodes": nodes,
            "isOn": False,
            "mostRecentInputs": {},
            "lastButtonPressTrue": {},
            "periods":{}
        }
    else:
        raise "whopps"
    
nodes={
    n[0]: n[1] for n in 
        [ parse_line(l) for l in lines ] 
}

conj = [ n for n in nodes if nodes[n]["type"] == "&" ]
ff = [ n for n in nodes if nodes[n]["type"] == "%" ]
for c in conj:
    for f in ff:
        if c in nodes[f]["nodes"]:
            nodes[c]["mostRecentInputs"][f]=False
            nodes[c]["lastButtonPressTrue"][f]=0



QUEUE=[]
LOW_PULSES=0
HIGH_PULSES=0
PERIODS=set([])
def process_pulse( sender, ndnm, isHigh ):
    global LOW_PULSES
    global HIGH_PULSES
    global COUNT_BUTTON_PRESSES
    if isHigh:
        HIGH_PULSES += 1
    else:
        LOW_PULSES += 1

    if ndnm == "cl":
        if sender in nodes[ndnm]["mostRecentInputs"] and nodes[ndnm]["mostRecentInputs"][sender]:
            lbp=nodes[ndnm]["lastButtonPressTrue"]
            if sender in lbp:
                res = COUNT_BUTTON_PRESSES - nodes[ndnm]["lastButtonPressTrue"][sender] 
                nodes[ndnm]["lastButtonPressTrue"][sender]=COUNT_BUTTON_PRESSES
                nodes[ndnm]["periods"][sender].append(res)
            else:    
                nodes[ndnm]["lastButtonPressTrue"][sender]=COUNT_BUTTON_PRESSES
                nodes[ndnm]["periods"][sender]=[]

    nd = None
    if ndnm in nodes:
        nd= nodes[ndnm]
    else:
        return
     
    if nd["type"] == "B":
        for newnd in nd["nodes"]:
            QUEUE.append((ndnm, newnd, False))
    elif nd["type"] == "%":
        if isHigh:
            pass
        else:
            nd["isOn"] = not nd["isOn"]
            pulse = nd["isOn"]
            for newnd in nd["nodes"]:
                QUEUE.append((ndnm, newnd, pulse))
                #process_pulse(ndnm,newnd,pulse)
    elif nd["type"] == "&":
        nd["mostRecentInputs"][sender]=isHigh
        pulse = not all(nd["mostRecentInputs"].values())
        for newnd in nd["nodes"]:
            QUEUE.append((ndnm, newnd, pulse))
    else:
        print("errpr")
        pass             

COUNT_BUTTON_PRESSES=0
for x in range(10000):
    QUEUE.append(("button","broadcaster",False))
    COUNT_BUTTON_PRESSES = x + 1
    while QUEUE:
        nd=QUEUE.pop(0)
        #print(f'{nd[0]} -{"HIGH" if nd[2] else "LOW"}-> {nd[1]}')
        process_pulse(nd[0],nd[1],nd[2])


print(PERIODS)
print(nodes["cl"])
# print(LOW_PULSES)
# print(HIGH_PULSES)
# print(LOW_PULSES * HIGH_PULSES)


