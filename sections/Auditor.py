import streamlit as st
from modules.auditor_service import service_feedback, service_3_gaps_info
from modules.auditor_polish import polish
from modules.auditor_inputs import service_2_checks, service_3_num_gaps


st.header("Service and Polish Inputs")
st.markdown("---")

# All columns to fill the inputs
inputs, start, end, minutes, instances = st.columns(5)
with inputs:
    st.markdown('Checkings',
                help="When the expert checked the student's understanding"
                )
    before_after = service_2_checks()
    st.markdown("---")

    num_gaps = service_3_num_gaps()
    st.markdown("---")

    polish_feedback_text = polish(instances)

gaps_feedback, gap_score = service_3_gaps_info(num_gaps, start, end, minutes)

service_feedback_text= service_feedback(before_after, gaps_feedback, gap_score)

# Add a separator at the end for a cleaner look
st.markdown("---")

st.subheader("Service Feedback")
st.markdown(service_feedback_text)
st.code(service_feedback_text)

st.markdown("---")

st.subheader("Polish Feedback")
st.markdown(polish_feedback_text)
st.code(polish_feedback_text)

st.markdown("---")

st.subheader("Accuracy Feedback")
st.markdown(polish_feedback_text)
st.code(polish_feedback_text)

st.markdown("---")

st.subheader("Format Feedback")
st.markdown(polish_feedback_text)
st.code(polish_feedback_text)
