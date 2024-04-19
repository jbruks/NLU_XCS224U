# LLMs HIGH LEVEL ARCHITECTURE

from openai import OpenAI
client = OpenAI(api_key='you Open AI api key')

def QuestionToOpenAI(p):
    #print('basicQuestionToOpenAI')
    response = client.chat.completions.create(
        #model="gpt-4-turbo",
        model="gpt-3.5-turbo",
        messages=[ {"role": "user", "content": p}            ]        )
    return(response.choices[0].message.content)

class Agent:
    def __init__(self, name):
        self.name = name

    def process(self, data):
        try:
            r=QuestionToOpenAI(data)
            return r
        except Exception as e:
            return f"Error processing API call: {str(e)}"

class ContextualPrimingAgent(Agent):
    def process(self, data):
        r = super().process("Please improve the following question adding Contextual Priming, QUESTION: " + data)
        # print("ContextualPriming: " + r + "\n")
        return r
        
class ExplicitInstructionsAgent(Agent):
    def process(self, data):
        r = super().process("Please extend (but not remove anything) the following question adding Explict Instructions, QUESTION: " + data)
        # print("ExplicitInstructionsAgent: " + r + "\n")
        #return super().process(f"Chain of Thought applied on {data}")
        return r
        
class TokensAgent(Agent):
    def process(self, data):
        r = super().process("Please extend (but not remove anything) the following question adding appropiate Tokens, QUESTION: " + data)
        # print("TokensAgent: " + r + "\n")
        #return super().process(f"Tokens applied on {data}")
        return r
        
class WhatNotToDoAgent(Agent):
    def process(self, data):
        r = super().process("Please extend (but not remove anything) the following question addins instructions on What not To Answer, QUESTION: " + data)
        # print("WhatNotToDoAgent: " + r + "\n")
        #return super().process(f"What not to do applied on {data}")
        return r
      
class FewShotLearningAgent(Agent):
    def process(self, data):
        r = super().process("Please extend (but not remove anything) the following question adding one Few Short Learning example, QUESTION: " + data)
        # print("FewShotLearningAgent: " + r + "\n")
        #return super().process(f"Few-shot learning adapted for {data}")
        return r

class ChainOfThoughtAgent(Agent):
    def process(self, data):
        r = super().process("Please extend (but not remove anything) the following question by applying Chain of Thought, QUESTION: " + data)
        # print("ChainOfThoughtAgent: " + r + "\n")
        #return super().process(f"Chain of Thought applied on {data}")
        return r
        
class FormatAnswerAgent(Agent):
    def process(self, data):
        r = super().process("Please extend (but not remove anything) the following question by indicating the answer format you consider appropiate, QUESTION: " + data)
        # print("FormatAnswerAgent: " + r + "\n")
        #return super().process(f"Format Answer applied on {data}")
        return r
        
class RetrievalAugmentedGenerationAgent(Agent):
    def process(self, data):
        #r = super().process("Please complete (but not remove anything) the following question QUESTION: " + data)
        # print("RAG not enabled \n")
        #return super().process(f"REtrieval Augmented Generation on {data}")
        return (data)

class LanguageModelAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
    
    #def process(self, data):
    #    return super().process(data)
    
    def process(self, data):
        try:
            # First we arrenge the question
            r = QuestionToOpenAI("Please organize the text of following question, but keeping all details, QUESTION: " + data)
            #print ("**************************************************************************\n")
            #print ("LLM AGENT: FINAL QUESTION: \n")
            #print (r + "\n")
            #print ("**************************************************************************\n")
            r=QuestionToOpenAI(r)
            return r
        except Exception as e:
            return f"Error processing API call: {str(e)}"

class InterfaceAgent(Agent):
    def __init__(self, name, coordinator):
        super().__init__(name)
        self.coordinator = coordinator
    def run(self):
        while True:
            input_data = input("Please enter your input. This Models is specialized in complex questions (type 'quit' to exit): ")
            if input_data.lower() == 'quit':
                print("Exiting...")
                break
            r = self.coordinator.handle_request(input_data)
            print (r)          
        #input_data = "I need information on NVidia cards for LLM processing"
        #print(input_data + "\n")        
        #r = self.coordinator.handle_request(input_data)
        
class LoopForTestingAgent(Agent):
    def __init__(self, name, coordinator):
        super().__init__(name)
        self.coordinator = coordinator
    def run(self):
        pass:
       
            
class Coordinator:
    def __init__(self, agents):
        self.agents = agents
            
    def handle_request(self, input_data):    
        #print ("COORDINATOR AGENT. INITIALL QUESTION:\n" + input_data + "\n")    
        #Question Processing and improving
        r=input_data
        r = r + "\n" + self.agents[0].process(input_data)
        r = r + "\n" + self.agents[1].process(input_data)
        r = r + "\n" + self.agents[2].process(input_data)
        r = r + "\n" + self.agents[3].process(input_data)
        r = r + "\n" + self.agents[4].process(input_data)
        r = r + "\n" + self.agents[5].process(input_data)
        r = r + "\n" + self.agents[6].process(input_data)        
        #print ("**************************************************************************\n")
        #print ("COORDINATOR AGENT. FINAL FULL ADDED QUESTIONS:\n" + r + "\n")
        #print ("**************************************************************************\n")        
        #Final question sent to LLM
        r=self.agents[8].process(r)        
        #print ("**************************************************************************\n")
        #print ("COORDINATOR AGENT. FINAL ANSWER:\n" + r + "\n")
        #print ("**************************************************************************\n")        
        return r        

def main():    
    # Initialize Auxiliar LLM Techiques agents
    contextual_priming_agent    = ContextualPrimingAgent("ContextPriming")                      #0          
    explicit_instructions_gent  = ExplicitInstructionsAgent("ExplicitInstructions")             #1
    tokens_agent                = TokensAgent("Tokens")                                         #2
    not_to_do_agent             = WhatNotToDoAgent("NotToDo")                                   #3
    few_shot_learn_agent        = FewShotLearningAgent("FSL")                                   #4
    chain_of_thought_agent      = ChainOfThoughtAgent("CoT")                                    #5
    format_answer_agent         = FormatAnswerAgent("FormatAnswer")                             #6
    rag_agent                   = RetrievalAugmentedGenerationAgent("RAG")                      #7         
    # LLM Final Question execution Agent
    language_model_agent = LanguageModelAgent("OpenAI API Agent")                               #8
    # Coordinator setup
    coordinator = Coordinator([
        contextual_priming_agent, 
        explicit_instructions_gent, 
        tokens_agent, 
        not_to_do_agent, 
        few_shot_learn_agent, 
        chain_of_thought_agent, 
        format_answer_agent, 
        rag_agent, 
        language_model_agent
        ])              
               
    # Initialize Interface Agent
    interface_agent = InterfaceAgent("User Interface", coordinator)                             #10
    
    # Initializa loop for test Agent
    loop_for_test = LoopForTestingAgent(Agent):"Loop for Test", coordinator)                    #11
        
    # Run the interface
    interface_agent.run()

if __name__ == "__main__":
    main()
