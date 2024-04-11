import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts import HumanMessagePromptTemplate
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache

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
   return nlp_results