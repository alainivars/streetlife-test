# pytest tests
#
# python 3 example of resolve the :
# https://gist.github.com/jorgebastida/f90adff6bf83736b2a23#file-readme-txt
#
# Author: Alain IVARS (alainivars@gmail.com) SkypeId: highfeature
# Copyright 2016 HIGHFEATURE All rights reserved
# Licence: M.I.T
#
# to run test:
# pip3 install pytest
# py.test tests.py

import networkx as nx

# assume:
# - don't test existing libraries
# - don't test models, they are to simple
from models import Cat, Human
from utilities import calculate_move_cat, calculate_move_human


class TestClass:
    """
    Test basic move for a cat
    The network represent a single branch graph.
    0-----1-----2-----3-----4
    """
    def create_the_network(self):
        # create the network
        net = nx.Graph()
        for station in range(0,5):
            net.add_node(station, {'name': str(station), 'closed': False})
        link = zip(range(0,4),range(1,5))
        net.add_edges_from(link)
        return net

    """
    Test basic move for a cat
    The network represent a single branch graph.
    0-----1-----2-----3-----4
    """
    def test_calculate_move_cat(self):
        # create the network
        net = self.create_the_network()
        # put cat in the network
        cat = Cat(id=1, current_station=0)
        assert cat.current_station == 0
        calculate_move_cat(cat, net)
        assert cat.current_station == 1

    """
    Test basic move for an human with a valid path
    The network represent a single branch graph.
    0-----1-----2-----3-----4
    """
    def test_calculate_move_human_valid_path(self):
        # create the network
        net = self.create_the_network()
        # put cat in the network
        cat = Cat(id=1, current_station=4)
        assert cat.current_station == 4
        # put cat in the network
        human = Human(id=1, current_station=0)
        # test with a valid path
        assert human.current_station == 0
        calculate_move_human(human, cat, net)
        assert human.current_station == 1

    """
    Test basic move for an human broken path
    The network represent a single branch graph.
    0-----1-----2-----3-----4
    """
    def test_calculate_move_human_broken_path(self):
        # create the network
        net = self.create_the_network()
        # put cat in the network
        cat = Cat(id=1, current_station=4)
        assert cat.current_station == 4
        # put cat in the network
        human = Human(id=1, current_station=1)
        # test with a broken path at next station
        net.node[2]['closed'] = True
        calculate_move_human(human, cat, net)
        assert human.current_station == 1
        assert not human.can_move

    """
    Test basic move for an human with broken path at next station
    The network represent a single branch graph.
    0-----1-----2-----3-----4
    """
    def test_calculate_move_human_broken_path_next_station(self):
        # create the network
        net = self.create_the_network()
        # put cat in the network
        cat = Cat(id=1, current_station=4)
        assert cat.current_station == 4
        # put cat in the network
        human = Human(id=1, current_station=1)
        # test with a broken path at next station
        net.node[2]['closed'] = True
        calculate_move_human(human, cat, net)
        assert human.current_station == 1
        assert not human.can_move

    """
    Test basic move for an human with broken path at other station
    The network represent a single branch graph.
    0-----1-----2-----3-----4
    """
    def test_calculate_move_human_broken_path_other_station(self):
        # create the network
        net = self.create_the_network()
        # put cat in the network
        cat = Cat(id=1, current_station=4)
        assert cat.current_station == 4
        # put cat in the network
        human = Human(id=1, current_station=1)
        # test with a broken path at next station
        net.node[3]['closed'] = True
        # first move possible
        calculate_move_human(human, cat, net)
        assert human.current_station == 2
        # second move don't exit
        calculate_move_human(human, cat, net)
        assert human.current_station == 2
        assert not human.can_move
