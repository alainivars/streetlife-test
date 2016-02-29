#!/usr/bin/env python3
#
# python 3 example of resolve the :
# https://gist.github.com/jorgebastida/f90adff6bf83736b2a23#file-readme-txt
#
# Author: Alain IVARS (alainivars@gmail.com) SkypeId: highfeature
# Copyright 2016 HIGHFEATURE All rights reserved
# Licence: M.I.T
#
# PS: to reduce the execution time without big result changes, modify the
# MAX_MOVE_CAT = 100000 to MAX_MOVE_CAT = 10000
# Normally I write the tests first, but for first draw draft I don't write tests
#
# this is a point of view of an Architect... and here you can see how clear specifications
# are vital to avoid misunderstand with the customer.
# No assumptions, the true live :
# - The Owner don't in real-time where is the cat
# - Human and cat move in random order, that mean:
#   - the cat can move beforre or after the human (3 times to check the meeting)

import random
import sys
import getopt
import json

MAX_MOVE_CAT = 10000
STATIONS_JSON_FILE = "tfl_stations.json"
CONNECTIONS_JSON_FILE = "tfl_connections.json"
# don't like global VM, but it's first draw
# can be put in singleton for design pattern purist...
# hummm, a question for design pattern purists: how many design pattern are used in this sample ?
# give me they names and how many time they are used each ? after the good answer I will tell you
# witch design pattern I use commonly at work and how
stations = []
connections = []


class Entity:
    """docstring for Entity

    Attributes:
        id: An integer representing the identifier of the entity.
        current_station: An integer representing the identifier of the current station.
    """
    def __init__(self, id, current_station):
        self.id = id
        self.current_station = current_station
        self.count_move = 0
        self.can_move = True


class Cat(Entity):
    """docstring for Cat

    Attributes:
        id: An integer representing the identifier of the entity.
        current_station: An integer representing the identifier of the current station.
    """
    def __init__(self, id, current_station):
        super(Cat, self).__init__(id, current_station)

    """docstring for calculate_move"""
    def calculate_move(self):
        self.count_move += 1
        matches = (c for c in connections if c[0] == self.current_station and not stations[c[1]].closed)
        if matches:
            self.current_station = random.choice(matches)[1]
        else:
            # no path (ei. all destination station are closed)
            self.can_move = False


class Human(Entity):
    """docstring for Human

    Attributes:
        id: An integer representing the identifier of the entity.
        current_station: An integer representing the identifier of the current station.
    """
    def __init__(self, id, current_station):
        super(Human, self).__init__(id, current_station)
        self.last_station = current_station
        self.found_cat = False

    """docstring for calculate_move"""
    def calculate_move(self):
        self.count_move += 1
        matches = [c for c in connections if c[0] == self.current_station and
                   c[1] != self.last_station and not stations[c[1]].closed]
        if not len(matches):
            matches = [c for c in connections if c[0] == self.current_station and
                       not stations[c[1]].closed]
        if matches:
            self.current_station = random.choice(matches)[1]
        else:
            # no path (ei. all destination station are closed)
            self.can_move = False


class Station:
    """docstring for Station

    Attributes:
        id: An integer representing the identifier of the entity.
        name: An string of the current station.
    """
    def __init__(self, id, name):
        super(Station, self).__init__()
        self.id = id
        self.name = name
        self.closed = False


def usage():
    """command line help"""
    print("usage: ", sys.argv[0], "-h --help -c --count number")
    

if __name__ == "__main__":

    count = None
    humans = []
    cats = []
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

    # build an empty stations list of 1000 to direct access
    for x in range(1000):
        stations.append(Station(id=x, name=None))
    # fill the list with station from json dile datas
    with open(STATIONS_JSON_FILE) as data_file:
        stations_datas = json.load(data_file)
        for station in stations_datas:
            stations[int(station[0])].id = int(station[0])
            stations[int(station[0])].name = station[1]

    # build the list of connections from file json
    with open(CONNECTIONS_JSON_FILE) as data_file:
        connections_datas = json.load(data_file)
        for connection in connections_datas:
            connections.append([int(connection[0]), int(connection[1])])
        # now build reverse conbination to simplfy move algorithm
        for connection in connections_datas:
            connections.append([int(connection[1]), int(connection[0])])
        # not sure it's usefull but it's first draw and it better for debug
        connections.sort()

    # create Humans and cats
    for i in range(count):
        stations_existantes = [s for s in stations if s.name]
        humans.append(Human(id=i, current_station=(random.choice(stations_existantes)).id))
        cats.append(Human(id=i, current_station=(random.choice(stations_existantes)).id))

    # let's go (single thread, first draft)
    for i in range(MAX_MOVE_CAT):
        for human in humans:
            if not human.found_cat and found != count:
                if human.current_station == cats[human.id].current_station:
                    print("Owner {} found cat {} - {} is now closed.".format(
                          human.id, cats[human.id].id, stations[human.current_station].name))
                    human.found_cat = True
                    found += 1
                    stations[human.current_station].closed = True
                if human.can_move:
                    human.calculate_move()
                if cats[human.id].can_move:
                    cats[human.id].calculate_move()

    print("Total number of cats: ", count)
    print("Number of cats found: ", found)
    sum_average = 0
    count_average = 0
    count_human_blocked = 0
    count_cat_blocked = 0
    for human in humans:
        if human.found_cat:
            sum_average += human.count_move
            count_average += 1
        if not human.can_move:
            count_human_blocked += 1
        if not cats[human.id].can_move:
            count_cat_blocked += 1
    print("Average number of movements required to find a cat: ", int(sum_average/count_average))
    print("Humans blocked at a station: ", count_human_blocked)
    print("Cats blocked at a station: ", count_cat_blocked)

    exit(0)