import streamlit as st
import requests
import dotenv 
import os

dotenv.load_dotenv()

API_URL = "http://localhost:8081"
 
st.set_page_config(page_title="Medical Chatbot", page_icon="💬", layout="wide")

st.title("🩺 MedicalBot - Your AI Medical Assistant")
st.markdown("Ask anything about **medicines, diagnostics, and symptoms!** 🤖")

query = st.text_input("Enter your question:", placeholder="e.g., What are the side effects of Paracetamol?")

if st.button("Ask"):
    if query.strip():
        with st.spinner("Fetching response..."):
            response = requests.post(f"{API_URL}/ask", json={"query": query})
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer found.").get("answer")

                st.markdown("### ✅ Answer")
                st.write(answer)
            else:
                st.error("❌ Failed to fetch response. Try again!")
    else:
        st.warning("⚠️ Please enter a question.")
