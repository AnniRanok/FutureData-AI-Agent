#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from scipy.stats import zscore
import os

# --- Налаштування сторінки ---
st.set_page_config(page_title="Future Data Agent", layout="wide")
st.title("💬 Future Data – Conversational Finance Assistant")

# --- Стан ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "history" not in st.session_state:
    st.session_state.history = []
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

def log_activity(msg):
    st.session_state.activity_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# --- Чат блок ---
st.subheader("🧠 Ask the AI Agent")
for msg in st.session_state.chat_history:
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**Agent:** {msg['agent']}")
    st.markdown(f"""
        <script>
            var u = new SpeechSynthesisUtterance("{msg['agent'].replace('"', '')}");
            u.lang = 'en-US';
            speechSynthesis.speak(u);
        </script>
    """, unsafe_allow_html=True)

chat_input = st.text_input("💬 Type your question to the agent")
if chat_input:
    prompt = f"You are an AI finance assistant. Answer concisely and insightfully.\n\nQuestion: {chat_input}\nAnswer:"
    res = requests.post("http://localhost:11434/api/generate", json={"model": "mixtral", "prompt": prompt, "stream": False})
    reply = res.json().get("response", "...").strip()
    st.session_state.chat_history.append({"user": chat_input, "agent": reply})
    st.experimental_rerun()

# --- Завантаження файлу ---
st.sidebar.header("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose CSV or Excel", type=["csv", "xlsx"])
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    st.success(f"Loaded `{uploaded_file.name}` with shape {df.shape}")
    st.dataframe(df.head(), use_container_width=True)
    log_activity(f"File loaded: {uploaded_file.name}")

    # --- Запит ---
    user_query = st.text_input("🔎 Ask a question about your data")
    if user_query:
        column_list = ", ".join(df.columns)
        system_prompt = (
            f"You are a Python assistant. You will receive a DataFrame with columns: {column_list}. "
            "Return valid Python code using 'df'."
        )
        resp = requests.post("http://localhost:11434/api/generate", json={
            "model": "mixtral",
            "prompt": system_prompt + f"\n\nUser question: {user_query}", "stream": False
        })
        code = resp.json().get("response", "").strip()
        st.code(code, language="python")
        log_activity("Code generated")

        local_vars = {"df": df}
        exec(code, {}, local_vars)
        result = local_vars.get("result")

        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        elif isinstance(result, (int, float, str)):
            st.write("📈 Result:", result)
        elif plt.get_fignums():
            st.pyplot(plt.gcf())
            plt.clf()

        # --- Summary ---
        summary_prompt = f"Summarize this result in 1–2 sentences:\nQuestion: {user_query}\nCode: {code}\nResult: {str(result)}"
        summary = requests.post("http://localhost:11434/api/generate", json={
            "model": "mixtral", "prompt": summary_prompt, "stream": False
        }).json().get("response", "")
        st.success(f"🧠 Summary: {summary}")
        log_activity("Summary created")

        # --- KPI ---
        st.subheader("📊 KPI Scanner")
        kpi_cols = [col for col in df.columns if any(k in col.lower() for k in ['revenue','loss','profit','amount','score','pd'])]
        for col in kpi_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                st.markdown(f"**{col}** – Mean: `{df[col].mean():.2f}`")
                st.bar_chart(df[col])
                log_activity(f"KPI chart: {col}")

        # --- Аномалії ---
        st.subheader("🚨 Anomaly Detector")
        anomalies = []
        for col in df.select_dtypes(include=['float64', 'int64']).columns:
            try:
                z = zscore(df[col].dropna())
                if any(abs(z) > 3):
                    outliers = df[(abs(zscore(df[col])) > 3)]
                    st.warning(f"Anomalies in `{col}`")
                    st.dataframe(outliers)
                    anomalies.append(col)
                    log_activity(f"Anomaly in {col}")
            except:
                continue

        # --- TODO.md ---
        st.subheader("📌 Suggested Actions")
        todos = []
        for col in anomalies:
            todos.append(f"- Investigate anomaly in column **{col}**")
        for col in kpi_cols:
            if df[col].mean() < 0:
                todos.append(f"- Check negative values in KPI **{col}**")
        if user_query:
            todos.append(f"- Follow up on: **{user_query}**")
        todo_md = "# TODO\n\n" + "\n".join(todos)
        st.code(todo_md, language="markdown")
        with open("/mnt/data/todo.md", "w") as f:
            f.write(todo_md)
        st.download_button("⬇️ Download TODO.md", data=todo_md, file_name="todo.md")

# --- Agent log ---
if st.session_state.activity_log:
    st.sidebar.subheader("🎬 Agent Log")
    for log in reversed(st.session_state.activity_log):
        st.sidebar.markdown(log)

# --- Стилізація ---
st.markdown("""
<style>
    .stButton>button { background-color: #2C3E50; color: white; border-radius: 6px; }
    .stDownloadButton>button { background-color: #27AE60; color: white; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

