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
FSL_EXAMPLES_PER_ABSTRACT = 1

class AgentGenerateFSLExamples(AgentBaseClass):
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

    def run(self, number_of_fsl_examples):
        print(f"{self.identifier} running")
        self.setup_database()
        cursor = self.fetch_abstract()
        rows = cursor.fetchall() 
        for row in rows:
            abstract = row['abstract']
            pubmed_id = row['pubmed_id']
            print(f"Processing abstract ID {pubmed_id}")
            results = []
            for _ in range(number_of_fsl_examples):
                result = self.generate_fsl_example(abstract)
                results.append(result)
                print(f"Generated FSL example {_ + 1} for abstract ID {pubmed_id}")
            for result in results:
                self.save_result(result, pubmed_id)
        cursor.close()  # Always ensure the cursor is closed after processing is complete    
        print("Completed processing all abstracts.")
        self.close_database()


    def fetch_abstract(self):
        fetch_query = "SELECT pubmed_id, abstract FROM t01 WHERE set_train_test = 'train' ;" #LIMIT 5;"
        self.cursor.execute(fetch_query)
        return self.cursor        

    def generate_fsl_example(self, abstract):
        """Generate FSL examples using OpenAI's GPT-4 API."""
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "user", "content": "Generate ONE Few Shot Learning Question and Answer based in following abstract. Please provide the result in a format 'Text of the question|Text of the answer'. ABSTRACT: " + abstract}
                    ]
                )
            
            return(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating FSL example: {e}")
            return None

    def save_result(self, result, pubmed_id):
        """Save the generated result into the FSL_results table."""
        if result:
            parts=result.split('|', 1)
            # Accessing the parts
            question = parts[0]
            answer = parts[1] if len(parts) > 1 else None          
            # insert_query = "INSERT INTO FSL_results (pubmed_id, result) VALUES (%s, %s);"
            insert_query = "INSERT INTO sch01.fsl_question_answer_examples(pubmed_id, fsl_question, fsl_answer)	VALUES (%s, %s, %s);"
            self.cursor.execute(insert_query, (pubmed_id, question, answer))
            print(f"Result saved successfully for abstract ID {pubmed_id} in FSL_results table.")

    def close_database(self):
        """Close the cursor and the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    messaging_system = Messaging(DB_CONFIG)
    agent = AgentGenerateFSLExamples("AgentGenerateFSLExamples", messaging_system)
    agent.run(FSL_EXAMPLES_PER_ABSTRACT)
