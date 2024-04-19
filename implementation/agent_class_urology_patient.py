# EJECUTAR DESDE EL DIRECTORIO CODE

from messaging import Messaging
from agent_base_class import AgentBaseClass
from db_config import DB_CONFIG
import time
        
PROFILE = "Urology Patient"

ACTIONS =               "1	Request Appointment.	Adhere to the treatments and medication schedules prescribed."
ACTIONS = ACTIONS +     "2	Attend Appointments.	Regularly visit the healthcare provider for follow-ups."
ACTIONS = ACTIONS +     "3	Provide Feedback.	Communicate effectiveness of treatment and any side effects."
ACTIONS = ACTIONS +     "4	Follow Treatment Plans.	Adhere to the treatments and medication schedules prescribed."
ACTIONS = ACTIONS +     "5	Self-Care.	Engage in recommended lifestyle and dietary changes."
ACTIONS = ACTIONS +     "6	Education.	Learn about their condition and treatment options."
ACTIONS = ACTIONS +     "7	Compliance with Guidelines.	Follow instructions for tests and treatments."

#AGENTS = "Urologist Service Manager, Urologist Doctor, Nurse, Radiologist, Patient"
AGENTS = "AgentUrologyDoctor"

ENVIRONMENT = 0

#--Short Term Memory for conversations. In-memeory
#--Long Term Memory for tasks or important items to be remembered. In-Database
#--Satisfaction: Cuts conversation

# Automatic Wake Up. Take action by default

       
class AgentUrologyPatient(AgentBaseClass):
    def run(self): 
        print("run")
        while True:
            print("AgentUrologyPatient")
            # Read message for A
            message_for_me = self.messaging_system.read_message('AgentUrologyPatient')
            if message_for_me is not None:
                # Assess what to do with A and prepare an answer for B
                context =           "My Name is: " + PROFILE
                context = context + "The actions that I can do are: " + ACTIONS
                context = context + "Other agents that i can interact are: " + AGENTS
                p= " Taking into account the CONTEXT: " + context + ", then:  Prepare an answer for the following question: " + message_for_me['content'] + '. '
                p = p + "Please format the answer as: 'The Name of other Agent destiny of my message or action| Answer the recived question, and request of a new task if proceeds' where this information is based in the previously context provided."
                r=AgentBaseClass.basicQuestionToOpenAI(p)           
                parts       = r.split('|', 1)
                receiver    = parts[0]
                taskaction  = parts[1]
                self.messaging_system.send_message('AgentUrologyPatient', receiver, taskaction)                            
            
            time.sleep(5)  # Delay for 5 seconds

if __name__ == "__main__":
    messaging_system = Messaging(DB_CONFIG)
    messaging_system.send_message('AgentUrologyPatient', 'AgentUrologyDoctor', 'Hello, I need and a visit with an Urology Doctor. ')        
    agentUP1 = AgentUrologyPatient("AgentUrologyPatient", messaging_system)
    agentUP1.run()

    
