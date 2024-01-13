
def ask_for_feedback(context_vector, state, graph):
    print("Could you rate the previous response by typing one of the following values :")
    print("1 (very bad) 2(bad) 3(good) 4(very good)")
    value = -1
    while value not in ["1", "2", "3", "4"]:
        value = input("rating: ")
        if value not in ["1", "2", "3", "4"]:
            print("Invalid input!")

    graph.update_weight(context_vector, state, int(value))
