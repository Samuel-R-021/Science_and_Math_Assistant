import streamlit as st

def service_2_checks():

    before = st.checkbox('before')
    after = st.checkbox('after')

    match (bool(before), bool(after)):
        case (False, False):  # No checkings
            before_after = "Both"
        case (True, False):   # Checked before
            before_after = "after"
        case (False, True):   # Checked after
            before_after = "before"
        case (True, True):    # Checked both
            before_after = None

    return before_after

def service_3_num_gaps():
     
    return st.number_input(
        label="Number of gaps",
        min_value=0,
        step=1,
        help="Select the total number of gaps between messages."
    )


def gap_start(previous_end_msg, disabled):
    return st.number_input(
                label="Start",
                min_value=previous_end_msg,
                step=1,
                disabled=disabled,
                help="The number of the message that starts this gap."
            )
    

def gap_end(start_msg, disabled):
    return st.number_input(
                label="End",
                min_value=start_msg + 1,
                step=1,
                disabled=disabled,
                help="The number of the message that ends this gap."
            )

def gap_time(i, disabled):
    return st.number_input(
                label="Length",
                min_value=3,
                step=1,
                key = i,
                disabled=disabled,
                help="The length of the gap in a positive integer (e.g., minutes)."
            )

