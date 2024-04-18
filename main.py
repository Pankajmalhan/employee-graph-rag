from dotenv import load_dotenv
from src.utils.llm import process_gpt, extract_entities_relationships
from src.prompts import people_prompt_template, project_prompt_template, slack_prompt_template
from src.utils.cypher import generate_cypher
import json
import os
from neo4j import GraphDatabase

def run_cypher(cypher_statements):
   # Generate and execute cypher statements

   # Neo4j configuration & constraints
   neo4j_url = os.getenv("NEO4J_CONNECTION_URL")
   neo4j_user = os.getenv("NEO4J_USER")
   neo4j_password = os.getenv("NEO4J_PASSWORD")
   gds = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))
   
   for i, stmt in enumerate(cypher_statements.split("\n")):
      print(f"Executing cypher statement {i+1} of {len(cypher_statements)}/: Statement: {stmt}")
      try:
         gds.execute_query(stmt)
      except Exception as e:
         with open("failed_statements.txt", "w") as f:
               f.write(f"{stmt} - Exception: {e}\n")

# Final function to bring all the steps together
def ingestion_pipeline(folders):
    # Extrating the entites and relationships from each folder, append into one json_object
    entities_relationships = []
    for key, value in folders.items():
        entities_relationships.extend(extract_entities_relationships(key, value))
    with open("entities.txt", "w") as f:
       f.write(json.dumps(entities_relationships))
    



def main():
   # folders = {
   #  "people_profiles": people_prompt_template,
   #  "project_briefs": project_prompt_template,
   #  "slack_messages": slack_prompt_template,
   # }

   # # ingestion_pipeline(folders)
   # entities_relationships={}
   # with open("entities.txt", "r") as f:
   #    entities_relationships = json.loads(f.read())
   # print(type(entities_relationships))
   # generate_cypher(entities_relationships)

   cypher_queries=[]
   with open("cyphers.txt", "r") as f:
      cypher_queries = f.read()

   run_cypher(cypher_queries)
   
   
if __name__ == "__main__":
   # Load environment variables
    load_dotenv()
    main()