import itertools
from calc_BR_state_machine import calc_BR_state_machine_player_i_ver
from build_joint_state_machine import construct_joint_state_machine
from check_SPE_state_machine import check_SPE_state_machine, check_SPE_state_machine_by_graph

"""
This file contains examples of strategy state machine for the paper "Subgame-perfect Cooperation in Networks".
"""


def V_graph_PD_a_ver():
    """
    Graph 1.2b with the prisoner's dilemma of 1.1b in the paper, with the strategies from section 4.
    A three players "V" graph: left - middle - right, with SPE strategies.
    """
    c = 2
    d = 4
    l = 1
    EPSILON = 0.01

    # The possible actions for every player
    left_actions = {"C", "D"}
    middle_actions = {"C", "D"}
    right_actions = {"C", "D"}
    actions_set = [left_actions, middle_actions, right_actions]
    all_actions = ["CCC", "CCD", "CDC", "CDD", "DCC", "DCD", "DDC", "DDD"]

    # the transition function for every player
    left_state_transition = {
        0: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 0, "DCD": 0, "DDC": 1, "DDD": 1},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {"CCC": 6, "CCD": 6, "CDC": 4, "CDD": 4, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
    }
    right_state_transition = {
        0: {"CCC": 0, "CCD": 6, "CDC": 1, "CDD": 4, "DCC": 0, "DCD": 6, "DDC": 1, "DDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 0, "DCD": 0, "DDC": 1, "DDD": 1},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {"CCC": 6, "CCD": 6, "CDC": 4, "CDD": 4, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
    }
    middle_state_transition = {
        0: {"CCC": 0, "CCD": 14, "CDC": 6, "CDD": 11, "DCC": 10, "DCD": 9, "DDC": 3, "DDD": 1},
        1: {i: 2 for i in all_actions},
        2: {i: 0 for i in all_actions},
        3: {i: 4 for i in all_actions},
        4: {i: 5 for i in all_actions},
        5: {"CCC": 0, "CCD": 0, "CDC": 6, "CDD": 6, "DCC": 10, "DCD": 10, "DDC": 3, "DDD": 3},
        6: {i: 7 for i in all_actions},
        7: {i: 8 for i in all_actions},
        8: {"CCC": 0, "CCD": 0, "CDC": 6, "CDD": 6, "DCC": 0, "DCD": 0, "DDC": 6, "DDD": 6},
        9: {"CCC": 9, "CCD": 9, "CDC": 1, "CDD": 1, "DCC": 9, "DCD": 9, "DDC": 1, "DDD": 1},
        10: {"CCC": 10, "CCD": 9, "CDC": 3, "CDD": 1, "DCC": 10, "DCD": 9, "DDC": 3, "DDD": 1},
        11: {i: 12 for i in all_actions},
        12: {i: 13 for i in all_actions},
        13: {"CCC": 0, "CCD": 14, "CDC": 6, "CDD": 11, "DCC": 0, "DCD": 14, "DDC": 6, "DDD": 11},
        14: {"CCC": 14, "CCD": 14, "CDC": 11, "CDD": 11, "DCC": 9, "DCD": 9, "DDC": 1, "DDD": 1},
    }
    transitions = [left_state_transition, middle_state_transition, right_state_transition]

    # the strategy function for every player
    left_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
    }
    right_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
    }
    middle_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "C",
        6: "D",
        7: "D",
        8: "C",
        9: "D",
        10: "D",
        11: "D",
        12: "D",
        13: "C",
        14: "D",
    }
    strategies = [left_state_strategy, middle_state_strategy, right_state_strategy]

    # the utility for the one-shot game
    left_utility = {"CCC": c, "CCD": c, "CDC": -l, "CDD": -l, "DCC": d, "DCD": d, "DDC": 0, "DDD": 0}
    right_utility = {"CCC": c, "CCD": d, "CDC": -l, "CDD": 0, "DCC": c, "DCD": d, "DDC": -l, "DDD": 0}
    middle_utility = {"CCC": 2 * c, "CCD": c - l, "CDC": 2 * d, "CDD": d, "DCC": c - l, "DCD": -2 * l, "DDC": d,
                      "DDD": 0}
    utilities_by_actions = [left_utility, middle_utility, right_utility]

    # constructing the joint strategy state machine
    joint_Q, joint_f, joint_s = construct_joint_state_machine(actions_set, transitions, strategies)

    # check if the strategies are SPE
    check_SPE_state_machine(joint_Q, joint_f, joint_s, utilities_by_actions, EPSILON=EPSILON)

    # check SPE using graph representation
    games = {
        (0, 1): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (1, 2): {"CC": c, "CD": -l, "DC": d, "DD": 0},
    }

    check_SPE_state_machine_by_graph(3, games, transitions, strategies)

    # calculate the best-response of the middle player, and show the returned strategy with the other players'
    # strategies are SPE
    joint = calc_BR_state_machine_player_i_ver(1, [left_state_transition, right_state_transition],
                                               [left_state_strategy, right_state_strategy], utilities_by_actions)

    check_SPE_state_machine(*joint, utilities_by_actions, EPSILON=EPSILON)


