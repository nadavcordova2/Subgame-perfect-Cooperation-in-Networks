# Subgame-perfect Cooperation in Networks
This repository contains the algorithms presented in the "Subgame-perfect Cooperation in Networks" thesis by Nadav Cordova from the Hebrew University. It includes four algorithms, each located in a separate file:

* Algorithm 1: Constructs a joint strategy state machine from the single-player state machines of multiple players. File: build_joint_state_machine.py
* Algorithm 2: Calculates the long-term utility function of a joint state machine. File: check_SPE_state_machine.py
* Algorithm 3: Checks if given strategies are Subgame Perfect Equilibrium (SPE) when provided as a joint state machine or single-player state machines. File: check_SPE_state_machine.py
* Algorithm 4: Calculates a player's best-response strategy given the strategy state machines of all other players. File: calc_BR_state_machine.py

In addition, the repository contains examples discussed in the fifth section of the thesis:

* File: creating_three_players_state_machines.py - This file contains functions that create strategy state machines for three players in a "V" graph, specifically for the repeated prisoner's dilemma with customizable parameters and a discount factor close to 1.
* File: examples.py - This file includes various examples of state machines whose strategies represent Subgame Perfect Equilibrium in different types of games.

Feel free to explore the algorithms and examples provided in this repository.
