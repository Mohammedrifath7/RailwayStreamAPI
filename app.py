import os
import re
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

# Streamlit page config
st.set_page_config(
    page_title="Railway Complaint Classifier",
    page_icon="🚆",
    layout="centered"
)

# Custom CSS for Netflix-style Dark Theme UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Main background - Netflix dark */
    .stApp {
        background-color: #141414;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }
    
    /* Header styling - Netflix style */
    h1 {
        color: #E50914 !important;
        font-weight: 800 !important;
        text-align: center;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 8px rgba(229, 9, 20, 0.3);
    }
    
    /* Caption/subtitle */
    .stCaption {
        text-align: center;
        color: #b3b3b3 !important;
        font-size: 1.05rem !important;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background-color: #2a2a2a;
    }
    
    /* Text area container - Dark card */
    .stTextArea {
        background-color: #1f1f1f;
        padding: 1.8rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        border: 1px solid #2a2a2a;
    }
    
    /* Text area label - White text */
    .stTextArea label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.8rem;
        letter-spacing: 0.3px;
    }
    
    /* Text area input - White text on dark background */
    .stTextArea textarea {
        background-color: #2a2a2a !important;
        border: 1.5px solid #404040 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #E50914 !important;
        box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.2) !important;
        outline: none !important;
        background-color: #333333 !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #808080 !important;
    }
    
    /* Button styling - Netflix red */
    .stButton button {
        background-color: #E50914 !important;
        color: white !important;
        border: none !important;
        padding: 0.85rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stButton button:hover {
        background-color: #f40612 !important;
        box-shadow: 0 6px 16px rgba(229, 9, 20, 0.6) !important;
        transform: translateY(-2px);
    }
    
    .stButton button:active {
        transform: translateY(0px);
    }
    
    /* Alert boxes - Dark theme versions */
    .stAlert {
        border-radius: 8px !important;
        border-left: 4px solid !important;
        padding: 1.2rem !important;
        margin: 1.2rem 0 !important;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Success message - Dark green */
    .stSuccess {
        background-color: #1a3a1a !important;
        border-left-color: #4ade80 !important;
        color: #86efac !important;
    }
    
    /* Info message - Dark blue */
    .stInfo {
        background-color: #1a2a3a !important;
        border-left-color: #60a5fa !important;
        color: #93c5fd !important;
    }
    
    /* Error/Complaint message - Dark red */
    .stError {
        background-color: #3a1a1a !important;
        border-left-color: #f87171 !important;
        color: #fca5a5 !important;
    }
    
    /* Warning message - Dark yellow */
    .stWarning {
        background-color: #3a2a1a !important;
        border-left-color: #fbbf24 !important;
        color: #fcd34d !important;
    }
    
    /* Subheader - White text */
    h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1.2rem !important;
        font-size: 1.4rem !important;
        letter-spacing: -0.3px;
    }
    
    /* Department list items - Dark cards */
    .stMarkdown p {
        background-color: #1f1f1f;
        padding: 1rem 1.3rem;
        border-radius: 8px;
        margin: 0.6rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        color: #ffffff;
        font-weight: 500;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #E50914 !important;
        transition: all 0.2s ease;
    }
    
    .stMarkdown p:hover {
        background-color: #252525;
        transform: translateX(5px);
    }
    
    /* Spinner - Netflix red */
    .stSpinner > div {
        border-top-color: #E50914 !important;
    }
    
    /* Code block for errors - Dark */
    .stCodeBlock {
        background-color: #0a0a0a !important;
        border-radius: 6px !important;
        padding: 1rem !important;
        border: 1px solid #2a2a2a !important;
    }
    
    .stCodeBlock code {
        color: #ff6b6b !important;
    }
    
    /* Footer text */
    .footer {
        text-align: center;
        color: #808080;
        margin-top: 3.5rem;
        font-size: 0.9rem;
        padding-top: 2rem;
        border-top: 1px solid #2a2a2a;
    }
    
    /* Scrollbar styling - Dark theme */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #141414;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #E50914;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚆 Railway Complaint Classification System")
st.caption("Multilingual | CT / NCT | Multi-Label Department Detection")

st.divider()

# Input
user_input = st.text_area(
    "Enter your railway issue (any Indian language):",
    height=140,
    placeholder="Eg: ट्रेन 2 घंटे लेट है और AC काम नहीं कर रहा"
)

# Departments
DEPARTMENTS = [
    "Train Delay",
    "Electrical",
    "Water",
    "Amenities",
    "Housekeeping",
    "Coach",
    "Ticket / Refund",
    "Security",
    "Medical",
    "Catering / Food"
]

# Prompt
def build_prompt(text):
    return f"""
You are an Indian Railway complaint classification system.

TASKS:
1. Decide if the input is a railway complaint (CT) or not (NCT).
2. If CT, classify all relevant departments.

Allowed departments:
{", ".join(DEPARTMENTS)}

IMPORTANT RULES:
- Understand ALL Indian languages.
- Choose departments ONLY from the list.
- Respond with ONLY valid JSON.
- Do NOT add explanations or extra text.

JSON FORMAT:
{{
  "type": "CT or NCT",
  "departments": []
}}

INPUT:
{text}
"""

# JSON extractor (SAFE)
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        raise ValueError("No JSON found in model output")

# Button
if st.button("Classify Complaint 🚦", use_container_width=True):
    if not user_input.strip():
        st.warning("Please enter a problem.")
    else:
        with st.spinner("Analyzing complaint..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": build_prompt(user_input)}
                    ],
                    temperature=0
                )

                raw_output = response.choices[0].message.content.strip()

                result = extract_json(raw_output)

                st.success("Analysis Completed")

                # Output
                if result["type"] == "NCT":
                    st.info("🟢 This is **NOT a complaint (NCT)**")
                else:
                    st.error("🔴 This is a **COMPLAINT (CT)**")

                    if result["departments"]:
                        st.subheader("📌 Related Departments:")
                        for dept in result["departments"]:
                            st.write(f"✅ {dept}")
                    else:
                        st.warning("No department identified.")

            except Exception as e:
                st.error("LLM response could not be processed.")
                st.code(str(e))

# Footer
st.markdown("""
<div class="footer">
    Powered by AI • Indian Railways Complaint Management
</div>
""", unsafe_allow_html=True)
