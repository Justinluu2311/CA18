from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import json

from memory.graph import ContextVector, Graph, Node, State
from memory.feedback import ask_for_feedback

local_path = './models/gpt4all-falcon-q4_0.gguf'
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

def chatGPTContextVector(rawInput, textInput):
    template = """
    Instruction: {instruction}

    Answer: 
    
    The user will give a text describing their action in a Dungeons and Dragons game.

    From this text I want you to give me a single ContextVector which is described as follows: Environment, PlayerCharacter, Characterstate, Action, Object.
    
    Please extract the environment from this.

    From the following please extract the character's state. The character state can either be "no hitpoints" or "alive".

    From the following also extract a character's current action. The action can ONLY be "Death saving throw", "Dead", "Fighting", "Walking", "Resting" or "Interacting". Make sure to categorize it into one of these six actions. The death saving throw is only used when the character has less than 0 hp"

    From the following also extract an object the character is performing the action on. Define the character that is performing the action as "PlayerCharacter" and the object as "Object".

    Return this as a JSON object. With the keys being: Environment, PlayerCharacter, Characterstate, Action, Object.
    Return only 1 JSON object.
    """

    prompt = PromptTemplate(template=template, input_variables=["instruction"])
    llm = GPT4All(model=local_path, callback_manager=callback_manager, verbose=False)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

    if textInput:
        instruction = input("Enter your action: ")
    else:
        instruction = rawInput

    response = llm_chain.invoke(instruction)

    return response["text"]

#turn memory=False if the model is not supposed to use memory.
def chatGPTState(vector, story, state, memory=True):
    template = """
    Instruction: 
    {request}
    Tell a short event within 3 sentences in third person based on the attributes in the given context vector 
    and as a narrator in third person, make sure the story meaningfully progresses
    and ask the listener what they would do in such a situation.

    """

    prompt = PromptTemplate(template=template, input_variables=["instruction"])
    llm = GPT4All(model=local_path, callback_manager=callback_manager, verbose=False)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    request = """The context vector is {}, this is what happened before: {}.
    """.format(vector, story)

    if not memory:
        request = ""
    response = llm_chain.invoke(request)

    return response["text"]

def convertToJSON(json_string):
    # Convert JSON string to JSON object (dictionary in Python)
    json_object = json.loads(json_string)

    return json_object

def pipeline(currentStory, rawInput, textInput=True):
    loaded_graph = Graph()
    loaded_graph.load_from_file("graph.txt")
    json_string = chatGPTContextVector(rawInput, textInput)
    
    json_object = convertToJSON(json_string)

    context_vector = ContextVector(json_object["Environment"], json_object["PlayerCharacter"], json_object["Characterstate"], json_object["Action"], json_object["Object"])
    
    most_similar_vector = loaded_graph.find_similar_state_vector(context_vector)
    next_state = None
    new_story = None
    if most_similar_vector is not None:
        if len(most_similar_vector.children) > 0:
            next_state = loaded_graph.get_next_state(most_similar_vector)
            # when it returns next state we generate a story from this state.
            new_story = chatGPTState(most_similar_vector.data, currentStory, next_state)
        else:
            # when the next_state is None then it should generate a completely new story based on the context vector
            # Convert this story into a state so we can store it.
            # Connect this state to the context vector and save it in the graph.
            new_story = chatGPTState(most_similar_vector.data, currentStory, None)
            next_state = State(most_similar_vector.data.state_vector[0], "")
            next_state_node = Node(next_state, 1, most_similar_vector)
            most_similar_vector.children.append(next_state_node)
            loaded_graph.add_node(next_state_node)
    else:
        # when the next_state is None then it should generate a completely new story based on the context vector
        # Convert this story into a state so we can store it.
        # Connect this state to the context vector and save it in the graph.
        new_node = Node(context_vector)
        new_story = chatGPTState(context_vector, currentStory, None)
        next_state = State(context_vector.state_vector[0], "")
        next_state_node = Node(next_state, 1, new_node)
        new_node.children.append(next_state_node)
        loaded_graph.add_node(new_node)
        loaded_graph.add_node(next_state_node)

    loaded_graph.save_to_file("graph.txt")

    full_story = new_story
    return context_vector, next_state, new_story, loaded_graph, full_story

# pipeline("You find yourself in a mysterious forest. The trees are tall, and the air is filled with enchantment. You are a brave adventurer seeking treasures and facing challenges.", "")