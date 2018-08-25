# for immutability not really needed but ya know
import copy

#vector format is [m, c, b]
# missionaries, cannibals, and whether or not boat is on right side

vector_length = 3

# action vectors
actions = [
    [1, 0, 1],
    [2, 0, 1],
    [0, 1, 1],
    [0, 2, 1],
    [1, 1, 1]
]

# using vector addition + subtraction, goal is to get to goal state where there are 0 cannibals, 0 missionaries, and no boat on the wrong side

state_initial = [3, 3, 1]
goal_state = [0, 0, 0]

# generates all possible states
def possible_states():

    pos_states = []

    for b in range(0,2):
        for c in range(0,4):
            for m in range(0,4):
                pos_states.append([m, c, b])

    return pos_states

# Checks if goal state is reached
def is_goal_state(state):
    return (state == goal_state)

# Checks if state is even valid
def is_state_valid(state):
    cannibals = state[1]
    missionaries = state[0]

    return (not cannibals > missionaries)


# function that applies the action vector and yield the resulting state
def apply_action(state, action, mode = 1):

    res_state = [state[0] + (mode * action[0]), state[1] + (mode * action[1]), state [2] + (mode * action[2])]
    return res_state

# applies all possible actions to a given state and returns produced raw states
def apply_actions(state, mode = 1):

    res_states = []

    for action in actions:
        res_states.append(apply_action(state, action, mode))

    return res_states

# filters through states and returns the valid ones
def filter_valid_states(states):

    filtered_states = []

    for state in states:
        if (is_state_valid(state)):
            filtered_states.append(state)

    return filtered_states

# generates children for a specific depth and state
def generate_children(state, depth):

    mode = 1

    if ((depth + 1) % 2 == 0):
        mode = 1
    else:
        mode = -1

    raw_children = apply_actions(state, mode)
    children = filter_valid_states(raw_children)

    return children

def gen_node(state, prev_action, children, depth):
    return {
        'state': state,
        'prev_action': prev_action,
        'children': children,
        'depth': depth
    }

def gen_tree():

    tree = gen_node(state_initial, None, [], 0)

    ## TODO implement state tree gen



    return tree


def run():
    print("running program")
    print ("possible states")

    pos_states = possible_states()
    for pos_state in pos_states:
        print (pos_state)

    print()

    print ("starting state is ")
    print (state_initial)
    print()

    print ("goal state is ")
    print (goal_state)
    print()

    print ("generating state tree...")
    state_tree = gen_tree()

    print (state_tree)
    print()

    # Tests
    print ("tests 001")
    res_states = apply_actions(state_initial, mode = -1)
    print (res_states)
    print()

    print ("tests 002")
    res_states = generate_children(state_initial, 0)
    print (res_states)
    print()

    pass

if __name__ == "__main__":
    run()