def V_graph_PD_b_ver():
    """
    Graph 1.2b with the prisoner's dilemma of 1.1a in the paper, with the strategies from section 4.
    A three players "V" graph: left - middle - right, with SPE strategies.
    The number of steps for the middle player to "gain the edge players trust back" is 2.
    """
    c = 2
    d = 4
    l = 3
    EPSILON = 0.01

    # The possible actions for every player
    left_actions = {"C", "D"}
    middle_actions = {"C", "D"}
    right_actions = {"C", "D"}
    actions_set = [left_actions, middle_actions, right_actions]
    all_actions = ["CCC", "CCD", "CDC", "CDD", "DCC", "DCD", "DDC", "DDD"]

    # the transition function for every player
    left_state_transition = {
        0: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {"CCC": 7, "CCD": 7, "CDC": 1, "CDD": 1, "DCC": 7, "DCD": 7, "DDC": 1, "DDD": 1},
        7: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 0, "DCD": 0, "DDC": 1, "DDD": 1},  # addition from before
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {"CCC": 6, "CCD": 6, "CDC": 4, "CDD": 4, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
    }
    right_state_transition = {
        0: {"CCC": 0, "CCD": 6, "CDC": 1, "CDD": 4, "DCC": 0, "DCD": 6, "DDC": 1, "DDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {"CCC": 7, "CCD": 7, "CDC": 1, "CDD": 1, "DCC": 7, "DCD": 7, "DDC": 1, "DDD": 1},
        7: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 0, "DCD": 0, "DDC": 1, "DDD": 1},  # addition from before
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {"CCC": 6, "CCD": 6, "CDC": 4, "CDD": 4, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
    }
    # states 15 to 19 are additional states from the strategy in the previous function
    middle_state_transition = {
        0: {"CCC": 0, "CCD": 14, "CDC": 6, "CDD": 11, "DCC": 10, "DCD": 9, "DDC": 3, "DDD": 1},
        1: {i: 2 for i in all_actions},
        2: {i: 0 for i in all_actions},
        3: {i: 4 for i in all_actions},
        4: {i: 5 for i in all_actions},
        5: {"CCC": 15, "CCD": 15, "CDC": 6, "CDD": 6, "DCC": 17, "DCD": 17, "DDC": 3, "DDD": 3},
        15: {"CCC": 0, "CCD": 0, "CDC": 6, "CDD": 6, "DCC": 10, "DCD": 10, "DDC": 3, "DDD": 3},
        17: {"CCC": 10, "CCD": 10, "CDC": 3, "CDD": 3, "DCC": 10, "DCD": 10, "DDC": 3, "DDD": 3},
        6: {i: 7 for i in all_actions},
        7: {i: 8 for i in all_actions},
        8: {"CCC": 16, "CCD": 16, "CDC": 6, "CDD": 6, "DCC": 16, "DCD": 16, "DDC": 6, "DDD": 6},
        16: {"CCC": 0, "CCD": 0, "CDC": 6, "CDD": 6, "DCC": 0, "DCD": 0, "DDC": 6, "DDD": 6},
        9: {"CCC": 9, "CCD": 9, "CDC": 1, "CDD": 1, "DCC": 9, "DCD": 9, "DDC": 1, "DDD": 1},
        10: {"CCC": 10, "CCD": 9, "CDC": 3, "CDD": 1, "DCC": 10, "DCD": 9, "DDC": 3, "DDD": 1},
        11: {i: 12 for i in all_actions},
        12: {i: 13 for i in all_actions},
        13: {"CCC": 18, "CCD": 19, "CDC": 6, "CDD": 11, "DCC": 18, "DCD": 19, "DDC": 6, "DDD": 11},
        18: {"CCC": 0, "CCD": 14, "CDC": 6, "CDD": 11, "DCC": 0, "DCD": 14, "DDC": 6, "DDD": 11},
        19: {"CCC": 14, "CCD": 14, "CDC": 11, "CDD": 11, "DCC": 14, "DCD": 14, "DDC": 11, "DDD": 11},
        14: {"CCC": 14, "CCD": 14, "CDC": 11, "CDD": 11, "DCC": 9, "DCD": 9, "DDC": 1, "DDD": 1},

    }
    transitions = [left_state_transition, middle_state_transition, right_state_transition]

    # the strategy function for every player
    left_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
        7: "D",
    }
    right_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
        7: "D",
        8: "D",
        9: "D",
    }
    middle_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "C",
        6: "D",
        7: "D",
        8: "C",
        9: "D",
        10: "D",
        11: "D",
        12: "D",
        13: "C",
        14: "D",
        15: "C",
        16: "C",
        17: "D",
        18: "C",
        19: "D",
    }
    strategies = [left_state_strategy, middle_state_strategy, right_state_strategy]

    # check SPE using graph representation
    games = {
        (0, 1): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (1, 2): {"CC": c, "CD": -l, "DC": d, "DD": 0},
    }

    check_SPE_state_machine_by_graph(3, games, transitions, strategies)


