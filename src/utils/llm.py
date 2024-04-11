import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts import HumanMessagePromptTemplate
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
from timeit import default_timer as timer
import glob
import json

set_llm_cache(SQLiteCache(database_path=".langchain.db"))
load_dotenv()

# Load the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# Enable tracing for LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY


# Function to call the OpenAI API
def process_gpt(file_prompt, system_msg):
   llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key= OPENAI_API_KEY)
   chat_template = ChatPromptTemplate.from_messages(
        [   SystemMessage(content=system_msg),
            HumanMessage(content=file_prompt),
        ])
   chain = chat_template | llm
   nlp_results =  chain.invoke({})
   return nlp_results.content


# Function to take folder of files and a prompt template, and return a json-object of all the entities and relationships
def extract_entities_relationships(folder, prompt_template):
    start = timer()
    files = glob.glob(f"./data/{folder}/*")
    system_msg = "You are a helpful IT-project and account management expert who extracts information from documents."
    print(f"Running pipeline for {len(files)} files in {folder} folder")
    results = []
    for i, file in enumerate(files):
        print(f"Extracting entities and relationships for {file}")
        try:
            with open(file, "r") as f:
                text = f.read().rstrip()
                prompt = PromptTemplate.from_template(prompt_template).invoke({"ctext":text}).to_string()
                result = process_gpt(prompt, system_msg=system_msg)
                results.append(json.loads(result))
        except Exception as e:
            print(f"Error processing {file}: {e}")
    end = timer()
    print(f"Pipeline completed in {end-start} seconds")
    return results