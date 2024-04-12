from dotenv import load_dotenv
from src.utils.llm import process_gpt, extract_entities_relationships
from src.prompts import people_prompt_template, project_prompt_template, slack_prompt_template
import os

# Final function to bring all the steps together
def ingestion_pipeline(folders):
    # Extrating the entites and relationships from each folder, append into one json_object
    entities_relationships = []
    for key, value in folders.items():
        entities_relationships.extend(extract_entities_relationships(key, value))
    with open("entities.txt", "w") as f:
       f.write(f"{entities_relationships}")

    # Generate and execute cypher statements
   #  cypher_statements = generate_cypher(entities_relationships)
   #  for i, stmt in enumerate(cypher_statements):
   #      print(f"Executing cypher statement {i+1} of {len(cypher_statements)}")
   #      try:
   #          gds.execute_query(stmt)
   #      except Exception as e:
   #          with open("failed_statements.txt", "w") as f:
   #              f.write(f"{stmt} - Exception: {e}\n")


def main():
   folders = {
    "people_profiles": people_prompt_template,
   #  "project_briefs": project_prompt_template,
   #  "slack_messages": slack_prompt_template,
   }

   ingestion_pipeline(folders)
   
if __name__ == "__main__":
   # Load environment variables
    load_dotenv()
    main()