#! /usr/bin/env python3
import networkx as nx

f = open("/Users/jameshook/dev/aoc2023/day25/input.txt","r")
lines = [ l.strip() for l in f.readlines() ]
cnodes=["dvr","bbp","qvq","jzv","gtj","tzj"]

def parse_node( ln ):
    parts = ln.split(":")
    src=parts[0].strip()
    joined_nodes=[ n.strip() for n in parts[1].split(" ") if n != "" ]
    return (src, joined_nodes)

def add_node_to_graph( dict , nd1 , nd2 ):
    if not nd1 in dict:
        dict[nd1]=set([nd2])
    else:
        dict[nd1].add(nd2)

def make_graph( nodes ):
    graph_dict = {}
    for nd in nodes:
        for jn in nd[1]:
            add_node_to_graph( graph_dict , nd[0] , jn)
            add_node_to_graph( graph_dict , jn , nd[0])
    return graph_dict

nodes = [ parse_node( ln ) for ln in lines ]

gd= make_graph( nodes)

for n in cnodes:
    print(n, gd[n])

G = nx.Graph()

for n in nodes:
    for j in n[1]:
        if n[0] in cnodes and j in cnodes:
            print("not adding", n[0],j)
        else:
            G.add_edge(n[0],j)

print(G.number_of_nodes())
if nx.is_connected(G):
    print("CONNECTED")
else:
    print("not connected")

print(nx.number_connected_components(G))
set1_1=nx.node_connected_component(G,"bbp")
set1_2=nx.node_connected_component(G,"dvr")
set2_1=nx.node_connected_component(G,"tzj")
set2_2=nx.node_connected_component(G,"gtj")
set3_1=nx.node_connected_component(G,"jzv")
set3_2=nx.node_connected_component(G,"qvq")

print( len(set1_1) , len(set1_2))
print( len(set2_1) , len(set2_2))
print( len(set3_1) , len(set3_2))

print( len(set1_1) * len(set1_2))


# bc = nx.betweenness_centrality(G,1400)
# s=sorted(bc.items(), key=lambda x:x[1])
# # s=[ n[1] for n in bc.items() ]
# print(s)
# # print("}")


