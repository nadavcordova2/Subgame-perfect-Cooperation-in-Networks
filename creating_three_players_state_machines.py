from check_SPE_state_machine import check_SPE_state_machine_by_graph

all_actions = ["CCC", "CCD", "CDC", "CDD", "DCC", "DCD", "DDC", "DDD"]


def side_state_machine(punish_num, trust_gain_num):
    """
    Creating part of the side player strategy state machine - all the states without the initial state.

    :param punish_num: The number of steps of punishment.
    :param trust_gain_num: The number of steps after the middle has deviated he need to play "C" the gain the edge
    players trust back.

    :return: The side player state machine strategy, without the initial state.
    """
    state_transition = {}

    # CD?
    for i in range(1, punish_num - 1):
        state_transition[i] = {j: i + 1 for j in all_actions}
    for i in range(punish_num - 1, punish_num + trust_gain_num - 2):
        state_transition[i] = {"CCC": i + 1, "CCD": i + 1, "CDC": 1, "CDD": 1, "DCC": i + 1, "DCD": i + 1, "DDC": 1,
                               "DDD": 1}
    state_transition[punish_num + trust_gain_num - 2] = {"CCC": 0, "CCD": 0, "CDC": 1, "CDD": 1, "DCC": 0, "DCD": 0,
                                                         "DDC": 1, "DDD": 1}

    # DC?
    DC_state = punish_num + trust_gain_num - 1
    state_transition[DC_state] = {"CCC": DC_state, "CCD": DC_state, "CDC": DC_state + 1, "CDD": DC_state + 1,
                                  "DCC": DC_state, "DCD": DC_state, "DDC": DC_state + 1, "DDD": DC_state + 1}
    for i in range(punish_num + trust_gain_num, 2 * punish_num + trust_gain_num - 3):
        state_transition[i] = {j: i + 1 for j in all_actions}
    state_transition[2 * punish_num + trust_gain_num - 3] = {j: 0 for j in all_actions}

    # DD?
    for i in range(2 * punish_num + trust_gain_num - 2, 3 * punish_num + trust_gain_num - 5):
        state_transition[i] = {j: i + 1 for j in all_actions}
    state_transition[3 * punish_num + trust_gain_num - 5] = {j: 0 for j in all_actions}

    state_action = {i: "D" for i in range(3 * punish_num + trust_gain_num - 4)}
    state_action[0] = "C"

    return state_transition, state_action


def left_state_machine(punish_num, trust_gain_num):
    """
    Creating the left player strategy state machine.

    :param punish_num: The number of steps of punishment.
    :param trust_gain_num: The number of steps after the middle has deviated he need to play "C" the gain the edge
    players trust back.

    :return: The left player state machine strategy.
    """
    left_state_transition, left_state_action = side_state_machine(punish_num, trust_gain_num)

    # CC?
    CC = 0
    CD = 1
    DC = punish_num + trust_gain_num - 1
    DD = 2 * punish_num + trust_gain_num - 2
    left_state_transition[0] = {"CCC": CC, "CCD": CC, "CDC": CD, "CDD": CD, "DCC": DC, "DCD": DC, "DDC": DD, "DDD": DD}

    return left_state_transition, left_state_action


def right_state_machine(punish_num, trust_gain_num):
    """
    Creating the right player strategy state machine.

    :param punish_num: The number of steps of punishment.
    :param trust_gain_num: The number of steps after the middle has deviated he need to play "C" the gain the edge
    players trust back.

    :return: The right player state machine strategy.
    """
    right_state_transition, right_state_action = side_state_machine(punish_num, trust_gain_num)

    # CC?
    CC = 0
    CD = punish_num + trust_gain_num - 1
    DC = 1
    DD = 2 * punish_num + trust_gain_num - 2
    right_state_transition[0] = {"CCC": CC, "CCD": CD, "CDC": DC, "CDD": DD, "DCC": CC, "DCD": CD, "DDC": DC, "DDD": DD}

    return right_state_transition, right_state_action


