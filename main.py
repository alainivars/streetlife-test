#!/usr/bin/env python3
#
# python 3 example of resolve the :
# https://gist.github.com/jorgebastida/f90adff6bf83736b2a23#file-readme-txt
#
# Author: Alain IVARS (alainivars@gmail.com) SkypeId: highfeature
# Copyright 2016 HIGHFEATURE All rights reserved
# Licence: M.I.T
#

"""
This is a point of view of an Architect ... and here you can see how clear specifications are vitals to avoid
misunderstand with the customer.
An other important point: set random start positions in specification broke the repeatability of the validation
Other points: "NEVER RE-INVENT THE WHELL" and "KEEP IT SIMPLE, STUPID"
Last point on PEP8: I like all the recommendations in this PEP except one, the limit of 79 characters by line
for me that an antediluvian thing when screen had only 80 characters by line, now in the 21st century, every editors
even vi can display up to 120 characters by line and I use that, that make the code more readable, specialy when
I see some lines cutted in 10 sub-lines with backslash at end, tha remind me some obscur codes in C or C++
whi I had to debug. You can agree or not, you have the right, this is my opinion, of course when I work for a client
I follow these coding rules and these can be very different from one to an other.
I thing the version 3.0.0 will be a Django version because I LOVE that Framework and made the movements and show the
result on google or GIS map will be very nice :)

Assumptions :
- we are in the 21st centuries and all cats are equipped with a tracking system
- other thing not specified: when we comapare if human and cat are in same station;
  before moves, after moves, after human move but before human move ???
  I have decided to check it at every moment and, believe me that change a lot the result.
"""
import random
import sys
import getopt
import json
import networkx as nx

from models import Human, Cat

MAX_MOVE_CAT = 10000
STATIONS_JSON_FILE = "tfl_stations.json"
CONNECTIONS_JSON_FILE = "tfl_connections.json"

# hummm, a question for design pattern purists: how many design pattern are used in this sample ?
# give me they names and how many time they are used each ? after the good answer I will tell you
# witch design pattern I use commonly at work and how


def usage():
    """command line help"""
    print("usage: ", sys.argv[0], "-h --help -c --count number")


def check_metting(human, cat, net):
    if human.current_station == cat.current_station:
        print("Owner {} found cat {} - {} is now closed.".format(
              human.id, cat.id, net.node[human.current_station]['name']))
        human.found_cat = True
        human.can_move = False
        cat.can_move = False
        net.node[human.current_station]['closed'] = True
        return 1
    return 0

if __name__ == "__main__":

    count = None
    humans = []
    cats = []
    net = None
    found = 0

    """get datas from command line: just the count is important for us"""
    try:
        _, args = getopt.getopt(sys.argv, "hc:", ["help","count="])
        if args[1] in ("-c", "--count"):
            count = int(args[2])
        else:
            usage()
            exit(1)
    except:  # don't like global, but it's first draw
        usage()
        exit(1)

    # build the net
    net = nx.Graph()

    # build the net with station from json file datas
    with open(STATIONS_JSON_FILE) as data_file:
        stations_datas = json.load(data_file)
        for station in stations_datas:
            net.add_node(int(station[0]), {'name': station[1], 'closed': False})

    # build the net of connections from file json
    with open(CONNECTIONS_JSON_FILE) as data_file:
        connections_datas = json.load(data_file)
        for connection in connections_datas:
            net.add_edge(int(connection[0]), int(connection[1]))

    # create Humans and cats
    for i in range(count):
        not_closed_stations = [s for s in net.nodes()]
        human_current_station = random.choice(not_closed_stations)
        humans.append(Human(id=i, current_station=human_current_station))
        not_closed_stations.remove(human_current_station)
        cats.append(Cat(id=i, current_station=(random.choice(not_closed_stations))))

    # let's go (single thread, second draft)
    sum_average = 0
    count_average = 0
    count_human_blocked = 0
    count_cat_blocked = 0
    for i in range(MAX_MOVE_CAT):
        for human in humans:
            if not human.found_cat and found != count:
                found += check_metting(human, cats[human.id], net)
                if human.can_move:
                    human.calculate_move(cats[human.id], net)
                    found += check_metting(human, cats[human.id], net)
                    # if human can't move that mind not path to cat,
                    # in that case don't need move cat
                    if cats[human.id].can_move:
                        cats[human.id].calculate_move(net)
                        found += check_metting(human, cats[human.id], net)
                else:
                    count_human_blocked += 1
                    humans.remove(human)
            else:
                sum_average += human.count_move
                count_average += 1
                humans.remove(human)

    print("Total number of cats: ", count)
    print("Number of cats found: ", found)
    for cat in cats:
        if not cat.can_move:
            count_cat_blocked += 1
    if count_average:
        print("Average number of movements required to find a cat: ",
              int(sum_average/count_average))
    print("Humans without path to cat: ", count_human_blocked)
    print("Cats blocked at a station: ", count_cat_blocked)

    exit(0)