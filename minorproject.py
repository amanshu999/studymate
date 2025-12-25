import os
import warnings
import json
import re

# Suppress warnings before importing streamlit
warnings.filterwarnings("ignore")
os.environ['STREAMLIT_RUNNING_IN_BARE_MODE'] = 'true'

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configure_gemini():
    """Configure Gemini with the correct model"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        st.error("🔑 Please set GEMINI_API_KEY in your .env file")
        st.info("Create a .env file in your project folder with:")
        st.code("GEMINI_API_KEY=your_actual_api_key_here")
        return None
    
    genai.configure(api_key=api_key)
    
    # Use the latest available models from your test
    model_names = [
        'gemini-2.0-flash',
        'gemini-2.0-flash-001',
        'gemini-pro-latest',
        'gemini-2.5-flash',
    ]
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model with a simple prompt
            response = model.generate_content("Say 'TEST OK'")
            st.sidebar.success(f"✅ Using model: {model_name}")
            return model
        except Exception as e:
            continue
    st.error("❌ No compatible Gemini model found.")
    return None

def generate_study_material(subject, topic):
    """Generate comprehensive study materials using Gemini"""
    model = configure_gemini()
    if model is None:
        return None
    
    prompt = f"""
    Create comprehensive study materials for:
    SUBJECT: {subject}
    TOPIC: {topic}
    
    Return the response in EXACTLY this JSON format:
    {{
        "summary": "Detailed summary of the topic (4-6 paragraphs covering all important aspects)",
        "flashcards": [
            {{"question": "question1", "answer": "detailed answer1"}},
            {{"question": "question2", "answer": "detailed answer2"}},
            {{"question": "question3", "answer": "detailed answer3"}},
            {{"question": "question4", "answer": "detailed answer4"}},
            {{"question": "question5", "answer": "detailed answer5"}},
            {{"question": "question6", "answer": "detailed answer6"}},
            {{"question": "question7", "answer": "detailed answer7"}},
            {{"question": "question8", "answer": "detailed answer8"}},
            {{"question": "question9", "answer": "detailed answer9"}},
            {{"question": "question10", "answer": "detailed answer10"}},
            {{"question": "question11", "answer": "detailed answer11"}},
            {{"question": "question12", "answer": "detailed answer12"}},
            {{"question": "question13", "answer": "detailed answer13"}},
            {{"question": "question14", "answer": "detailed answer14"}},
            {{"question": "question15", "answer": "detailed answer15"}}
        ],
        "mcqs": [
            {{
                "question": "question1",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "A) option1",
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question2",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "B) option2", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question3",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "C) option3", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question4",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "D) option4", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question5",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "A) option1", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question6",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "B) option2", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question7",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "C) option3", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question8",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "D) option4", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question9",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "A) option1", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question10",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "B) option2", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question11",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "C) option3", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }},
            {{
                "question": "question12",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct_answer": "D) option4", 
                "explanation": "Detailed explanation of why this is correct and others are wrong"
            }}
        ],
        "hard_terms": [
            {{"term": "term1", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term2", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term3", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term4", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term5", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term6", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term7", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term8", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term9", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term10", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term11", "explanation": "comprehensive explanation with examples"}},
            {{"term": "term12", "explanation": "comprehensive explanation with examples"}}
        ],
        "example_problems": [
            {{
                "problem": "detailed problem statement 1",
                "solution": "comprehensive step-by-step solution",
                "explanation": "detailed explanation of why this approach works and key concepts"
            }},
            {{
                "problem": "detailed problem statement 2", 
                "solution": "comprehensive step-by-step solution",
                "explanation": "detailed explanation of why this approach works and key concepts"
            }},
            {{
                "problem": "detailed problem statement 3",
                "solution": "comprehensive step-by-step solution",
                "explanation": "detailed explanation of why this approach works and key concepts"
            }}
        ]
    }}
    
    IMPORTANT REQUIREMENTS:
    - Generate AT LEAST 12 MCQs (multiple choice questions)
    - Generate AT LEAST 15 flashcards
    - Generate AT LEAST 12 hard terms with explanations
    - Generate AT LEAST 3 example problems
    - Make all content comprehensive, detailed, and educational
    - Ensure MCQs cover different aspects of the topic
    - Provide detailed explanations for MCQ answers
    - Make flashcards cover fundamental concepts
    - Ensure hard terms include key terminology from the topic
    - Make example problems practical and illustrative
    
    Provide accurate and educational content suitable for students.
    Make the content engaging and informative.
    """
    
    try:
        response = model.generate_content(prompt)
        return parse_response(response.text)
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

def parse_response(response_text):
    """Parse the Gemini response and extract structured data"""
    try:
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks if present
        cleaned_text = re.sub(r'```json\s*', '', cleaned_text)
        cleaned_text = re.sub(r'```\s*', '', cleaned_text)
        
        # Parse JSON
        data = json.loads(cleaned_text)
        return data
    except json.JSONDecodeError as e:
        st.error(f"Error parsing response: {str(e)}")
        st.error(f"Raw response: {response_text[:500]}...")
        # Fallback: return empty structure
        return {
            "summary": "Unable to parse response. The AI might have returned content in the wrong format. Please try again.",
            "flashcards": [],
            "mcqs": [],
            "hard_terms": [],
            "example_problems": []
        }

def main():
    st.set_page_config(
        page_title="Study Mate", 
        page_icon="📚", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📚 Study Mate - Your AI Study Companion")
    st.markdown("### Get comprehensive study materials for any subject and topic!")
    
    # Initialize session state
    if 'materials' not in st.session_state:
        st.session_state.materials = None
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📖 Study Input")
        subject = st.text_input("Subject (e.g., Physics, History, Python):", placeholder="Mathematics")
        topic = st.text_input("Topic (e.g., Calculus, French Revolution, OOP):", placeholder="Linear Algebra")
        
        if st.button("Generate Study Materials", type="primary", use_container_width=True):
            if subject and topic:
                with st.spinner("🧠 Generating comprehensive study materials... This may take a moment."):
                    st.session_state.materials = generate_study_material(subject, topic)
            else:
                st.warning("Please enter both subject and topic")
        
        st.markdown("---")
        st.markdown("### 🔧 Project Credits:")
        st.markdown("""
        1. Amanshu Sharma    
        2. Saksham Malhotra
        3. Paramjeet          
        4. Gurmeet             
        5. Pavneet       
        6. Vikas Angural 
        """)
    
    # Display materials if available
    if st.session_state.materials:
        materials = st.session_state.materials
        
        # Summary Section
        st.header("📝 Comprehensive Summary")
        st.write(materials.get('summary', 'No summary available'))
        
       
        
        # Create tabs for different study materials
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Flashcards", "❓ MCQs", "🔤 Key Terms", "📊 Examples"])
        
        # Flashcards Tab
        with tab1:
            st.subheader(f"Flashcards ({len(materials.get('flashcards', []))} cards)")
            flashcards = materials.get('flashcards', [])
            if flashcards:
                # Display flashcards in a grid
                cols = st.columns(2)
                for i, card in enumerate(flashcards):
                    with cols[i % 2]:
                        with st.expander(f"📄 Card {i+1}: {card.get('question', '')}", expanded=False):
                            st.success(f"**Answer:** {card.get('answer', '')}")
            else:
                st.info("No flashcards generated. Try again with a different topic.")
        
        # MCQs Tab
        with tab2:
            st.subheader(f"Multiple Choice Questions ({len(materials.get('mcqs', []))} questions)")
            mcqs = materials.get('mcqs', [])
            if mcqs:
                for i, mcq in enumerate(mcqs):
                    with st.container():
                        st.write(f"**{i+1}. {mcq.get('question', '')}**")
                        
                        # Display options
                        options = mcq.get('options', [])
                        for option in options:
                            st.write(f"   {option}")
                        
                        with st.expander("Show Answer & Detailed Explanation", expanded=False):
                            st.success(f"**Correct Answer:** {mcq.get('correct_answer', '')}")
                            st.info(f"**Explanation:** {mcq.get('explanation', '')}")
                        st.markdown("---")
            else:
                st.info("No MCQs generated. Try again with a different topic.")
        
        # Hard Terms Tab
        with tab3:
            st.subheader(f"Key Terms Explained ({len(materials.get('hard_terms', []))} terms)")
            terms = materials.get('hard_terms', [])
            if terms:
                # Display terms in a 2-column layout
                cols = st.columns(2)
                for i, term in enumerate(terms):
                    with cols[i % 2]:
                        with st.container():
                            st.markdown(f"### 🔍 {term.get('term', '')}")
                            st.write(term.get('explanation', ''))
                            st.markdown("---")
            else:
                st.info("No key terms generated. Try again with a different topic.")
        
        # Example Problems Tab
        with tab4:
            st.subheader(f"Example Problems ({len(materials.get('example_problems', []))} examples)")
            examples = materials.get('example_problems', [])
            if examples:
                for i, example in enumerate(examples):
                    with st.expander(f"Example {i+1}: Problem Statement", expanded=False):
                        st.write(f"**Problem:** {example.get('problem', '')}")
                        st.write(f"**Solution:**")
                        st.code(example.get('solution', ''), language='text')
                        st.write(f"**Explanation:** {example.get('explanation', '')}")
            else:
                st.info("No example problems generated. Try again with a different topic.")
    
    else:
        # Welcome message when no materials are generated
        st.markdown("""
        ## 🎯 Welcome to Study Mate!
        
        **How to use:**
        1. **Enter your subject** in the sidebar
        2. **Enter the specific topic** you want to study  
        3. **Click "Generate Study Materials"**
        4. **Explore** the generated content in different tabs
        
        ### 📚 You'll get:
        - **Comprehensive summary** (4-6 paragraphs)
        - **15+ flashcards** for quick review
        - **12+ MCQs** with detailed explanations  
        - **12+ key terms** with comprehensive explanations
        - **3+ example problems** with step-by-step solutions
        
        ### 💡 Example Inputs:
        - **Subject:** Physics | **Topic:** Newton's Laws
        - **Subject:** History | **Topic:** Roman Empire  
        - **Subject:** Programming | **Topic:** Functions
        - **Subject:** Biology | **Topic:** DNA Replication
        """)

if __name__ == "__main__":
    main()