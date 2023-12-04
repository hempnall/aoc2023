#! /usr/bin/env python
f = open("input.txt","r")
lines = [ l.strip() for l in f.readlines() ]
num_red=12
num_blue=14
num_green=13


def parse_games( game):
    sub_games = game.split(",")
    return {
        c[1]: int(c[0]) for c in 
            [ o.strip().split(" ") for o in sub_games]
    }

def parse_line( line ):
    game = line.split(":")
    game_id = int(  game[0][5::] )
    games = game[1].split(";")
    return {
        "game_id": game_id,
        "games": [ parse_games( game.strip() ) for game in games ]
    }

def is_subgame_possible( game):
    return (not "red" in game or game["red"] <= num_red) and \
        (not "blue" in game or game["blue"] <= num_blue) and \
            (not "green" in game or game["green"] <= num_green)

def colour_count( game, colour):
    count = [ k[colour] if colour in k else 0 for k in game]
    return max(count)

def game_power( game ):
    num_reds = colour_count( game , "red")
    num_blues = colour_count( game , "blue")
    num_greens = colour_count( game , "green")
    return num_reds * num_blues * num_greens

games = [ parse_line(ln) for ln in lines ]

possibilities = [ {
    "game_id": k["game_id"],
    "possibles": [ is_subgame_possible( game) for game in k["games"] ]
} for k in games ]

possible_games = [
    k["game_id"] for k in possibilities if all( k["possibles"])
]


print(sum(possible_games))

game_powers = [
    game_power(k["games"]) for k in games
]

print (game_powers)

sum_game_powers = sum( game_powers )
print(sum_game_powers)
