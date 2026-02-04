import os
import google.generativeai as genai
import streamlit as st
from app.utils.parsers import parse_response

def configure_gemini():
    """Configure Gemini with the correct model"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        st.error("🔑 Please set GEMINI_API_KEY in your .env file")
        st.info("Create a .env file in your project folder with:")
        st.code("GEMINI_API_KEY=your_actual_api_key_here")
        return None
    
    genai.configure(api_key=api_key)
    
    # Use the latest available models
    model_names = [
        'gemini-2.0-flash',
        'gemini-1.5-flash',
        'gemini-pro',
    ]
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Simple connection test
            # We skip the "Say TEST OK" call to save latency, trusting the configuration works
            # if the object creation succeeded.
            return model
        except Exception:
            continue
    
    st.error("❌ No compatible Gemini model found.")
    return None

@st.cache_data(show_spinner=False)
def generate_study_material(subject, topic):
    """Generate comprehensive study materials using Gemini with caching"""
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
