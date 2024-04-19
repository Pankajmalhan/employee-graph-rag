import streamlit as st
from streamlit_chat import message
from timeit import default_timer as timer
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from src.prompts import cypher_generation_template, CYPHER_QA_TEMPLATE
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
import dotenv
import os

dotenv.load_dotenv()

#Neo4j configuration
neo4j_url = os.getenv("NEO4J_CONNECTION_URL")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key= OPENAI_API_KEY)

cypher_prompt = PromptTemplate(
    template = cypher_generation_template,
    input_variables = ["schema", "question"]
)

qa_prompt = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)

def query_graph(user_input):
    graph = Neo4jGraph(url=neo4j_url, username=neo4j_user, password=neo4j_password)
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt
        )
    result = chain(user_input)
    return result



# st.set_page_config(layout="wide")

# if "user_msgs" not in st.session_state:
#     st.session_state.user_msgs = []
# if "system_msgs" not in st.session_state:
#     st.session_state.system_msgs = []

# title_col, empty_col, img_col = st.columns([2, 1, 2])    

# with title_col:
#     st.title("Conversational Neo4J Assistant")
# with img_col:
#     st.image("https://dist.neo4j.com/wp-content/uploads/20210423062553/neo4j-social-share-21.png", width=200)

# user_input = st.text_input("Enter your question", key="input")
# cypher_query = None
# database_results = None
# if user_input:
#     with st.spinner("Processing your question..."):
#         st.session_state.user_msgs.append(user_input)
#         start = timer()

#         try:
#             result = query_graph(user_input)
            
#             intermediate_steps = result["intermediate_steps"]
#             cypher_query = intermediate_steps[0]["query"]
#             database_results = intermediate_steps[1]["context"]

#             answer = result["result"]
#             st.session_state.system_msgs.append(answer)
#         except Exception as e:
#             st.write("Failed to process question. Please try again.")
#             print(e)

#     st.write(f"Time taken: {timer() - start:.2f}s")

#     col1, col2, col3 = st.columns([1, 1, 1])

#     # Display the chat history
#     with col1:
#         if st.session_state["system_msgs"]:
#             for i in range(len(st.session_state["system_msgs"]) - 1, -1, -1):
#                 message(st.session_state["system_msgs"][i], key = str(i) + "_assistant")
#                 message(st.session_state["user_msgs"][i], is_user=True, key=str(i) + "_user")

#     with col2:
#         if cypher_query:
#             st.text_area("Last Cypher Query", cypher_query, key="_cypher", height=240)
        
#     with col3:
#         if database_results:
#             st.text_area("Last Database Results", database_results, key="_database", height=240)
    

question = input("Question\n")
result = query_graph(question)

intermediate_steps = result["intermediate_steps"]
cypher_query = intermediate_steps[0]["query"]
database_results = intermediate_steps[1]["context"]

answer = result["result"]
print(answer)