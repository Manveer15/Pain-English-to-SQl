import os
import sqlite3
import streamlit as st
from database import upload_to_sqlite
from dotenv import load_dotenv 

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Generate SQL query using LLM
def get_sql_query(user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
        You are an expert in converting English questions to SQL query!
        The SQL database has the name STUDENT and has the following columns - NAME, COURSE, SECTION and MARKS.
        For example:
        - How many entries of records are present? -> SELECT COUNT(*) FROM STUDENT;
        - Tell me all the students studying in Data Science COURSE? -> SELECT * FROM STUDENT WHERE COURSE="Data Science";
        Return only SQL without backticks or the word 'sql'.
        Now convert: {user_query}
    """)

    model = "llama3-8b-8192"
    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name=model
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    return chain.invoke({"user_query": user_query})

# Execute SQL query
def return_sql_response(sql_query, db_path="student.db"):
    with sqlite3.connect(db_path) as conn:
        return conn.execute(sql_query).fetchall()

# Streamlit UI
def main():
    st.set_page_config(page_title="Text To SQL")
    st.title("Talk to Your  Database")
    st.markdown("Convert natural language to SQL and upload CSV/Excel to update the database.")

    # Upload section
    st.sidebar.header("📁 Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        upload_to_sqlite(uploaded_file)

    st.divider()

    # SQL Chat section
    st.header(" Ask the Database")
    user_query = st.text_input("Enter your question:")
    if st.button("Submit"):
        try:
            sql_query = get_sql_query(user_query)
            results = return_sql_response(sql_query)

            st.subheader("🧾 Generated SQL:")
            st.code(sql_query, language="sql")

            st.subheader(" Query Results:")
            if results:
                st.dataframe(results)
            else:
                st.info("No results found.")
        except Exception as e:
            st.error(f"❌ Error running query: {e}")

if __name__ == '__main__':
    main()
