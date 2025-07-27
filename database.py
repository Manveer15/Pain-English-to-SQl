import sqlite3
import pandas as pd
import streamlit as st

# Helper to infer SQLite column types from Pandas dtypes
def infer_sqlite_type(pd_type):
    if pd.api.types.is_integer_dtype(pd_type):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(pd_type):
        return "REAL"
    elif pd.api.types.is_bool_dtype(pd_type):
        return "BOOLEAN"
    else:
        return "TEXT"

# Main function to upload and insert into SQLite
def upload_to_sqlite(uploaded_file, db_path="student.db", table_name="STUDENT"):
    try:
        # Read file into DataFrame
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a .csv or .xlsx file.")
            return

        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Auto-create table with inferred schema
        column_definitions = ", ".join(
            f"{col} {infer_sqlite_type(dtype)}" for col, dtype in zip(df.columns, df.dtypes)
        )
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
        cursor.execute(create_table_sql)

        # Insert data
        placeholders = ", ".join("?" for _ in df.columns)
        insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders});"
        cursor.executemany(insert_sql, df.values.tolist())
        conn.commit()

        st.success(f"✅ Uploaded and inserted {len(df)} rows into `{table_name}` table.")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error while processing the file: {e}")
    finally:
        conn.close()
