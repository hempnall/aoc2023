#! /usr/bin/env python
sample={ "times" : [ 7 ,   15 ,    30 ] ,
         "distance": [ 9 , 40 , 200 ]}   

input = {
         "times" : [  48   ,  93   ,  85   ,  95] ,
         "distance": [ 296 ,  1928  , 1236 ,  1391]}  


def get_distance( accel, total):
    return accel * (total - accel)

def get_count_of_max( time , distance ):
    distances = [ get_distance(idx+1 , time ) for idx in range(0,time) ]
    return len( [ d for d in distances if d > distance  ] )

def calc_answer( input_data ):
    times_array=input_data["times"]
    distances_array=input_data["distance"]
    len_times_array=len(times_array)
    if len_times_array!= len(distances_array):
        raise "ooooooops"
    
    combos = [ get_count_of_max( times_array[idx] , distances_array[idx] ) for idx in range(0,len_times_array) ]
    prod=1
    for idx in range(0,len_times_array):
        prod *= combos[idx]

    return prod

print(calc_answer(input))
print(get_count_of_max(71530,940200))
print(get_count_of_max(48938595,296192812361391))