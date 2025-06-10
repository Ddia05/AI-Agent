from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv() #loads the env varibales in the python script 

@tool
def calculator(a: float, b: float)-> str:
    """useful for performing basic arithmetic calculations"""
    return f"The sum of {a} and {b} is {a+b}"


def main():
    #initialise the AI agent and chatbot 
    model = ChatOpenAI(temperature=0)   #the higher the temp - the more random the model is 
    tools = [calculator] 
    agent_executor = create_react_agent(model,tools)   #bringing in a prebuilt agent 

    print("Hello! I'm your AI assistant, you can press 'quit' to exit")
    print("You can ask me to perform calculations or just chat with me")

    while True: 
        user_input = input("\nYou: ").strip()

        if user_input=="quit":
            break 

        print("\nAssistant: ",end="")
        for chunk in agent_executor.stream(
            {"messages":[HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content,end="")
        
        print()

if __name__=="__main__":
    main()

