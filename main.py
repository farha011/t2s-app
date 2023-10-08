#Author Farha
#Last updated: Oct 8 2023

import streamlit as st
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from langchain.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("openaikey")
print(openai_api_key)
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name='gpt-3.5-turbo')

# Database connection parameters
azure_server = os.getenv("azure_server")
azure_database = os.getenv("azure_database")
azure_username = os.getenv("azure_username")
azure_password = os.getenv("azure_password")

# Schemas
schema1 = os.getenv("schema1")
schema2 = os.getenv("schema2")

# Create a SQLAlchemy engine for Azure SQL Server with multiple schemas
db_uri = f"mssql+pyodbc://{azure_username}:{azure_password}@{azure_server}/{azure_database}?driver=ODBC+Driver+17+for+SQL+Server&schema={schema1},{schema2}"
engine = create_engine(db_uri)
print(db_uri)

# Initialize SQLDatabase instance
db = SQLDatabase(engine)

# Initialize SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Streamlit UI
def main():
    st.title("Ask query to Database")

    user_input = st.text_area("Please write your query here:")

    if st.button("Click for Response"):
        sql_query = db_chain.run(user_input)
        st.write("Results:", sql_query)

if __name__ == '__main__':
    main()
