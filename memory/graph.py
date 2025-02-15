import pickle
import random


def calculate_similarity(state_vector1, state_vector2):
    similarity = sum(1 for a, b in zip(state_vector1.state_vector, state_vector2.state_vector) if a == b)
    total_attributes = len(state_vector1.state_vector)
    return similarity / total_attributes


class ContextVector:
    def __init__(self, environment, player_character, character_state, action, obj):
        self.state_vector = (environment, (player_character, character_state, action, obj))

    def __str__(self):
        return f"ContextVector(state_vector={self.state_vector})"

class State:
    def __init__(self, environment, previousgptstory):
        self.state_vector = (environment, [], previousgptstory)
    
    def __str__(self):
        return f"State({self.state_vector})"


class Node:
    def __init__(self, data, weight=1, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
        self.weight = weight

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        parent_data = self.parent.data if self.parent else "None"
        children_data = [child.data for child in self.children]
        return f"Node(Data: {self.data}, Weight: {self.weight}, Parent: {parent_data}, Children: {children_data})"


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, data, parent=None):
        node = Node(data, 1, parent)
        if parent:
            parent.add_child(node)
        self.nodes.append(node)
        return node

    def find_similar_state_vector(self, target_state_vector):
        max_similarity = 1.0
        most_similar_node = None

        for node in self.nodes:
            if isinstance(node.data, ContextVector):
                similarity = calculate_similarity(target_state_vector, node.data)
                if similarity >= max_similarity:
                    max_similarity = similarity
                    most_similar_node = node

        return most_similar_node

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            loaded_graph = pickle.load(file)
            # Copy the loaded data to the current object
            self.nodes = loaded_graph.nodes


    def get_next_state(self, node):
        total = 0
        for child in node.children:
            total += child.weight

        probabilities = []
        for child in node.children:
            probabilities.append(child.weight / total)
        
        child_index = random.choices(range(len(probabilities)), weights=probabilities, k=1)[0]
        return node.children[child_index]
    
    
    def update_weight(self, cv, state, value):
        for s in cv.children:
            if s == state:
                s.weight = s.weight + value








# Example usage
# graph = Graph()

# # Creating ContextVector instances
# state1 = ContextVector("Forest", "PlayerCharacter", "alive", "Walking", "None")
# state2 = ContextVector("City", "PlayerCharacter", "alive", "Interacting", "merchant")
# state3 = ContextVector("Village", "PlayerCharacter", "no hitpoints", "Death saving throw", "ground")
# state4 = ContextVector("Camp", "PlayerCharacter", "alive", "Interacting", "tent")
# state5 = ContextVector("Forest", "PlayerCharacter", "alive", "Fighting", "bear")
# state6 = ContextVector("City", "PlayerCharacter", "no hitpoints", "Dead", "ground")
# state7 = ContextVector("Village", "PlayerCharacter", "alive", "Resting", "fire")
# state8 = ContextVector("Camp", "PlayerCharacter", "alive", "Fighting", "bandits")
# state9 = ContextVector("City", "PlayerCharacter", "alive", "Walking", "buildings")
# state10 = ContextVector("Forest", "PlayerCharacter", "alive", "Interacting", "map")

# # Adding states as nodes to the graph
# node1 = graph.add_node(state1)
# node2 = graph.add_node(state2)
# node3 = graph.add_node(state3)
# node4 = graph.add_node(state4)
# node5 = graph.add_node(state5)
# node6 = graph.add_node(state6)
# node7 = graph.add_node(state7)
# node9 = graph.add_node(state9)
# node10 = graph.add_node(state10)

# # Connecting nodes
# state1 = State("Forest", None)
# state2 = State("Forest", None)
# state3 = State("Camp", None)
# state_node1 = graph.add_node(state1, node1)
# node5 = graph.add_node(state5, state_node1)
# state_node2 = graph.add_node(state2, node5)
# node8 = graph.add_node(state8, state_node2)


# # state_node3 = graph.add_node(state3, node8)


# # Save the graph to a file
# graph.save_to_file("graph.txt")

# # Load the graph from a file
# loaded_graph = Graph()
# loaded_graph.load_from_file("graph.txt")

# # Find a similar state vector and get its child nodes
# new_state_vector = ContextVector("Forest", "Player1", "alive", "Walking", "Tree")
# similar_node = loaded_graph.find_similar_state_vector(new_state_vector)

# if similar_node:
#     print("Most similar state vector found. Child node data:")
#     child_data = similar_node.children[0].data
#     if isinstance(child_data, ContextVector):
#         print("Environment:", child_data.state_vector[0])
#         print("Player Character:", child_data.state_vector[1][0])
#         print("Character State:", child_data.state_vector[1][1])
#         print("Action:", child_data.state_vector[1][2])
#         print("Object:", child_data.state_vector[1][3])
#     elif isinstance(child_data, State):
#         print("Additional state data:", child_data.state_vector)
# else:
#     print("No similar state vector found.")
