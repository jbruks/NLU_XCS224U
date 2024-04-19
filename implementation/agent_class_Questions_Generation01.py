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
QUESTIONS_PER_ABSTRACT = 1

class AgentGenerateQuestionGeneration(AgentBaseClass):
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
            print(f"Processing abstract ID {pubmed_id}")
            
            
            simple_question = self.generate_simple_question(abstract)
            complex_question, complex_question_cot = self.generate_complex_question(abstract)
             
            
            self.save_question(simple_question, complex_question, complex_question_cot, pubmed_id)
            
            print(f"Generated Questions for abstract ID {pubmed_id}")
        cursor.close()  # Always ensure the cursor is closed after processing is complete    
        print("Completed processing all abstracts.")
        self.close_database()


    def fetch_abstract(self):
        fetch_query = "SELECT pubmed_id, abstract FROM t01 WHERE set_train_test ='test';"
        self.cursor.execute(fetch_query)
        return self.cursor        

    def generate_simple_question(self, abstract):
        """Generate symple questionOpenAI's GPT-4 API."""
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "user", "content": "Generate an Question for the following abstract. Please provide the result in a format 'Text of the question'. ABSTRACT: " + abstract}
                    ]
                )
            
            return(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating simple question: {e}")
            return None
    
    def generate_complex_question(self, abstract):
        """Generate FSL examples using OpenAI's GPT-4 API."""
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "user", "content": "Generate an COMPLEX Question for the following abstract. Please provide the result in a format 'Text of the question'. ABSTRACT: " + abstract}
                    ]
                )
                
            complex_question_cot = " Please answer the following question applying Chain Of Thought reassoning. " +  response.choices[0].message.content   
            
            return(response.choices[0].message.content, complex_question_cot)
            
        except Exception as e:
            print(f"Error generating complex question: {e}")
            return None
    
    
            
            return(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating complex question: {e}")
            return None

    def save_question(self, simple_question, complex_question, complex_question_cot, pubmed_id):
        """Save the generated result into the FSL_results table."""
        #if result:
                      
        # insert_query = "INSERT INTO sch01.questions (pubmed_id, simple_question) VALUES (%s, %s);"
        insert_query = "INSERT INTO sch01.questions(pubmed_id, simple_question, complex_question, complex_question_cot)	VALUES (%s, %s, %s, %s);"
        self.cursor.execute(insert_query, (pubmed_id, simple_question, complex_question, complex_question_cot))
        print(f"Result saved successfully for abstract ID {pubmed_id} in Questions table.")

    def close_database(self):
        """Close the cursor and the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    messaging_system = Messaging(DB_CONFIG)
    agent = AgentGenerateQuestionGeneration("AgentGenerateFSLExamples", messaging_system)
    agent.run(QUESTIONS_PER_ABSTRACT)