def Four_players_line_PD_ver():
    """
    An example of SPE strategies in a line of length 4. Players 0 and 1 play grim-trigger with each
    other, and also players 2 and 3.
    """
    c = 3
    d = 5
    l = 1

    # The possible actions for every player
    a_actions = {"C", "D"}
    b_actions = {"C", "D"}
    c_actions = {"C", "D"}
    d_actions = {"C", "D"}
    actions_set = [a_actions, b_actions, c_actions, d_actions]
    all_actions = ["".join(element) for element in itertools.product(*actions_set)]

    # the transition function for every player
    a_tra = {
        0: {ac: 0 if ac[:2] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    b_tra = {
        0: {ac: 0 if ac[:2] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    c_tra = {
        0: {ac: 0 if ac[2:] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    d_tra = {
        0: {ac: 0 if ac[2:] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    transitions = [a_tra, b_tra, c_tra, d_tra]

    # the strategy function for every player
    a_ac = {
        0: "C",
        1: "D",
    }
    b_ac = {
        0: "C",
        1: "D",
    }
    c_ac = {
        0: "C",
        1: "D",
    }
    d_ac = {
        0: "C",
        1: "D",
    }
    strategies = [a_ac, b_ac, c_ac, d_ac]

    # check SPE using graph representation
    games = {
        (0, 1): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (1, 2): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (2, 3): {"CC": c, "CD": -l, "DC": d, "DD": 0},
    }

    check_SPE_state_machine_by_graph(4, games, transitions, strategies)


def Four_players_cycle_PD_ver():
    """
    An example of SPE strategies in an even length cycle of length 4. Players 0 and 1 play grim-trigger with each
    other, and also players 2 and 3.
    """
    c = 3
    d = 5
    l = 1

    # The possible actions for every player
    a_actions = {"C", "D"}
    b_actions = {"C", "D"}
    c_actions = {"C", "D"}
    d_actions = {"C", "D"}
    actions_set = [a_actions, b_actions, c_actions, d_actions]
    all_actions = ["".join(element) for element in itertools.product(*actions_set)]

    # the transition function for every player
    a_tra = {
        0: {ac: 0 if ac[:2] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    b_tra = {
        0: {ac: 0 if ac[:2] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    c_tra = {
        0: {ac: 0 if ac[2:] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    d_tra = {
        0: {ac: 0 if ac[2:] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    transitions = [a_tra, b_tra, c_tra, d_tra]

    # the strategy function for every player
    a_ac = {
        0: "C",
        1: "D",
    }
    b_ac = {
        0: "C",
        1: "D",
    }
    c_ac = {
        0: "C",
        1: "D",
    }
    d_ac = {
        0: "C",
        1: "D",
    }
    strategies = [a_ac, b_ac, c_ac, d_ac]

    # check SPE using graph representation
    games = {
        (0, 1): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (1, 2): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (2, 3): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (3, 0): {"CC": c, "CD": -l, "DC": d, "DD": 0},
    }

    check_SPE_state_machine_by_graph(4, games, transitions, strategies)


def Five_players_cycle_PD_ver():
    """
    An example of SPE strategies in an odd length cycle of length 5. Players 3 and 4 play grim-trigger with each
    other, while players 0,1 and 2 play the SPE strategies for a V graph, the same as in "V_graph_PD_a" function.
    """
    c = 3
    d = 4.5
    l = 1
    left_actions = {"C", "D"}
    middle_actions = {"C", "D"}
    right_actions = {"C", "D"}
    clique_left_actions = {"C", "D"}
    clique_right_actions = {"C", "D"}
    actions_set = [left_actions, middle_actions, right_actions, clique_left_actions, clique_right_actions]
    actions_set_small = [left_actions, middle_actions, right_actions]
    all_actions = ["".join(element) for element in itertools.product(*actions_set)]
    all_actions_small = ["".join(element) for element in itertools.product(*actions_set_small)]

    # the transition function for every player
    clique_left_tra = {
        0: {ac: 0 if ac[3:] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    clique_right_tra = {
        0: {ac: 0 if ac[3:] == "CC" else 1 for ac in all_actions},
        1: {i: 1 for i in all_actions},
    }
    left_state_transition_help = {
        0: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
        1: {i: 2 for i in all_actions_small},
        2: {i: 3 for i in all_actions_small},
        3: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 0, "DCD": 0, "DDC": 1, "DDD": 1},
        4: {i: 5 for i in all_actions_small},
        5: {i: 0 for i in all_actions_small},
        6: {"CCC": 6, "CCD": 6, "CDC": 4, "CDD": 4, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
    }
    right_state_transition_help = {
        0: {"CCC": 0, "CCD": 6, "CDC": 1, "CDD": 4, "DCC": 0, "DCD": 6, "DDC": 1, "DDD": 4},
        1: {i: 2 for i in all_actions_small},
        2: {i: 3 for i in all_actions_small},
        3: {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 0, "DCD": 0, "DDC": 1, "DDD": 1},
        4: {i: 5 for i in all_actions_small},
        5: {i: 0 for i in all_actions_small},
        6: {"CCC": 6, "CCD": 6, "CDC": 4, "CDD": 4, "DCC": 6, "DCD": 6, "DDC": 4, "DDD": 4},
    }
    middle_state_transition_help = {
        0: {"CCC": 0, "CCD": 14, "CDC": 6, "CDD": 11, "DCC": 10, "DCD": 9, "DDC": 3, "DDD": 1},
        1: {i: 2 for i in all_actions_small},
        2: {i: 0 for i in all_actions_small},
        3: {i: 4 for i in all_actions_small},
        4: {i: 5 for i in all_actions_small},
        5: {"CCC": 0, "CCD": 0, "CDC": 6, "CDD": 6, "DCC": 10, "DCD": 10, "DDC": 3, "DDD": 3},
        6: {i: 7 for i in all_actions_small},
        7: {i: 8 for i in all_actions_small},
        8: {"CCC": 0, "CCD": 0, "CDC": 6, "CDD": 6, "DCC": 0, "DCD": 0, "DDC": 6, "DDD": 6},
        9: {"CCC": 9, "CCD": 9, "CDC": 1, "CDD": 1, "DCC": 9, "DCD": 9, "DDC": 1, "DDD": 1},
        10: {"CCC": 10, "CCD": 9, "CDC": 3, "CDD": 1, "DCC": 10, "DCD": 9, "DDC": 3, "DDD": 1},
        11: {i: 12 for i in all_actions_small},
        12: {i: 13 for i in all_actions_small},
        13: {"CCC": 0, "CCD": 14, "CDC": 6, "CDD": 11, "DCC": 0, "DCD": 14, "DDC": 6, "DDD": 11},
        14: {"CCC": 14, "CCD": 14, "CDC": 11, "CDD": 11, "DCC": 9, "DCD": 9, "DDC": 1, "DDD": 1},
    }
    left_state_transition = {}
    right_state_transition = {}
    middle_state_transition = {}

    for q in left_state_transition_help.keys():
        left_state_transition[q] = {}
        for ac in all_actions:
            left_state_transition[q][ac] = left_state_transition_help[q][ac[:3]]
    for q in right_state_transition_help.keys():
        right_state_transition[q] = {}
        for ac in all_actions:
            right_state_transition[q][ac] = right_state_transition_help[q][ac[:3]]
    for q in middle_state_transition_help.keys():
        middle_state_transition[q] = {}
        for ac in all_actions:
            middle_state_transition[q][ac] = middle_state_transition_help[q][ac[:3]]

    transitions = [left_state_transition, middle_state_transition, right_state_transition, clique_left_tra,
                   clique_right_tra]

    # the strategy function for every player
    clique_left_ac = {
        0: "C",
        1: "D",
    }
    clique_right_ac = {
        0: "C",
        1: "D",
    }
    left_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
    }
    right_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
    }
    middle_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "C",
        6: "D",
        7: "D",
        8: "C",
        9: "D",
        10: "D",
        11: "D",
        12: "D",
        13: "C",
        14: "D",
    }
    strategies = [left_state_strategy, middle_state_strategy, right_state_strategy, clique_left_ac, clique_right_ac]

    # check SPE using graph representation
    games = {
        (0, 1): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (1, 2): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (2, 3): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (3, 4): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (4, 0): {"CC": c, "CD": -l, "DC": d, "DD": 0},
    }

    check_SPE_state_machine_by_graph(5, games, transitions, strategies)


def Star_three_leafs_PD():
    """
    An example of SPE strategies in a star with a center and three leafs. Each of the leafs plays the same strategy as
    the edge players in the SPE strategies on the V graph (from the "V_graph_PD_a_ver" function). The strategy of the
    center is being calculated using Algorithm 4 from the paper, that find a best response given the other players
    state machines. Then, the function check that the new strategy, together with the leafs strategies, are indeed SPE.
    """
    c = 4
    d = 6
    l = 1
    EPSILON = 0.01

    # The possible actions for every player
    a_actions = {"C", "D"}
    b_actions = {"C", "D"}
    c_actions = {"C", "D"}
    d_actions = {"C", "D"}
    actions_set = [a_actions, b_actions, c_actions, d_actions]
    all_actions = ["".join(element) for element in itertools.product(*actions_set)]

    # The transitions functions of the leafs
    leaf_one_state_transition = {
        0: {"CCCC": 0, "CCCD": 0, "CCDC": 0, "CCDD": 0,
            "CDCC": 6, "CDCD": 6, "CDDC": 6, "CDDD": 6,
            "DCCC": 1, "DCCD": 1, "DCDC": 1, "DCDD": 1,
            "DDCC": 4, "DDCD": 4, "DDDC": 4, "DDDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {ac: 0 if ac[0] == "C" else 1 for ac in all_actions},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {ac: 6 if ac[0] == "C" else 4 for ac in all_actions},
    }
    leaf_two_state_transition = {
        0: {"CCCC": 0, "CCCD": 0, "CCDC": 6, "CCDD": 6,
            "CDCC": 0, "CDCD": 0, "CDDC": 6, "CDDD": 6,
            "DCCC": 1, "DCCD": 1, "DCDC": 4, "DCDD": 4,
            "DDCC": 1, "DDCD": 1, "DDDC": 4, "DDDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {ac: 0 if ac[0] == "C" else 1 for ac in all_actions},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {ac: 6 if ac[0] == "C" else 4 for ac in all_actions},
    }
    leaf_three_state_transition = {
        0: {"CCCC": 0, "CCCD": 6, "CCDC": 0, "CCDD": 6,
            "CDCC": 0, "CDCD": 6, "CDDC": 0, "CDDD": 6,
            "DCCC": 1, "DCCD": 4, "DCDC": 1, "DCDD": 4,
            "DDCC": 1, "DDCD": 4, "DDDC": 1, "DDDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {ac: 0 if ac[0] == "C" else 1 for ac in all_actions},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {ac: 6 if ac[0] == "C" else 4 for ac in all_actions},
    }
    transitions = [leaf_one_state_transition, leaf_two_state_transition, leaf_three_state_transition]

    # The strategy functions of the leafs
    leaf_one_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
    }
    leaf_two_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
    }
    leaf_three_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
    }
    strategies = [leaf_one_state_strategy, leaf_two_state_strategy, leaf_three_state_strategy]

    # The utilities of the players
    center_util = {
        "CCCC": 3 * c, "CCCD": 2 * c - l, "CCDC": 2 * c - l, "CCDD": c - 2 * l,
        "CDCC": 2 * c - l, "CDCD": c - 2 * l, "CDDC": c - 2 * l, "CDDD": - 3 * l,
        "DCCC": 3 * d, "DCCD": 2 * d, "DCDC": 2 * d, "DCDD": d,
        "DDCC": 2 * d, "DDCD": d, "DDDC": d, "DDDD": 0}
    leaf_one_util = {
        "CCCC": c, "CCCD": c, "CCDC": c, "CCDD": c,
        "CDCC": d, "CDCD": d, "CDDC": d, "CDDD": d,
        "DCCC": -l, "DCCD": -l, "DCDC": -l, "DCDD": -l,
        "DDCC": 0, "DDCD": 0, "DDDC": 0, "DDDD": 0
    }
    leaf_two_util = {
        "CCCC": c, "CCCD": c, "CCDC": d, "CCDD": d,
        "CDCC": c, "CDCD": c, "CDDC": d, "CDDD": d,
        "DCCC": -l, "DCCD": -l, "DCDC": 0, "DCDD": 0,
        "DDCC": -l, "DDCD": -l, "DDDC": 0, "DDDD": 0
    }
    leaf_three_util = {
        "CCCC": c, "CCCD": d, "CCDC": c, "CCDD": d,
        "CDCC": c, "CDCD": d, "CDDC": c, "CDDD": d,
        "DCCC": -l, "DCCD": 0, "DCDC": -l, "DCDD": 0,
        "DDCC": -l, "DDCD": 0, "DDDC": -l, "DDDD": 0
    }
    utilities = [center_util, leaf_one_util, leaf_two_util, leaf_three_util]

    # Calculating the center BR strategy and checking SPE
    joint = calc_BR_state_machine_player_i_ver(0, transitions, strategies, utilities)

    print("The number of states for the center of the star is:", len(joint[0]))
    print("The transition function for the center is:")
    print(joint[1])
    print("The strategy function for the center is:")
    print(joint[2])

    print("The output of algorithm 3 on the strategies of the leafs with the output of algorithm 4 for the center is:")
    check_SPE_state_machine(*joint, utilities, EPSILON=EPSILON)


def Triangle_with_leaf_PD_ver():
    """
    The same as in the "Star_three_leafs_PD" function, but when the first and second leaf are also connected between
    them. The number of step for the middle player to gain trust back is now 2 instead of 1.
    """
    c = 4
    d = 6
    l = 1
    EPSILON = 0.001

    # The possible actions for every player
    a_actions = {"C", "D"}
    b_actions = {"C", "D"}
    c_actions = {"C", "D"}
    d_actions = {"C", "D"}
    actions_set = [a_actions, b_actions, c_actions, d_actions]
    all_actions = ["".join(element) for element in itertools.product(*actions_set)]

    # The transitions functions of the leafs
    leaf_one_state_transition = {
        0: {"CCCC": 0, "CCCD": 0, "CCDC": 0, "CCDD": 0,
            "CDCC": 6, "CDCD": 6, "CDDC": 6, "CDDD": 6,
            "DCCC": 1, "DCCD": 1, "DCDC": 1, "DCDD": 1,
            "DDCC": 4, "DDCD": 4, "DDDC": 4, "DDDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {ac: 7 if ac[0] == "C" else 1 for ac in all_actions},
        7: {ac: 0 if ac[0] == "C" else 1 for ac in all_actions},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {ac: 6 if ac[0] == "C" else 4 for ac in all_actions},
    }
    leaf_two_state_transition = {
        0: {"CCCC": 0, "CCCD": 0, "CCDC": 6, "CCDD": 6,
            "CDCC": 0, "CDCD": 0, "CDDC": 6, "CDDD": 6,
            "DCCC": 1, "DCCD": 1, "DCDC": 4, "DCDD": 4,
            "DDCC": 1, "DDCD": 1, "DDDC": 4, "DDDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {ac: 7 if ac[0] == "C" else 1 for ac in all_actions},
        7: {ac: 0 if ac[0] == "C" else 1 for ac in all_actions},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {ac: 6 if ac[0] == "C" else 4 for ac in all_actions},
    }
    leaf_three_state_transition = {
        0: {"CCCC": 0, "CCCD": 6, "CCDC": 0, "CCDD": 6,
            "CDCC": 0, "CDCD": 6, "CDDC": 0, "CDDD": 6,
            "DCCC": 1, "DCCD": 4, "DCDC": 1, "DCDD": 4,
            "DDCC": 1, "DDCD": 4, "DDDC": 1, "DDDD": 4},
        1: {i: 2 for i in all_actions},
        2: {i: 3 for i in all_actions},
        3: {ac: 7 if ac[0] == "C" else 1 for ac in all_actions},
        7: {ac: 0 if ac[0] == "C" else 1 for ac in all_actions},
        4: {i: 5 for i in all_actions},
        5: {i: 0 for i in all_actions},
        6: {ac: 6 if ac[0] == "C" else 4 for ac in all_actions},
    }
    transitions = [leaf_one_state_transition, leaf_two_state_transition, leaf_three_state_transition]

    # The strategy functions of the leafs
    leaf_one_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
        7: "D",
    }
    leaf_two_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
        7: "D",
    }
    leaf_three_state_strategy = {
        0: "C",
        1: "D",
        2: "D",
        3: "D",
        4: "D",
        5: "D",
        6: "D",
        7: "D",
    }
    strategies = [leaf_one_state_strategy, leaf_two_state_strategy, leaf_three_state_strategy]

    # The utilities of the players
    center_util = {
        "CCCC": 3 * c, "CCCD": 2 * c - l, "CCDC": 2 * c - l, "CCDD": c - 2 * l,
        "CDCC": 2 * c - l, "CDCD": c - 2 * l, "CDDC": c - 2 * l, "CDDD": - 3 * l,
        "DCCC": 3 * d, "DCCD": 2 * d, "DCDC": 2 * d, "DCDD": d,
        "DDCC": 2 * d, "DDCD": d, "DDDC": d, "DDDD": 0}
    leaf_one_util = {
        "CCCC": 2 * c, "CCCD": 2 * c, "CCDC": c - l, "CCDD": c - l,
        "CDCC": 2 * d, "CDCD": 2 * d, "CDDC": d, "CDDD": d,
        "DCCC": c - l, "DCCD": c - l, "DCDC": -2 * l, "DCDD": -2 * l,
        "DDCC": d, "DDCD": d, "DDDC": 0, "DDDD": 0
    }
    leaf_two_util = {
        "CCCC": 2 * c, "CCCD": 2 * c, "CCDC": 2 * d, "CCDD": 2 * d,
        "CDCC": c - l, "CDCD": c - l, "CDDC": d, "CDDD": d,
        "DCCC": c - l, "DCCD": c - l, "DCDC": d, "DCDD": d,
        "DDCC": -2 * l, "DDCD": -2 * l, "DDDC": 0, "DDDD": 0
    }
    leaf_three_util = {
        "CCCC": c, "CCCD": d, "CCDC": c, "CCDD": d,
        "CDCC": c, "CDCD": d, "CDDC": c, "CDDD": d,
        "DCCC": -l, "DCCD": 0, "DCDC": -l, "DCDD": 0,
        "DDCC": -l, "DDCD": 0, "DDDC": -l, "DDDD": 0
    }
    utilities = [center_util, leaf_one_util, leaf_two_util, leaf_three_util]

    # Calculating the center BR strategy and checking SPE
    joint = calc_BR_state_machine_player_i_ver(0, transitions, strategies, utilities)

    print("The number of states for the center of the star is:", len(joint[0]))
    print("The transition function for the center is:")
    print(joint[1])
    print("The strategy function for the center is:")
    print(joint[2])
    print()
    print("The output of algorithm 3 on the strategies of the leafs with the output of algorithm 4 for the center is:")
    check_SPE_state_machine(*joint, utilities, EPSILON=EPSILON)


def Two_players_chicken_GT_ver():
    """
    In the chicken game (hawk-dove game), this function is an example of "grim-trigger" strategies, when both of the
    players cooperate, giving them utility of 0. In the case where one of the players deviated, the game "collapses" to
    the Nash equilibrium that gives the deviating player negative utility.
    """
    v = 5
    c = 6
    EPSILON = 0.01

    # The possible actions for every player
    left_actions = {"C", "D"}
    right_actions = {"C", "D"}
    actions_set = [left_actions, right_actions]
    all_actions = ["CC", "CD", "DC", "DD"]

    # transitions and strategies
    left_state_transition = {
        0: {"CC": 0, "CD": 1, "DC": 2, "DD": 0},
        1: {i: 1 for i in all_actions},
        2: {i: 2 for i in all_actions},
    }
    left_state_strategy = {
        0: "C",
        1: "D",
        2: "C",
    }

    right_state_transition = {
        0: {"CC": 0, "CD": 2, "DC": 1, "DD": 0},
        1: {i: 1 for i in all_actions},
        2: {i: 2 for i in all_actions},
    }
    right_state_strategy = {
        0: "C",
        1: "D",
        2: "C",
    }

    transitions = [left_state_transition, right_state_transition]
    strategies = [left_state_strategy, right_state_strategy]

    # checking SPE
    games = {
        (0, 1): {"CC": 0, "CD": -v, "DC": v, "DD": -c},
    }

    check_SPE_state_machine_by_graph(2, games, transitions, strategies)


def Triangle_chicken_ver():
    """
    In the chicken game (hawk-dove game), this function is an example of "grim-trigger" strategies for three players in
    a triangle, meaning a three player clique. The strategies are one of fukk cooperation, but in the case where one of
    the player deviated, the game "collapses" to a Nash equilibrium that gives the deviating player (or players)
    negative utility.
    This strategies are "like" grim-trigger, in the sense that after a deviation, there no way for the players to
    return to cooperation, or even change the action they play in each turn without gaining lower utility.
    """
    v = 5
    c = 11
    EPSILON = 0.01

    # The possible actions for every player
    left_actions = {"C", "D"}
    middle_actions = {"C", "D"}
    right_actions = {"C", "D"}
    actions_set = [left_actions, middle_actions, right_actions]
    all_actions = ["CCC", "CCD", "CDC", "CDD", "DCC", "DCD", "DDC", "DDD"]

    # transitions
    one_state_transition = {
        0: {"CCC": 0, "CCD": 2, "CDC": 1, "CDD": 1, "DCC": 3, "DCD": 2, "DDC": 3, "DDD": 0},
        1: {i: 1 for i in all_actions},
        2: {i: 2 for i in all_actions},
        3: {i: 3 for i in all_actions},
    }
    two_state_transition = {
        0: {"CCC": 0, "CCD": 2, "CDC": 1, "CDD": 1, "DCC": 3, "DCD": 2, "DDC": 3, "DDD": 0},
        1: {i: 1 for i in all_actions},
        2: {i: 2 for i in all_actions},
        3: {i: 3 for i in all_actions},
    }
    three_state_transition = {
        0: {"CCC": 0, "CCD": 2, "CDC": 1, "CDD": 1, "DCC": 3, "DCD": 2, "DDC": 3, "DDD": 0},
        1: {i: 1 for i in all_actions},
        2: {i: 2 for i in all_actions},
        3: {i: 3 for i in all_actions},
    }
    transitions = [one_state_transition, two_state_transition, three_state_transition]

    # strategies
    one_state_strategy = {
        0: "C",
        1: "D",
        2: "C",
        3: "C",
    }
    two_state_strategy = {
        0: "C",
        1: "C",
        2: "D",
        3: "C",
    }
    three_state_strategy = {
        0: "C",
        1: "C",
        2: "C",
        3: "D",
    }
    strategies = [one_state_strategy, two_state_strategy, three_state_strategy]

    games = {
        (0, 1): {"CC": 0, "CD": -v, "DC": v, "DD": -c},
        (1, 2): {"CC": 0, "CD": -v, "DC": v, "DD": -c},
        (0, 2): {"CC": 0, "CD": -v, "DC": v, "DD": -c},
    }

    check_SPE_state_machine_by_graph(3, games, transitions, strategies)
