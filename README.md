# Pain-English-to-SQl
# 🧠 Text-to-SQL Chat with Database Upload (Streamlit + LLM)

This project lets you **talk to your SQLite database using natural language** and **upload CSV/Excel files** to automatically update the database — all via a beautiful **Streamlit UI** powered by **LangChain + Groq LLM (LLaMA3)**.

---

## ✨ Features

- 💬 Convert natural language questions into SQL queries using LLM
- 📁 Upload `.csv` or `.xlsx` files and auto-update your SQLite DB
- 🧠 Uses [LangChain](https://www.langchain.com/) and [Groq's LLaMA3](https://console.groq.com/)
- 🔍 Real-time SQL query execution and result display
- ⚡ Powered by Streamlit for interactive UI

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/manveer15/text-to-sql-streamlit.git
To run the Streamlit UI
cd text-to-sql-streamlit
2. Install Dependencies
pip install streamlit pandas openpyxl langchain langchain-groq
3. Set Up Environment Variable
You need a Groq API key.
export GROQ_API_KEY=your_groq_api_key

Create a .env file or set the environment variable in your shell:
