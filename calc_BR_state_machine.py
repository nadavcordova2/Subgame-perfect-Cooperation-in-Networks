from check_SPE_state_machine import calc_long_term_util
from build_joint_state_machine import construct_joint_state_machine
import itertools


def calc_BR_state_machine_player_i_ver(player_i, transitions_funcs: list, strategy_funcs: list,
                                       utilities_by_actions: list, EPSILON=0.01):
    """
    Algorithm 4 in "Subgame-perfect Cooperation in Networks".

    :param player_i: the player to calculate his best-response.
    :param transitions_funcs: a list of the transitions functions without one for player_i.
    :param strategy_funcs: a list of the strategy functions without one for player_i.
    :param utilities_by_actions: The utilities of the players in the one-step game.
    :param EPSILON: 1-DELTA.

    :return: The joint strategy state machine that gives each player his original strategy, except player_i, that
    the joint machine gives him his best-response strategy to the other players' strategies.
    """
    N = len(utilities_by_actions)  # number of players
    actions_sets = [{"C", "D"} for i in range(N)]  # the possible actions for each player are "C" and "D"
    single_transition = {}
    for element in itertools.product(*actions_sets):
        action = "".join(element)
        single_transition[action] = 0

    transitions_funcs = transitions_funcs[:player_i] + [{0: single_transition}] + transitions_funcs[player_i:]
    strategy_funcs = strategy_funcs[:player_i] + [{0: "D"}] + strategy_funcs[player_i:]

    joint_Q, joint_f, joint_s = construct_joint_state_machine(actions_sets, transitions_funcs, strategy_funcs)

    dif_act = {
        "C": "D",
        "D": "C",
    }

    # the iteration that improves player_i strategy each step
    for cnt in range(len(joint_Q)):
        DELTA = 1 - EPSILON
        long_term_utilities = calc_long_term_util(EPSILON, joint_Q, utilities_by_actions, joint_f, joint_s)
        for state in joint_Q:
            curr_util = long_term_utilities[state][player_i]  # the utility of the current action
            action = joint_s[state]
            action = action[:player_i] + dif_act[action[player_i]] + action[player_i + 1:]

            one_move_util = utilities_by_actions[player_i][action]
            rest_game_util = long_term_utilities[joint_f[state][action]][player_i]
            diff_util = one_move_util + DELTA * rest_game_util  # the utility of the different action
            if diff_util > curr_util:
                joint_s[state] = action  # change player_i action to the new action

    return joint_Q, joint_f, joint_s
