from pymed import PubMed
import json
import psycopg2

PUBMEDMAXRESULTS = 10



def SearchArticlesInPUBMED():
    connection = psycopg2.connect(
    user="postgres",
    password="F15strike*",
    host="127.0.0.1",
    port="5432",
    database="stf01"
    )
    
    
    
    cursor2 = connection.cursor()
    
    schema_name = 'sch01'
    cursor2.execute(f'SET search_path TO {schema_name}')
    
    print("SearchArticlesInPUBMED")
    # Create a PubMed object that GraphQL can use to query
    # Note that the parameters are not required but kindly requested by PubMed Central
    # https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
    pubmed = PubMed(tool="MyTool", email="juanbru27@gmail.com")
    query = "Prostate Cancer[Title]"
    # Execute the query against the API
    results = pubmed.query(query, max_results=PUBMEDMAXRESULTS)
    # Loop over the retrieved articles
    count =0
    for article in results:   
        json_string = article.toJSON()
        data = json.loads(json_string)
        try:
            insert_query = "INSERT INTO t01(pubmed_id, publication_date, title, abstract, keywords, journal, conclusions, methods, results, copyrights, doi ) VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s);" 
            s = data["pubmed_id"]
            s = s.split('\n', 1)[0]        
            try:
                record_to_insert = (
                    s, 
                    data["publication_date"], 
                    data["title"], 
                    data["abstract"], 
                    data["keywords"],
                    data["journal"],
                    data["conclusions"],
                    data["methods"],
                    data["results"],
                    data["copyrights"],
                    data["doi"]
                    #data["authors"]
                    )
                cursor2.execute(insert_query, record_to_insert)
                # Commit your changes
                connection.commit()
                # Get the number of rows affected
                # count = cursor.rowcount+1
                count = count+1
                #print(count, "Record inserted successfully into your_table table t01")            
            except:
                print ('E1')            
        except:
            print("E2")
    print(count, "Record inserted successfully into your_table table t01") 
    if connection:
        cursor2.close()
        connection.close()
        print("PostgreSQL connection is closed")
    
SearchArticlesInPUBMED()