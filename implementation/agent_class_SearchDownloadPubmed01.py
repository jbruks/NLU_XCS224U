import psycopg2
from psycopg2.extras import RealDictCursor
from pymed import PubMed
import json
from messaging import Messaging
from agent_base_class import AgentBaseClass  # Make sure this provides initialization and basic attributes
from db_config import DB_CONFIG  # Import DB_CONFIG

class AgentSearchDownloadPubmed(AgentBaseClass):
    PUBMED_MAX_RESULTS = 7500

    def __init__(self, identifier, m):
        super().__init__(identifier, m)
        self.pubmed = PubMed(tool="MyTool", email="juanbru27@gmail.com")
        self.connection = None
        self.cursor = None
        self.setup_database()

    def setup_database(self):
        """Set up database connection and cursor."""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            schema_name = 'sch01'
            self.cursor.execute(f'SET search_path TO {schema_name}')
        except Exception as e:
            print(f"Failed to connect to database: {e}")

    def run(self, query):
        print(f"{self.identifier} running")
        self.setup_database()
        self.search_and_download_articles(query)
        self.close_database()

    def search_and_download_articles(self, query):
        results = self.pubmed.query(query, max_results=self.PUBMED_MAX_RESULTS)
        count = 0
        for article in results:
            try:
                json_string = article.toJSON()
                data = json.loads(json_string)
                insert_query = """INSERT INTO t01(pubmed_id, publication_date, title, abstract, keywords, 
                                  journal, conclusions, methods, results, copyrights, doi) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                record_to_insert = (
                    data["pubmed_id"].split('\n', 1)[0], 
                    data.get("publication_date", ""),
                    data.get("title", ""),
                    data.get("abstract", ""),
                    data.get("keywords", []),
                    data.get("journal", ""),
                    data.get("conclusions", ""),
                    data.get("methods", ""),
                    data.get("results", ""),
                    data.get("copyrights", ""),
                    data.get("doi", "")
                )
                self.cursor.execute(insert_query, record_to_insert)
                count += 1
            except Exception as e:
                print(f"Failed to process article due to: {e}")

        print(f"{count} records inserted successfully into articles table.")

    def close_database(self):
        """Close the cursor and the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    messaging_system = Messaging(DB_CONFIG)
    agent = AgentSearchDownloadPubmed("AgentSearchDownloadPubmed", messaging_system)
    # Example query string to run
    #query = '("prostatic neoplasms"[MeSH Terms] OR ("prostatic"[All Fields] AND "neoplasms"[All Fields]) OR "prostatic neoplasms"[All Fields] OR ("prostate"[All Fields] AND "cancer"[All Fields]) OR "prostate cancer"[All Fields]) AND ((ffrft[Filter]) AND (fha[Filter]) AND (2021/1/1:2021/12/30[pdat])) '
    #agent.run(query)
    
    
    base_query = '("prostatic neoplasms"[MeSH Terms] OR ("prostatic"[All Fields] AND "neoplasms"[All Fields]) OR "prostatic neoplasms"[All Fields] OR ("prostate"[All Fields] AND "cancer"[All Fields]) OR "prostate cancer"[All Fields]) AND ((ffrft[Filter]) AND (fha[Filter]) AND ({}/1/1:{}[pdat]))'

    # Loop through the desired years
    for year in range(2001, 2021):  # Adjust the range as needed for 20 years
        formatted_query = base_query.format(year, year)
        agent.run(formatted_query)
    
    
    
