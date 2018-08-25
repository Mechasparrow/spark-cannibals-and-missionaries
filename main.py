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
    missionaries = state[0]
    cannibals = state[1]
    boat = state[2]

    if (cannibals > missionaries and missionaries > 0):
        return False
    if ((3- cannibals) > (3 - missionaries) and ((3 - missionaries) > 0)):
        return False

    return ((cannibals <= 3 and cannibals >= 0) and
    (missionaries <= 3 and missionaries >= 0) and
    (boat == 0 or boat == 1))

# function that applies the action vector and yield the resulting state
def apply_action(state, action):

    a_mode = 1

    if (state[2] == 1):
        a_mode = -1
    elif (state[2] == 0):
        a_mode = 1

    res_state = [state[0] + (a_mode * action[0]), state[1] + (a_mode * action[1]), state [2] + (a_mode * action[2])]
    return res_state

# applies all possible actions to a given state and returns produced raw states + action taken
def apply_actions(state):

    res_states = []

    for action in actions:
        res_states.append((apply_action(state, action), action))

    return res_states

# filters through states and returns the valid ones
def filter_valid_states(states):

    filtered_states = []

    for state in states:
        if (is_state_valid(state)):
            filtered_states.append(state)

    return filtered_states

# filter through states with actions attached
def filter_valid_state_action_pairs(state_action_pairs):

    filtered_pairs = []

    for (state, action) in state_action_pairs:
        if (is_state_valid(state)):
            filtered_pairs.append((state, action))

    return filtered_pairs

# generates children for a specific depth and state
def generate_children(state, depth):

    mode = 1

    if ((depth + 1) % 2 == 0):
        mode = 1
    else:
        mode = -1

    raw_children = apply_actions(state)
    children = filter_valid_state_action_pairs(raw_children)

    return children

#generate child nodes
def generate_children_nodes(state, depth):

    children = generate_children(state, depth)

    children_nodes = []

    for (state, action) in children:
        children_nodes.append(gen_node(state, action, [], depth + 1))

    return children_nodes

# generate generic node
def gen_node(state, prev_action, children, depth):
    return {
        'state': state,
        'prev_action': prev_action,
        'children': children,
        'depth': depth
    }

# key name of specific state depth pairing
def state_depth_string(state, depth):
    state_str_raw = []

    for v_val in state:
        state_str_raw.append(str(v_val))

    state_str ="".join(state_str_raw)

    depth = depth
    return state_str + "_" + str(depth)

# get key for a specific node
def get_node_key(node):
    return state_depth_string(node['state'], node['depth'])

# generate the state tree
def gen_tree():


    depth = 0

    # Tree starts as empty dict
    tree = dict()

    # root node
    root_node = gen_node(state_initial, None, [], depth)
    tree[get_node_key(root_node)] = root_node

    goal_state = False

    while not goal_state:

        # get all the nodes at the current tree depth
        current_depth_nodes = [v for (k, v) in tree.items() if v['depth'] == depth]
        for node in current_depth_nodes:
            if (goal_state):
                break
            c_nodes = generate_children_nodes(node['state'], node['depth'])
            c_node_keys = [get_node_key(node) for node in c_nodes]

            node['children'] = c_node_keys

            for c_node in c_nodes:
                tree[get_node_key(c_node)] = c_node
                if (is_goal_state(c_node['state'])):
                    goal_state = True
                    depth+=1
                    break

        if (goal_state):
            break

        depth+=1

    tree['depth'] = depth
    return tree

# display the tree
def display_tree(tree):
    print (tree)

    print (tree['depth'])

    for dpth in range(0, tree['depth']+1):
        depth_nodes = [v for (k, v) in tree.items() if (k != "depth" and v['depth'] == dpth)]

        print ('Depth ' + str(dpth) + ":")
        for node in depth_nodes:
            print (node['state'])

# play the actions out
def simulate_solution(actions):
    current_state = state_initial

    print("starting situation")
    describe_state(current_state)
    action_alternate = False
    step = 0

    for action in actions:
        current_state = apply_action(current_state, action)
        step += 1
        print()
        print("Step: " + str(step))
        print ("Take the following action: ")
        describe_action(action, action_alternate)
        action_alternate = (not action_alternate)

        print()
        print("current situation:")
        describe_state(current_state)

    print ("done")

# describe the actions taken
def describe_action(action, alternate):

    cannibals = action[1]
    missionaries = action[0]
    boat = action[2]

    ending_phrase = ""

    if (alternate == True):
        ending_phrase = "to the Left"
    elif (alternate == False):
        ending_phrase = "to the Right"

    print ("Take " + str(cannibals) + " cannibals and " + str(missionaries) + " missionaries with the " + str(boat) + " boat " + ending_phrase)

# describe the current state
def describe_state(state):
    cannibals = state[1]
    missionaries = state[0]
    boat = state[2]

    print (str(cannibals) + " cannibals on the left bank")
    print (str(missionaries) + " missionaries on the left bank")
    print (str(boat) + " boat on the left bank")


    print (str(3 - cannibals) + " cannibals on the right bank")
    print (str(3 - missionaries) + " missionaries on the right bank")
    print (str(1 - boat) + " boat on the right bank")

# get the list of actions to win by traversing in reverse from the goal node i.e backtrack
def get_winning_path(tree):

    actions_to_goal = []
    goal_node = [v for (k, v) in tree.items() if (k != "depth" and v['state'] == goal_state)][0]
    current_node = goal_node

    depth = tree['depth']

    while (depth != 0):
        depth = depth -1

        # appends action taken to get to current_node
        actions_to_goal.append(current_node['prev_action'])

        new_state = apply_action(current_node['state'], current_node['prev_action'])
        key = state_depth_string(new_state, depth)

        current_node = [v for (k, v) in tree.items() if (k == key)][0]

    return actions_to_goal[::-1]

# random tests
def run_tests():
    print ("tests 001:")
    res_states = apply_actions(state_initial)
    print (res_states)
    print()

    print ("tests 002:")
    res_states = generate_children(state_initial, 0)
    for (state, action) in res_states:
        print (state)
    print()

# runs the actual program
def run():
    print("running program")

    print ("generating state tree...")
    state_tree = gen_tree()
    print()

    print ("tree generated")

    winning_actions = get_winning_path(state_tree)
    simulate_solution(winning_actions)

if __name__ == "__main__":
    run()
