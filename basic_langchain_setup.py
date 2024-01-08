from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import json

from memory.graph import ContextVector

local_path = './models/gpt4all-falcon-q4_0.gguf' 
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

def chatGPTContextVector():
    template = """
    Instruction: {instruction}

    Answer: 
    
    The user will give a text describing their action in a Dungeons and Dragons game.

    From this text I want you to give me a single ContextVector which is described as follows: Environment, PlayerCharacter, Characterstate, Action, Object.
    
    Please extract the environment from this. The environment can be one of these options only: Forest, City, Village, Camp.

    From the following please extract the character's state. The character state can either be "no hitpoints" or "alive".

    From the following also extract a character's action. The action can be "Death saving throw", "Dead", "Fighting", "Walking", "Resting" or "Interacting".

    From the following also extract an object the character is performing the action on. Define the character that is performing the action as "PlayerCharacter" and the object as "Object".

    Return this as a JSON object. With the keys being: Environment, PlayerCharacter, Characterstate, Action, Object.

    """

    prompt = PromptTemplate(template=template, input_variables=["instruction"])
    llm = GPT4All(model=local_path, callback_manager=callback_manager, verbose=False)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

    instruction = input("Enter your prompt: ")

    response = llm_chain.invoke(instruction)

    return response["text"]

def convertToJSON(json_string):
    # Convert JSON string to JSON object (dictionary in Python)
    json_object = json.loads(json_string)

    return json_object

def pipeline():
    json_string = chatGPTContextVector()

    json_object = convertToJSON(json_string)

    context_vector = ContextVector(json_object["Environment"], json_object["PlayerCharacter"], json_object["Characterstate"], json_object["Action"], json_object["Object"])
    
    print(context_vector)

pipeline()
