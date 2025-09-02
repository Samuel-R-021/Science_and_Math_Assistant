import streamlit as st
from modules.auditor_service import service_feedback, service_3_gaps_info
from modules.auditor_polish import polish
from modules.auditor_inputs import service_2_checks, service_3_num_gaps


st.header("Service and Polish Inputs")
st.markdown("---")

col1, col2, col3 = st.columns([0.20,0.60,0.20], vertical_alignment="bottom" )

with col1:
    st.markdown('The expert checked:',
                help="When the expert checked the student's understanding"
                )
    before_after = service_2_checks()
    st.markdown('the final answer.')

with col2:
    num_gaps = service_3_num_gaps()

# --- Output Section: Generate the summary text ---
st.markdown("---")
start, end, minutes, instances = st.columns(4)

# gaps_data, auto_no, geq_6 = service_3_gaps_info(num_gaps, start, end, minutes)

# gaps_feedback, gap_score = service_3_fback_score(num_gaps, gaps_data, auto_no, geq_6)


gaps_feedback, gap_score = service_3_gaps_info(num_gaps, start, end, minutes)

with col3:
    polish_feedback_text = polish(instances)

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
