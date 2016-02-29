# utilities.py
#
# python 3 example of resolve the :
# https://gist.github.com/jorgebastida/f90adff6bf83736b2a23#file-readme-txt
#
# Author: Alain IVARS (alainivars@gmail.com) SkypeId: highfeature
# Copyright 2016 HIGHFEATURE All rights reserved
# Licence: M.I.T
#

import random
import networkx as nx
from networkx.algorithms import shortest_path, all_shortest_paths


def calculate_move_cat(cat, net):
    matches = list((c for c in net.neighbors(cat.current_station) if not net.node[c]['closed']))
    if matches:
        cat.count_move += 1
        cat.current_station = random.choice(matches)
    else:
        # no path (ei. all destination station are closed)
        cat.can_move = False


def calculate_move_human(human, cat, net):
    try:
        matches = shortest_path(net, source=human.current_station, target=cat.current_station)
    except nx.NetworkXNoPath:
        # no path (ei. all destination station are closed)
        human.can_move = False
        return
    if len(matches) > 1:
        if net.node[matches[1]]['closed']:
            matches = list(all_shortest_paths(net, source=human.current_station, target=cat.current_station)
                           )
            paths = []
            for path_id, sub_list in enumerate(matches):
                for c in sub_list:
                    if net.node[c]['closed']:
                        paths.append(False)
                        break
                if len(paths) < path_id:
                    paths.append(True)
            if True in paths:
                human.count_move += 1
                human.current_station = matches[path_id][1]
            else:
                human.can_move = False
        else:
            human.count_move += 1
            human.current_station = matches[1]
