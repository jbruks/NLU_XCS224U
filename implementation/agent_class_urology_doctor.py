# EJECUTAR DESDE EL DIRECTORIO CODE

from messaging import Messaging
from agent_base_class import AgentBaseClass
from db_config import DB_CONFIG
import time
        
PROFILE = "Urology Doctor"

ACTIONS =               "1	Diagnose and Treat.	Manage diseases of the urinary tract and reproductive organs."
ACTIONS = ACTIONS +     "2	Perform Surgeries	Conduct surgical procedures related to urology."
ACTIONS = ACTIONS +     "3	Prescribe Treatment	Develop treatment plans for patients."
ACTIONS = ACTIONS +     "4	Consultations	Provide specialist advice to other healthcare professionals."
ACTIONS = ACTIONS +     "5	Research and Development	Engage in research to advance urological medicine."
ACTIONS = ACTIONS +     "6	Patient Follow up	Communicate with Patient to check how things are going"

#AGENTS = "Urologist Service Manager, Urologist Doctor, Nurse, Radiologist, Patient"
AGENTS = "AgentUrologyPatient"

        
class AgentUrologyDoctor(AgentBaseClass):
    def run(self): 
        print("run")
        while True:
            print("AgentUrologyDoctor")
            # Read message for A
            message_for_me = self.messaging_system.read_message('AgentUrologyDoctor')
            if message_for_me is not None:
                # Assess what to do with A and prepare an answer for B
                context =           "My Name is: " + PROFILE
                context = context + "The actions that I can do are: " + ACTIONS
                context = context + "Other agents that I can interact are: " + AGENTS
                p= " Taking into account the next CONTEXT: " + context + ", then:  Prepare an answer for the following question: " + message_for_me['content'] + '. '
                p = p + "Please format the answer as: 'The Name of other Agent destiny of my message or action| Answer the recived question, and request of a new task if proceeds' where this information is based in the previously context provided."
                r=AgentBaseClass.basicQuestionToOpenAI(p)           
                parts       = r.split('|', 1)
                receiver    = parts[0]
                taskaction  = parts[1]
                self.messaging_system.send_message('AgentUrologyDoctor', receiver, taskaction)                            
            time.sleep(5)  # Delay for 5 seconds

if __name__ == "__main__":
    messaging_system = Messaging(DB_CONFIG)
    agentUD1 = AgentUrologyDoctor("AgentUrologyDoctor", messaging_system)
    agentUD1.run()
    
