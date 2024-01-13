import random
import graph

class CNode:
    def __init__(self, contextvector, state):
        self.node = (contextvector, state)

    def __str__(self):
        return f"Node({self.node[0]}, {self.node[1]})"
    
    def __eq__(self, other):
        # Define equality based on the contextvector and state
        return isinstance(other, CNode) and self.node == other.node
    
    def __hash__(self):
        # Hash based on the hash of the tuple (contextvector, state)
        return hash(self.node)
    

class CGraph:
    def __init__(self, next_states):
        self.nodes = {}
        self.next_states = next_states

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = []
            # Establish connections for this node to next states
            self.connect_to_all_current_states(node)
        return node

    def connect_to_all_current_states(self, node, weight=1):
        # Connect the given node to all current states in self.next_states with the specified weight
        for state in self.next_states:
            self.nodes[node].append((state, weight))

    def get_next_state(self, node):
        # Return the state with the highest weight in self.nodes[node]
        if node not in self.nodes:
            self.add_node(node)
        if len(self.next_states) == 0:
            return graph.State("No Environments", "No States")
        
        connections = self.nodes.get(node, [])

        # Find the state(s) with the highest weight
        max_weight = max(connections, key=lambda x: x[1])[1]
        max_weight_states = [state for state, weight in connections if weight == max_weight]

        # If there is a tie in weights, return a random state among the tied states
        return random.choice(max_weight_states)

    # Strengthen connection based on feedback
    def increase_connection(self, node, next_state, update_value=0.1):
        # Increase the weight of the connection between the given node and next_state
        if node in self.nodes:
            for i, connection in enumerate(self.nodes[node]):
                if connection[0] == next_state:
                    updated_connection = (connection[0], connection[1] + update_value)
                    self.nodes[node][i] = updated_connection

    # Weaken connection based on feedback
    def decrease_connection(self, node, next_state, update_value=-0.1):
        # Increase the weight of the connection between the given node and next_state
        if node in self.nodes:
            for i, connection in enumerate(self.nodes[node]):
                if connection[0] == next_state:
                    updated_connection = (connection[0], connection[1] + update_value)
                    self.nodes[node][i] = updated_connection


# state1 = graph.State("env1", "")
# state2 = graph.State("env2", "")
# state3 = graph.State("env3", "")
# state4 = graph.State("env4", "")

# cgraph = CGraph([state1, state2, state3, state4])

# cv1 = graph.ContextVector("Forest", "Player1", "alive", "Walking", "Tree")
# cv2 = graph.ContextVector("City", "Player2", "alive", "Resting", "Building")
# cv3 = graph.ContextVector("Village", "Player3", "no hit points", "Dead", "Well")

# node = CNode(cv1, state1)
# node2 = CNode(cv1, state1)

# cgraph.add_node(node)
# cgraph.add_node(node2)


# cgraph.increase_connection(node, state3)
# nxt = cgraph.get_next_state(node2)
# print(nxt)









