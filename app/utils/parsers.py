import json
import re
import streamlit as st

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
        if len(response_text) > 500:
             st.error(f"Raw response start: {response_text[:500]}...")
        else:
             st.error(f"Raw response: {response_text}")
        
        # Fallback: return empty structure
        return {
            "summary": "Unable to parse response. The AI might have returned content in the wrong format. Please try again.",
            "flashcards": [],
            "mcqs": [],
            "hard_terms": [],
            "example_problems": []
        }
