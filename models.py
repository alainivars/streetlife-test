# models.py
#
# python 3 example of resolve the :
# https://gist.github.com/jorgebastida/f90adff6bf83736b2a23#file-readme-txt
#
# Author: Alain IVARS (alainivars@gmail.com) SkypeId: highfeature
# Copyright 2016 HIGHFEATURE All rights reserved
# Licence: M.I.T
#

from utilities import calculate_move_cat, calculate_move_human


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
    def calculate_move(self, net):
        calculate_move_cat(self, net)


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
    def calculate_move(self, cat, net):
        calculate_move_human(self, cat, net)
