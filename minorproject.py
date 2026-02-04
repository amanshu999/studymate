import os
import warnings
import streamlit as st
from dotenv import load_dotenv

# Suppress warnings before importing streamlit
warnings.filterwarnings("ignore")
os.environ['STREAMLIT_RUNNING_IN_BARE_MODE'] = 'true'

# Load environment variables
load_dotenv()

from app.services.gemini import generate_study_material
from app.services.pdf_generator import generate_pdf

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
                    # Logic is now handled in the service with caching
                    st.session_state.materials = generate_study_material(subject, topic)
            else:
                st.warning("Please enter both subject and topic")
        
        st.markdown("---")
        st.markdown("### 🔧 Made by:")
        st.markdown("""
           Amanshu Sharma    
        """)
    
    # Display materials if available
    if st.session_state.materials:
        materials = st.session_state.materials
        
        # Header with Download Button
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.header("📝 Comprehensive Summary")
        with col2:
            pdf_bytes = generate_pdf(subject, topic, materials)
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"{subject}_{topic}_StudyGuide.pdf",
                mime="application/pdf"
            )

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