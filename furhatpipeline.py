from furhat_remote_api import FurhatRemoteAPI
import time
from basic_langchain_setup import pipeline
import furhatpipeline


def initialize_robot(furhat):
    # Startup message
    furhat.say(text="Hello! I am your dungeon assistant. I'm here to help you with your D&D game.")
    furhat.say(text="I can create scenarios, guide you through adventures, and assist you as a dungeon master.")
    furhat.say(text="I'm looking forward to assisting you with your game.")
    furhat.gesture(name="Smile")


def process_user_input(o):
    # Placeholder logic for processing user input

    return "You decided to explore further into the forest."


def get_user_rating(graph):
    # Placeholder logic for getting user rating (replace with actual implementation)
    print("Could you rate the previous response by typing one of the following values :")
    print("1 (very bad) 2(bad) 3(good) 4(very good)")
    furhat.say(text="Could you rate the previous response by typing one of the following values: 1 (very bad) 2(bad) 3(good) 4(very good)")
    value = -1
    while value not in ["1", "2", "3", "4"]:
        value = input("rating: ")
        if value not in ["1", "2", "3", "4"]:
            print("Invalid input!")

    graph.update_weight(context_vector, state, int(value))
    return 8


def listen_with_timeout(furhat, timeout_sec):
    start_time = time.time()
    user_input = ""

    # Okay so the furhat automatic voice thing feeels like it kinda sucks.
    user_input = furhat.listen()

    return user_input

# User opens app:
# User is greeted by furhat, furhat presents scenario and asks what action the user wants to take X
# User responds

# We take user response as plain text, ask chatgpt to retrieve context vector
# Look for most similar context vector in the graph, if exist, then return that story, else create new story
# With the new story create a response by chatGPT

# Tell furhat to read out the response
# LOOP

# after 5 responses by furhat ENDLOOP

def main_scenario_loop(furhat):
    story = "You find yourself in a mysterious forest. The trees are tall, and the air is filled with enchantment. You are a brave adventurer seeking treasures and facing challenges."
    print(story)
    furhat.say(text=story)
    flag = False
    game = True
    count = 0
    while game:
        # User input using furhat.listen()
        furhat.say(text="What action will you take?")
        user_input = furhat.listen()
        # print(user_input)

        # Process user input and generate a response
        context_vector, next_state, new_story, loaded_graph, full_story = pipeline("", story)

        # Display the result to the user
        furhat.say(text=new_story)
        # # Ask the user to rate the result
        # furhat.say(text="On a scale of 0 to 10, how would you rate this outcome?")
        # # user_rating = get_user_rating(context_vector, next_state, loaded_graph)
        # user_rating = 1
        # time.sleep(10)

        if count == 3:
            game = False
        count += 1
        story = full_story
        # Sleep to provide time for user interaction (you can adjust the duration)
        time.sleep(5)


if __name__ == "__main__":
    # Create a FurhatRemoteAPI object
    furhat = FurhatRemoteAPI("localhost")
    furhat.set_voice(name='Joanna')
    try:
        # Initialize the robot
        initialize_robot(furhat)

        time.sleep(2)

        # Start the main scenario loop
        main_scenario_loop(furhat)

    finally:
        # Close the connection when done
        print("done")
