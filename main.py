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

#checks if the state is valid
# you cant have cannibals outnumber missionaries...
# or they will eat the missionaries

def generate_node(state, prev_action, children):
    return {
        "state": state,
        "prev_action": prev_action,
        "children": children
    }

def valid_state(state):
    cannibals = state[1]
    missionaries = state[0]
    wrong_side_boat = state[2]

    if (cannibals > 3 or missionaries > 3 or wrong_side_boat > 1):
        return False

    return (cannibals <= missionaries)

def is_goal_state(state):
    return (state == goal_state)

def apply_actions_w_nodes (state):
    return apply_actions(state, nodes = True)

def apply_actions(state, nodes = False):

    next_states = []

    for action in actions:
        next_state = apply_action(state, action)

        if (valid_state(next_state)):
            if (nodes == False):
                next_states.append(next_state)
            elif (nodes == True):
                child_node = generate_node(next_state, action, None)
                next_states.append(child_node)

    return next_states

# Applies an action
def apply_action(state, action, reverse = False):
    boat_on_wrong_side = (state[2]) == 1

    # make a copy of the current state (just for immutability)
    new_state = copy.copy(state)

    # determines whether vector should be added or subtracted if the boat is on the wrong side
    vector_multiplier = 1

    if (boat_on_wrong_side):
        vector_multiplier = -1
    else:
        vector_multiplier = 1

    if (reverse):
        vector_multiplier *= -1

    # apply vector addition/subtraction to the state to yield the new state
    for i in range(0, vector_length):
        new_state[i] = new_state[i] + (vector_multiplier * action[i])

    return new_state

# figure this out
def recur_children(children):
    new_children = copy.copy(children)
    final_children = []

    for i in range(0, len(new_children)):
        new_children[i]['children'] = apply_actions_w_nodes(new_children[i]['state'])

    goal_found = False

    for child in new_children:
        for c in child['children']:

            if (is_goal_state(c['state'])):
                goal_found = True

    if (goal_found == False):
        for i in range(0, len(new_children)):
            new_children[i]['children'] = recur_children(new_children[i]['children'])

    return new_children

#figure this out
def gen_tree(state=state_initial, prev_action = None):
    children = apply_actions_w_nodes(state)

    new_children = recur_children(children)

    tree = generate_node(state, prev_action, new_children)

    return tree


def run():
    print("running program")

    tree = gen_tree()
    print ("tree: ", str(tree))

    pass

if __name__ == "__main__":
    run()
