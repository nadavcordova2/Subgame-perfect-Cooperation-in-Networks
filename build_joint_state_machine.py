import itertools


def construct_joint_state_machine(players_actions: list, transition_funcs: list, strategy_funcs: list):
    """
    Algorithm 1 in "Subgame-perfect Cooperation in Networks".
    Find the joint states, transitions, and actions for the joint strategy state machine.

    :param players_actions: players_actions[i] is a list of possible actions for player i.
    :param transition_funcs: transition_funcs[i] is a dict so that transition_funcs[i][q][action] when q is a state and
    'action' is a string returns the state that the state machine of player i goes to from state q after 'action'.
    :param strategy_funcs: strategy_funcs[i] is a dict so that strategy_funcs[i][q] returns the action from
    players_actions[i] to play in state q.

    :return: The joint strategy state machine of all the players, as described in the paper.
    """
    num_players = len(players_actions)
    # the initial states of the state machines are 0
    initial_state = tuple(0 for i in range(num_players))
    joint_states = [initial_state]
    states_queue = [initial_state]
    joint_transition = {}
    joint_strategy_func = {}

    while len(states_queue) != 0:
        q = states_queue.pop(0)
        q_action = "".join([strategy_funcs[i][q[i]] for i in range(num_players)])
        joint_strategy_func[q] = q_action

        q_transitions = {}
        for element in itertools.product(*players_actions):
            action = "".join(element)
            q_transitions[action] = tuple(transition_funcs[i][q[i]][action] for i in range(num_players))
        joint_transition[q] = q_transitions

        for state in q_transitions.values():
            if state not in joint_states:
                joint_states.append(state)
                states_queue.append(state)

    return joint_states, joint_transition, joint_strategy_func
