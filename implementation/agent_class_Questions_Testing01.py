import psycopg2
from psycopg2.extras import RealDictCursor
import json
from openai import OpenAI
from openai import ChatCompletion
from agent_base_class import AgentBaseClass
from db_config import DB_CONFIG
from messaging import Messaging

from config import OPENAI_API_KEY  # Import the API key from config

client = OpenAI(api_key=OPENAI_API_KEY)
QUESTIONS_TO_TEST = 1

FSL_EXAMPLES =                  "Question: What is sipuleucel-T, and why is its FDA approval significant for cancer therapy?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: Sipuleucel-T, also known as Provenge, is the first therapeutic cancer vaccine approved by the FDA. Its significance lies in introducing a new class of treatment that enhances patient survival with minimal side effects by activating a targeted immune response against cancer."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What is the incremental annual budget impact of adopting enzalutamide for chemotherapy-naïve mCRPC patients in a population of 115?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: The annual budget impact is $510,641."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What are the next steps suggested to enhance the clinical benefits of newly FDA-approved immunotherapy agents for metastatic prostate cancer and melanoma?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: The suggested next steps include developing immune-monitoring techniques, establishing clinical endpoint assessment guidelines, and exploring combination therapies to enhance benefits."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What treatment categories show promise in advanced prostate cancer, and which practice yields the best outcomes?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: Promising treatments include bone-building therapies, hormonal treatments, and immunotherapies. The best outcomes are achieved through sequential use of these therapies."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What are the primary and secondary outcomes of early taxane-based chemohormonal therapy added to ADT in treating newly diagnosed, metastatic, hormone-sensitive prostate cancer?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: The primary outcome shows that early taxane-based chemohormonal therapy likely reduces mortality when added to ADT, with a possible increase in severe side effects. Secondary outcomes suggest reduced risks of prostate cancer-specific death and progression."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: Which immune checkpoint inhibitor shows promise for prostate cancer therapy, and what is its current testing phase?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: Ipilimumab shows promise and is currently in phase III trials for prostate cancer."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What was the primary clinical outcome demonstrated by sipuleucel-T in the integrated analysis of trials D9901 and D9902A among advanced prostate cancer patients?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: The primary outcome was a 33% reduction in the risk of death."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What is the significance of the FDA approval of sipuleucel-T in the context of cancer treatment?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: The FDA approval is significant as it marks the first antigen-specific immunotherapy approved for cancer, representing a breakthrough in prostate cancer immunotherapy."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What was the primary endpoint of the phase 3 trial assessing the efficacy of sipuleucel-T in metastatic castration-resistant prostate cancer patients, and how was it analyzed?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: The primary endpoint was overall survival, analyzed using a stratified Cox regression model adjusted for baseline PSA and lactate dehydrogenase levels."
FSL_EXAMPLES = FSL_EXAMPLES +   "Question: What are the two licensed cancer-preventive vaccines mentioned, and which types of cancer do they target?"
FSL_EXAMPLES = FSL_EXAMPLES +   "Answer: The vaccines are anti-HBV, targeting hepatitis B virus-related hepatocellular carcinoma, and anti-HPV, targeting HPV-related cervical carcinoma."


class AgentQuestionsTesting(AgentBaseClass):
    def __init__(self, identifier, m):
        super().__init__(identifier, m)
        self.connection = None
        self.cursor = None
        self.openai_api_key = OPENAI_API_KEY  # Securely manage this key.
        self.setup_database()

    def setup_database(self):
        """Set up database connection and cursor."""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            schema_name = 'sch01'
            self.cursor.execute(f'SET search_path TO {schema_name}')
        except Exception as e:
            print(f"Failed to connect to database: {e}")

    def run(self, number_of_questions):
        print(f"{self.identifier} running")
        self.setup_database()
        cursor = self.fetch_abstract()
        rows = cursor.fetchall() 
        for row in rows:
            abstract = row['abstract']
            pubmed_id = row['pubmed_id']
            simple_question = row['simple_question']
            complex_question = row['complex_question']
            complex_question_cot = row['complex_question_cot']
            print(f"Processing abstract ID {pubmed_id}")
            results = []            
            result = self.test_simple_question(abstract, simple_question)
            result_fsl = self.test_simple_question_fsl(abstract, simple_question)            
            result_complex = self.test_complex_question(abstract, complex_question)
            result_complex_cot = self.test_complex_question_cot(abstract, complex_question_cot)            
            #results.append(result)
            print(f"Generated Answers for abstract ID {pubmed_id}")            
            self.save_answers(result, result_fsl, result_complex, result_complex_cot, pubmed_id)            
        cursor.close()  # Always ensure the cursor is closed after processing is complete    
        print("Completed processing all abstracts.")
        self.close_database()

    def fetch_abstract(self):
        fetch_query = "SELECT pubmed_id, title, abstract, simple_question, complex_question, complex_question_cot, set_train_test FROM sch01.v01"
        self.cursor.execute(fetch_query)
        return self.cursor        

    def test_simple_question(self, abstract, question):
        """Generate symple questionOpenAI's GPT-4 API."""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "user", "content": "Make the following question to the provided abstract. Provide as result EXCLUSIVELY the answer to the question. QUESTION: " + question + "; ABSTRACT: " + abstract}
                    ]
                )            
            return(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating simple question: {e}")
            return None
            
    def test_simple_question_fsl(self, abstract, question):
        """Generate symple questionOpenAI's GPT-4 API."""
        try:
            content = "I am giving you a set of question/answer examples. Please take into account this set of examples for the following work."
            content = "SET OF EXAMPLES: " + FSL_EXAMPLES 
            content = content + ". Now I will give you a QUESTION and and ABSTRACT. Execute the question on the abstracct Take into account previous set of examples. Provide as result EXCLUSIVELY the answer to the question. QUESTION: "
            content = content + question + "; ABSTRACT: " + abstract
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "user", "content": content}
                    ]
                )            
            return(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating simple question: {e}")
            return None
    
    def test_complex_question(self, abstract, question):
        """Generate symple questionOpenAI's GPT-4 API."""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "user", "content": "Make the following question to the provided abstract. Provide as result EXCLUSIVELY the answer to the question. QUESTION: " + question + "; ABSTRACT: " + abstract}
                    ]
                )            
            return(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating simple question: {e}")
            return None

    def test_complex_question_cot(self, abstract, question):
        """Generate symple questionOpenAI's GPT-4 API."""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "user", "content": "Make the following question to the provided abstract appplying CoT Reassoning. Provide as result EXCLUSIVELY the answer to the question. QUESTION: " + question + "; ABSTRACT: " + abstract}
                    ]
                )            
            return(response.choices[0].message.content)   
            
        except Exception as e:
            print(f"Error generating simple question: {e}")
            return None
      
    def save_answers(self, result, result_fsl, result_complex , result_complex_cot, pubmed_id):
        """Save the generated result into the FSL_results table."""
        if result:
            insert_query = "INSERT INTO sch01.answers(pubmed_id, simple_answer, simple_answer_fsl, complex_answer, complex_answer_cot)	VALUES (%s, %s, %s, %s, %s);"
            self.cursor.execute(insert_query, (pubmed_id, result, result_fsl, result_complex , result_complex_cot))
            print(f"Result saved successfully for abstract ID {pubmed_id} in Answers table.")

    def close_database(self):
        """Close the cursor and the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    messaging_system = Messaging(DB_CONFIG)
    agent = AgentQuestionsTesting("AgentQuestionsTesting", messaging_system)
    agent.run(QUESTIONS_TO_TEST)
