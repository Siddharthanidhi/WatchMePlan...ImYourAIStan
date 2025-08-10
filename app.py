import streamlit as st
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from agent import agent_step

def generate_pdf_bytes(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    width, height = letter
    margin = 1 * inch
    max_width = width - 2 * margin
    text_object = c.beginText()
    
    text_object.setTextOrigin(margin, height - margin)
    text_object.setFont("Helvetica", 12)
    
    paragraphs = text.split('\n')
    lines = []
    for para in paragraphs:
        wrapped = simpleSplit(para, 'Helvetica', 12, max_width)
        lines.extend(wrapped)
        lines.append('')  # blank line between paragraphs
    
    for line in lines:
        if text_object.getY() < margin:
            c.drawText(text_object)
            c.showPage()
            text_object = c.beginText()
            text_object.setTextOrigin(margin, height - margin)
            text_object.setFont("Helvetica", 12)
        text_object.textLine(line)
    
    c.drawText(text_object)
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_pdf_download_link(text, filename="plan.pdf"):
    pdf_bytes = generate_pdf_bytes(text)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📥 Download Plan as PDF</a>'
    return href

st.set_page_config(page_title="Agentic Task Planner", layout="centered")
st.title("🧠 Agentic Task Planning Assistant")
st.write("Enter a real-world goal or task. The AI agent will break it down and plan step-by-step.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_area("What would you like to plan?", placeholder="e.g. Plan a Goa trip under ₹10,000")

if st.button("Generate Plan") and user_input:
    with st.spinner("Thinking..."):
        action, questions, plan = agent_step(user_input, st.session_state.conversation)

        if action == "clarify":
            st.session_state.conversation.append({"role": "assistant", "content": "\n".join(questions)})
            st.warning("I need some more info to plan better:")
            for q in questions:
                st.write(f"- {q}")

        elif action == "plan":
            st.success("Here's your plan:")
            st.markdown(plan)

            pdf_link = generate_pdf_download_link(plan)
            st.markdown(pdf_link, unsafe_allow_html=True)

            st.session_state.conversation.clear()

        # Add user input to conversation history
        st.session_state.conversation.append({"role": "user", "content": user_input})
