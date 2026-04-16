import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# --- API KEY SETUP ---
# Pehle code se check karega, fir Streamlit secrets se
API_KEY = "AQ.Ab8RN6IwqAqM9Q-m6QXpji0EiQi9_EXIZCrvyLeP7HC4ee-4KQ" 

if not API_KEY or "AQ" not in API_KEY:
    API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Cleardeals Automation", layout="wide")
st.title("🏠 Cleardeals Property Data Extractor")

raw_text = st.text_area("WhatsApp Message Paste Karein:", height=300)

if st.button("Generate CSV"):
    if not raw_text:
        st.warning("Pehle data paste karein!")
    elif not API_KEY:
        st.error("API Key nahi mil rahi! Secrets mein check karein.")
    else:
        with st.spinner("AI processing kar raha hai..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Extract property data from this text into a CSV table. Columns: Date, Category, Property Code, Owner Name, Owner Contact, BHK, Area, Locality, Project Name, Floor, Furnishing (Strictly: Furnished, Semi-Furnished, Unfurnished), Price, Deposit, Source. If data is missing, use 'N/A'. Text: {raw_text}"
                response = model.generate_content(prompt)
                csv_data = response.text.replace('```csv', '').replace('```', '').strip()
                st.success("Data ready hai!")
                st.download_button(label="📥 Download CSV File", data=csv_data, file_name="properties.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Error: {e}")
