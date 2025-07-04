import streamlit as st
import helper
import pickle
from PIL import Image

# Load model
model = pickle.load(open('model.pkl','rb'))

# Configure page
st.set_page_config(
    page_title="Duplicate Question Detector",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: #333333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .header {
        color: #2c3e50;
    }
    .result {
        font-size: 24px;
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
        text-align: center;
    }
    .duplicate {
        background-color: #d4edda;
        color: #155724;
    }
    .not-duplicate {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True)

# Header section
col1, col2 = st.columns([1, 3])
with col1:
    st.image("IMAGE.png", width=100)
with col2:
    st.title("Duplicate Question Detector")
    st.markdown("🔍 Check if two questions are duplicates or not")

# Main content
with st.form("question_form"):
    st.subheader("Enter Two Questions")
    
    col1, col2 = st.columns(2)
    with col1:
        q1 = st.text_area("Question 1", height=150, 
                         placeholder="Type your first question here...")
    with col2:
        q2 = st.text_area("Question 2", height=150,
                         placeholder="Type your second question here...")
    
    submitted = st.form_submit_button("Check for Duplicates", type="primary")

    if submitted:
        if q1.strip() and q2.strip():
            with st.spinner("Analyzing questions..."):
                query = helper.query_point_creator(q1, q2)
                result = model.predict(query)[0]
                
                # Display result with animation
                st.balloons()
                if result:
                    st.markdown(
                        f'<div class="result duplicate">'
                        f'<h3>These questions are duplicates!</h3>'
                        f'<p>The system detected that these questions have the same meaning.</p>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="result not-duplicate">'
                        f'<h3>These questions are not duplicates</h3>'
                        f'<p>The system detected that these questions have different meanings.</p>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                
                # Show examples if you want
                st.markdown("---")
                st.subheader("Examples of Duplicate Questions")
                st.markdown("- 'How to learn Python?' ↔ 'What's the best way to learn Python?'")
                st.markdown("- 'Best laptop for coding?' ↔ 'Which laptop is good for programming?'")
                
        else:
            st.warning("Please enter both questions to check for duplicates")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 20px;">
        <p>Duplicate Question Detection System • Powered by NLP and Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
