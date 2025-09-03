import streamlit as st

def concept_feedback(concept_type):
    template_dict = {'Incomplete': "You received a B score because the concept provided was, and I quote, '', which is insufficient and unhelpful because it doesn’t help in filling the gap in the student's knowledge. Next time, please provide complete and detailed concepts in the concept phase before solving the questions. Doing so will help improve your score.",
                     'No concept': "You received an automatic C score because there was no concept provided, you just went directly to the step-by-step, which is unhelpful for the student because it doesn’t help in filling the gap in the student's knowledge. In future sessions, please provide complete and detailed concepts in the concept phase before solving the questions. Doing so will help you improve your score.",
                     'Long messages': "In this session, you sent - messages (messages #) with more than 5 lines and/or more than 1 math step. In future sessions, please remember to keep math steps messages no longer than 5 lines and no more than 1 step."
                     }
    return template_dict[concept_type] if concept_type else "All good"
    