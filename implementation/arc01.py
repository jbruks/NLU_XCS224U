# agent_base_class.py
from openai import OpenAI
client = OpenAI(api_key='you Open AI api key')

def basicQuestionToOpenAI(p):
    #print('basicQuestionToOpenAI')
    response = client.chat.completions.create(
        #model="gpt-4-turbo",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": p}
            ]
        )
    return(response.choices[0].message.content)

class Agent:
    def __init__(self, name):
        self.name = name

    def process(self, data):
        # Placeholder for processing data
        # print(f"{self.name} processing data...")
        # return f"{self.name} output: {data}"
        return(data)
        
class InputAgent(Agent):
    def process(self, data):
        # Special agent to handle input
        return input("Please enter your input (or type 'quit' to exit): ")

class CompositionalGeneralizationAgent(Agent):
    def process(self, data):
        # Implement specific logic here
        # return super().process(f"Compositional Generalization applied on {data}")
        return super().process(data)

class FewShotLearningAgent(Agent):
    def process(self, data):
        # Implement specific logic here
        # return super().process(f"Few-shot learning adapted for {data}")
        return super().process(data)

class ChainOfThoughtAgent(Agent):
    def process(self, data):
        # Implement specific logic here
        #return super().process(f"Chain of Thought deduced for {data}")
        return super().process(data)

class ContextManagementAgent(Agent):
    def process(self, data):
        # Implement specific logic here
        #return super().process(f"Context managed for {data}")
        return super().process(data)

class Coordinator:
    def __init__(self, agents):
        self.agents = agents

    def handle_request(self, input_data):
        results = []
        for agent in self.agents:
            output = agent.process(input_data)
            if output.lower() == 'quit':
                return output
            results.append(output)
            input_data = output  # Feed the output of one agent as input to the next
        
        p=basicQuestionToOpenAI(input_data)
            
        return p
        #return results

# Initialize agents
agents = [
    InputAgent("InputAgent"),  # First agent handles input
    CompositionalGeneralizationAgent("CGA"),
    FewShotLearningAgent("FSLA"),
    ChainOfThoughtAgent("COTA"),
    ContextManagementAgent("CMA")
]

# Initialize Coordinator
coordinator = Coordinator(agents)

# Interactive loop
while True:
    results = coordinator.handle_request(None)
    if results == 'quit':
        print("Exiting...")
        break
    print(results)
    #for result in results:
    #    print(result)
