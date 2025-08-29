import streamlit as st
from modules.auditor_service import service, service_3_time, service_feedback
from modules.auditor_polish import polish

st.title("Service Dimension")

before_after, num_gaps = service()

# --- Output Section: Generate the summary text ---

gaps_feedback, gap_score = service_3_time(num_gaps)

service_feedback_text= service_feedback(before_after, gaps_feedback, gap_score)

# Add a separator at the end for a cleaner look
st.markdown("---")
st.subheader("Service Feedback")

st.markdown(service_feedback_text)
st.code(service_feedback_text)

st.markdown("---")
st.title("Polish Dimension")

polish_feedback_text = polish()

st.markdown("---")
st.subheader("Polish Feedback")
st.markdown(polish_feedback_text)
st.code(polish_feedback_text)