def middle_state_machine(punish_num, trust_gain_num):
    """
    Creating the middle player strategy state machine.

    :param punish_num: The number of steps of punishment.
    :param trust_gain_num: The number of steps after the middle has deviated he need to play "C" the gain the edge
    players trust back.

    :return: The middle player state machine strategy.
    """
    # the number of the state in the machine matching for the next deviation (when all the players cooperated):
    CCC = 0
    DDD = 1
    DDC = punish_num - 1
    CDC = 2 * punish_num + trust_gain_num - 3
    DCD = 3 * punish_num + 2 * trust_gain_num - 5
    DCC = 4 * punish_num + 2 * trust_gain_num - 6
    CDD = 6 * punish_num + 3 * trust_gain_num - 10
    CCD = 7 * punish_num + 4 * trust_gain_num - 12

    # CCC - cooperation
    middle_f = {CCC: {"CCC": CCC, "CCD": CCD, "CDC": CDC, "CDD": CDD, "DCC": DCC, "DCD": DCD, "DDC": DDC, "DDD": DDD}}
    middle_s = {CCC: "C"}

    # DDD - all the players have deviated
    for i in range(DDD, DDC):
        middle_f[i] = {j: (i + 1) % (punish_num - 1) for j in all_actions}
        middle_s[i] = "D"

    # DDC - left and middle player deviated
    for i in range(DDC, DDC + punish_num - 2):
        middle_f[i] = {j: i + 1 for j in all_actions}
        middle_s[i] = "D"
    for i in range(DDC + punish_num - 2, CDC - 1):
        middle_f[i] = {"CCC": i + 1, "CCD": i + 1, "CDC": CDC, "CDD": CDC, "DCC": DCC - DDC + i + 1,
                       "DCD": DCC - DDC + i + 1, "DDC": DDC, "DDD": DDC}
        middle_s[i] = "C"

    middle_f[CDC - 1] = {"CCC": CCC, "CCD": CCC, "CDC": CDC, "CDD": CDC, "DCC": DCC, "DCD": DCC, "DDC": DDC, "DDD": DDC}
    middle_s[CDC - 1] = "C"

    # CDC - middle player deviated
    for i in range(CDC, CDC + punish_num - 2):
        middle_f[i] = {j: i + 1 for j in all_actions}
        middle_s[i] = "D"
    for i in range(CDC + punish_num - 2, DCD - 1):
        middle_f[i] = {"CCC": i + 1, "CCD": i + 1, "CDC": CDC, "CDD": CDC, "DCC": i + 1, "DCD": i + 1, "DDC": CDC,
                       "DDD": CDC}
        middle_s[i] = "C"

    middle_f[DCD - 1] = {"CCC": CCC, "CCD": CCC, "CDC": CDC, "CDD": CDC, "DCC": CCC, "DCD": CCC, "DDC": CDC, "DDD": CDC}
    middle_s[DCD - 1] = "C"

    # DCD - edge players deviated.
    middle_f[DCD] = {"CCC": DCD, "CCD": DCD, "CDC": DCD + 1, "CDD": DCD + 1,
                     "DCC": DCD, "DCD": DCD, "DDC": DCD + 1, "DDD": DCD + 1}
    middle_s[DCD] = "D"
    for i in range(DCD + 1, DCC):
        middle_f[i] = {j: (i + 1) % DCC for j in all_actions}
        middle_s[i] = "D"

    # DCC - left player deviated
    middle_f[DCC] = {"CCC": DCC, "CCD": DCD, "CDC": DCC + 1, "CDD": DCC + punish_num + trust_gain_num - 2, "DCC": DCC,
                     "DCD": DCD, "DDC": DCC + 1, "DDD": DCC + punish_num + trust_gain_num - 2}
    middle_s[DCC] = "D"
    for i in range(DCC + 1, DCC + punish_num - 2):
        middle_f[i] = {j: i + 1 for j in all_actions}
        middle_s[i] = "D"
    middle_f[DCC + punish_num - 2] = {j: DDC + punish_num - 2 for j in all_actions}
    middle_s[DCC + punish_num - 2] = "D"

    if trust_gain_num > 1:
        for i in range(DCC + punish_num - 1, DCC + punish_num + trust_gain_num - 3):
            middle_f[i] = {"CCC": i + 1, "CCD": i + 1, "CDC": DCC + 1, "CDD": DCC + 1, "DCC": i + 1, "DCD": i + 1,
                           "DDC": DCC + 1, "DDD": DCC + 1}
            middle_s[i] = "D"
        middle_f[DCC + punish_num + trust_gain_num - 3] = {"CCC": DCC, "CCD": DCC, "CDC": DCC + 1, "CDD": DCC + 1,
                                                           "DCC": DCC, "DCD": DCC, "DDC": DCC + 1, "DDD": DCC + 1}
        middle_s[DCC + punish_num + trust_gain_num - 3] = "D"

    for i in range(DCC + punish_num + trust_gain_num - 2, DCC + 2 * punish_num + trust_gain_num - 4):
        middle_f[i] = {j: (i + 1) % (DCC + 2 * punish_num + trust_gain_num - 4) for j in all_actions}
        middle_s[i] = "D"

    # CDD - middle and right player deviated
    for i in range(CDD, CDD + punish_num - 2):
        middle_f[i] = {j: i + 1 for j in all_actions}
        middle_s[i] = "D"
    for i in range(CDD + punish_num - 2, CCD - 1):
        middle_f[i] = {"CCC": i + 1, "CCD": CCD - CDD + i + 1, "CDC": CDC, "CDD": CDD,
                       "DCC": i + 1, "DCD": CCD - CDD + i + 1, "DDC": CDC, "DDD": CDD}
        middle_s[i] = "C"

    middle_f[CCD - 1] = {"CCC": CCC, "CCD": CCD, "CDC": CDC, "CDD": CDD,
                         "DCC": CCC, "DCD": CCD, "DDC": CDC, "DDD": CDD}
    middle_s[CCD - 1] = "C"

    # CCD - right player deviated
    middle_f[CCD] = {"CCC": CCD, "CCD": CCD, "CDC": CCD + 1, "CDD": CCD + 1, "DCC": DCD, "DCD": DCD,
                     "DDC": CCD + punish_num + trust_gain_num - 2, "DDD": CCD + punish_num + trust_gain_num - 2}
    middle_s[CCD] = "D"
    for i in range(CCD + 1, CCD + punish_num - 2):
        middle_f[i] = {j: i + 1 for j in all_actions}
        middle_s[i] = "D"

    middle_f[CCD + punish_num - 2] = {j: CDD + punish_num - 2 for j in all_actions}
    middle_s[CCD + punish_num - 2] = "D"

    if trust_gain_num > 1:
        for i in range(CCD + punish_num - 1, CCD + punish_num + trust_gain_num - 3):
            middle_f[i] = [i + 1, i + 1, CCD + 1, CCD + 1] * 2
            middle_f[i] = {"CCC": i + 1, "CCD": i + 1, "CDC": CCD + 1, "CDD": CCD + 1,
                           "DCC": i + 1, "DCD": i + 1, "DDC": CCD + 1, "DDD": CCD + 1}
            middle_s[i] = "D"
        middle_f[CCD + punish_num + trust_gain_num - 3] = {"CCC": CCD, "CCD": CCD, "CDC": CCD + 1,
                                                           "CDD": CCD + 1,
                                                           "DCC": CCD, "DCD": CCD, "DDC": CCD + 1,
                                                           "DDD": CCD + 1}
        middle_s[CCD + punish_num + trust_gain_num - 3] = "D"

    for i in range(CCD + punish_num + trust_gain_num - 2, CCD + 2 * punish_num + trust_gain_num - 4):
        middle_f[i] = {j: (i + 1) % (CCD + 2 * punish_num + trust_gain_num - 4) for j in all_actions}
        middle_s[i] = "D"

    return middle_f, middle_s


