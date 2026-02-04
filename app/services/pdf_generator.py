from fpdf import FPDF
import tempfile

class StudyGuidePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Study Mate - AI Study Guide', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        # Encode to latin-1 to avoid utf-8 issues with standard fpdf, usually better to use replacement chars
        # Or better: use a font that supports unicode. For simplicity, we'll try to handle basic text.
        try:
             self.multi_cell(0, 5, body)
        except:
             # Fallback cleanup for unsupported chars
             cleaned = body.encode('latin-1', 'replace').decode('latin-1')
             self.multi_cell(0, 5, cleaned)
        self.ln()

def generate_pdf(subject, topic, materials):
    pdf = StudyGuidePDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f"Subject: {subject}", 0, 1)
    pdf.set_font('Arial', 'I', 14)
    pdf.cell(0, 10, f"Topic: {topic}", 0, 1)
    pdf.ln(10)
    
    # Summary
    if materials.get('summary'):
        pdf.chapter_title("Summary")
        pdf.chapter_body(materials['summary'])
    
    # Key Terms
    if materials.get('hard_terms'):
        pdf.chapter_title("Key Terms")
        for term in materials['hard_terms']:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 5, f"- {term.get('term', '')}", 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 5, f"  {term.get('explanation', '')}")
            pdf.ln(2)
        pdf.ln(5)

    # Flashcards
    if materials.get('flashcards'):
        pdf.chapter_title("Flashcards (Q&A)")
        for i, card in enumerate(materials['flashcards'], 1):
            pdf.set_font('Arial', 'B', 11)
            pdf.multi_cell(0, 5, f"Q{i}: {card.get('question', '')}")
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 5, f"A: {card.get('answer', '')}")
            pdf.ln(3)

    # MCQs
    if materials.get('mcqs'):
        pdf.chapter_title("Multiple Choice Questions")
        for i, mcq in enumerate(materials['mcqs'], 1):
            pdf.set_font('Arial', 'B', 11)
            pdf.multi_cell(0, 5, f"{i}. {mcq.get('question', '')}")
            
            pdf.set_font('Arial', '', 10)
            for opt in mcq.get('options', []):
                 pdf.cell(0, 5, f"   {opt}", 0, 1)
            
            pdf.ln(1)
            pdf.set_font('Arial', 'I', 10)
            pdf.multi_cell(0, 5, f"   Answer: {mcq.get('correct_answer', '')}")
            pdf.ln(3)

    return pdf.output(dest='S').encode('latin-1', 'replace') # Return as bytes for streamlit download
