import numpy as np
import itertools
from build_joint_state_machine import construct_joint_state_machine


def find_cycles(graph):
    """
    Finds cycles in a directed graph, using DFS.

    :param graph:  The directed graph represented as a dictionary where keys are nodes and values are their neighbors.
    :return:  A list of lists where each sublist represents a cycle in the graph.
    """
    visited_nodes = set()
    current_path = []
    cycles = []  # The final result, a list of cycles

    def depth_first_search(node):
        """
        Depth-first search.
        """
        if node in visited_nodes:
            # If the node has already been visited, it means we have found a cycle
            if node in current_path:
                start_index = current_path.index(node)
                cycles.append(current_path[start_index:])
            return

        # Mark the node as visited
        visited_nodes.add(node)

        current_path.append(node)
        depth_first_search(graph[node])
        current_path.pop()

    for node_out in graph:
        if node_out not in visited_nodes:
            depth_first_search(node_out)

    return cycles


def calc_long_term_util(EPSILON, joint_states, utilities_by_actions, transition_funcs, strategy_funcs):
    """
    Algorithm 2 in "Subgame-perfect Cooperation in Networks".
    The function calculate the long term utility as was defined in the paper.

    :param EPSILON: 1-DELTA.
    :param joint_states: The states of the joint strategy state machine.
    :param utilities_by_actions: The utilities for the players in the one-step game.
    :param strategy_funcs: The strategy functions of the joint strategy state machine.
    :param transition_funcs: The transitions function of the joint strategy state machine.

    :return: The long term utility function.
    """
    num_players = len(joint_states[0])
    DELTA = 1 - EPSILON
    graph = {s: transition_funcs[s][strategy_funcs[s]] for s in joint_states}
    cycles = find_cycles(graph)

    long_term_util = {s: np.zeros(3) for s in joint_states}
    remaining_states = joint_states.copy()
    calculated_states = []
    # Need to calculate the utilities of the cycles... (A + delta * B + delta ^ 2 * C + ...) / (1 - delta ^ length)
    for c in cycles:
        init_node = c[0]
        util_sum = np.zeros(num_players)
        for node in range(len(c)):
            util_sum += (DELTA ** node) * np.array(
                [utilities_by_actions[i][strategy_funcs[c[node]]] for i in range(num_players)])
        long_term_util[init_node] = util_sum / (1 - (DELTA ** len(c)))
        remaining_states.remove(init_node)
        calculated_states.append(init_node)

    # calculate the long term utilities of each player in each state
    while len(remaining_states) != 0:
        for state in remaining_states:
            action = strategy_funcs[state]
            if transition_funcs[state][action] not in calculated_states:
                continue
            cur_action_util = [utilities_by_actions[i][action] for i in range(num_players)]
            long_term_util[state] = np.array(cur_action_util) + DELTA * long_term_util[transition_funcs[state][action]]
            remaining_states.remove(state)
            calculated_states.append(state)
    return long_term_util


def check_SPE_state_machine(joint_states: list, transition_funcs: dict, strategy_funcs: dict,
                            utils_by_actions: list, EPSILON=0.01):
    """
    Given a joint strategy state machine, when each player has the same set of actions: {"C", "D"}, check whether the
    strategies of the joint state machine represent a subgame perfect equilibrium, and if not print the possible
    deviations in the state machine.

    :param joint_states: The state of the joint strategy state machine.
    :param transition_funcs: A list of state transition functions for each player.
    :param strategy_funcs: A list of state-action mappings for each player.
    :param utils_by_actions: The utilities of the players in the one-step game.
    :param EPSILON: 1-DELTA.

    :return: True if the strategies are SPE, otherwise False.
    """
    DELTA = 1 - EPSILON
    long_term_util = calc_long_term_util(EPSILON, joint_states, utils_by_actions, transition_funcs, strategy_funcs)
    num_players = len(joint_states[0])

    # check deviations in each state for each player
    dif_act = {
        "C": "D",
        "D": "C",
    }

    SPE = True
    for state in joint_states:
        eq_utility = long_term_util[state]

        for i in range(num_players):
            action = strategy_funcs[state]
            action = action[:i] + dif_act[action[i]] + action[i + 1:]
            dif_act_utility = [utils_by_actions[j][action] for j in range(num_players)]
            if dif_act_utility[i] + DELTA * long_term_util[transition_funcs[state][action]][i] > eq_utility[i]:
                print("in state:", state, "player", i, "dont play BR")
                SPE = False

    if SPE:
        print("SPE")
    else:
        print("not SPE")
    return SPE


def calculate_single_player_utility_by_graph(n: int, games: dict, player: int, players_actions):
    """
    Given a graph, a player, and the games on each of his nodes, calculate the utilities matching for every possible
    combinations of actions of all the players in the (one shot) game.

    :param n: The number of players.
    :param games: A dictionary mapping  edges to the matching two player game.
    :param player: The player we want to calculate his utilities.
    :param players_actions: players_actions[i] is a list of possible actions for player i.

    :return: The utilities for the given player for every possible combination of actions in the one shot game.
    """
    utilities = {}
    for element in itertools.product(*players_actions):
        action = "".join(element)
        act_utility = 0
        for k in range(n):
            if k != player and (k, player) in games:
                act_utility += games[(k, player)][action[player] + action[k]]
        utilities[action] = act_utility

    return utilities


def check_SPE_state_machine_by_graph(n: int, games: dict, transition_funcs, strategy_funcs, EPSILON=0.01):
    """
    Algorithm 3 in "Subgame-perfect Cooperation in Networks".
    Given n players, a dictionary that contains the edges in the graph of the players and the two player game
    for every edge, also given a joint strategy state machine, the function returns whether the strategies are SPE
    in the repeated game on the graph.

    :param n: the number of players.
    :param games: a dict with keys as edges (i,j) in the graph, and the values are the utility 'matrices' of player i from
    the symmetric game where each of i,j choose an action from {C,D}.
    The 'matrices' are also dicts with the entries as "CC", "CD", "DC" and "DD".
    meaning: games[(1, 2)]["CD"] gives the utility for a player when he plays C and the other player plays D.
    :param transition_funcs: the transitions of the single player state machine strategy.
    :param strategy_funcs: the actions of the single player state machine strategy.
    :param EPSILON: 1 - DELTA, the discount factor.

    :return: True if the strategies are SPE in the DELTA-discounted game of the game constructed from the sum of the
    utilities of the games on each edge.
    """
    run_on = list(games.keys())
    for edge in run_on:
        games[(edge[1], edge[0])] = games[edge]

    actions_sets = [{"C", "D"} for i in range(n)]
    utilities = [calculate_single_player_utility_by_graph(n, games, i, actions_sets) for i in range(n)]

    joint_Q, joint_f, joint_s = construct_joint_state_machine(actions_sets, transition_funcs, strategy_funcs)

    return check_SPE_state_machine(joint_Q, joint_f, joint_s, utilities, EPSILON=EPSILON)