def create_three_players_state_machines(c, d, l, EPSILON=0.01):
    """
    Section 5.2.1 in "Subgame-perfect Cooperation in Networks".
    This function returns three single player strategy state machines, so that this strategies are SPE in the V graph
    left-middle-right, for the repeated prisoner's dilemma, with parameters c,d,l and DELTA=1-EPSILON as given to
    the function.

    :param c: The utility for each of the players in the PD when they both cooperate.
    :param d: The utility for a deviating player when the other player hasn't deviated in the PD.
    :param l: The utility for a cooperating player when the other player has deviated in the PD.
    :param EPSILON: 1 - DELTA.

    :return: The single player strategy state machine of the three players.
    """
    # the number of steps of punishment and "gaining trust back".
    punish_num = max([(d // c) + 1, 3])
    trust_gain_num = (l // (d - c)) + 1

    # the strategies of the players
    left_state_transition, left_state_action = left_state_machine(punish_num, trust_gain_num)
    middle_state_transition, middle_state_action = middle_state_machine(punish_num, trust_gain_num)
    right_state_transition, right_state_action = right_state_machine(punish_num, trust_gain_num)

    transitions_funcs = [left_state_transition, middle_state_transition, right_state_transition]
    strategy_funcs = [left_state_action, middle_state_action, right_state_action]

    # check that the strategies are indeed SPE
    games = {
        (0, 1): {"CC": c, "CD": -l, "DC": d, "DD": 0},
        (1, 2): {"CC": c, "CD": -l, "DC": d, "DD": 0},
    }
    check_SPE_state_machine_by_graph(3, games, transitions_funcs, strategy_funcs)

    return transitions_funcs, strategy_funcs


create_three_players_state_machines(1, 2, 4)
