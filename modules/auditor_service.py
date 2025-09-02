import streamlit as st
from modules.auditor_inputs import gap_start, gap_end, gap_time

def service_2_feedback(gap_feedback, before_after=None): 
    if gap_feedback: 
        feedback_checking = "during the session" if before_after == "Both" else f"{before_after} the final answer"
        return feedback_checking
    feedback_checking = ("Remember to always check with students in the form of a clear direct question at least once during "
            "the concept/explanation and another after the final answer or during discussion "
            "(avoid sending 2 or more messages together at the end after the final answer, just to fulfill the criteria."
            " In that case, it will be considered as 1)")
    return feedback_checking
    
def service_3_gaps_info(num_gaps, start, end, minutes):

    # This variable will store the last end message number to use for the next gap's start message.
    # It is initialized to 0, so the first gap can start with message number 0 (which is the start of the session).
    previous_end_msg = 0
    
    # A list to store the data for each gap
    gaps_data = []

    # Initial values for automatic No score and number of gaps equal or greater than 6 minutes
    auto_no = False
    geq_6 = 0
    
    # start, end, minutes = st.columns(3)
    if num_gaps == 0:
        rows = 1
        disabled = True
    else:
        rows = num_gaps
        disabled = False


    for i in range(int(rows)):
        
        with start:
            start_msg = gap_start(previous_end_msg, disabled)
        with end:
            end_msg = gap_end(start_msg, disabled)
        with minutes:
            gap_length = gap_time(i, disabled)

            # Store the current gap's data in the list
        gaps_data.append({
            "start": int(start_msg),
            "end": int(end_msg),
            "length": int(gap_length)
        })

        # Update the previous_end_msg variable for the next iteration.
        # This is done after all the widgets for the current gap have been created.
        previous_end_msg = end_msg

        if gap_length > 5:
            auto_no = True
            geq_6 += 1

    # return gaps_data, auto_no, geq_6
    return service_3_fback_score(num_gaps, gaps_data, auto_no, geq_6)

def service_3_fback_score(num_gaps, gaps_data, auto_no, geq_6):

    if num_gaps == 0:
        gap_score = "A"
        gaps_feedback = None
        return gaps_feedback, gap_score

    # Format the list of gaps for the output string
    formatted_gaps = []
    for gap in gaps_data:
        formatted_gaps.append(f"#{gap['start']}-{gap['end']} {gap['length']} min")

    # Join the formatted gap strings with commas
    gaps_text = ", ".join(formatted_gaps)

    if num_gaps == 1 and auto_no is False:
        gap_score = "A"
        gaps_feedback = None
        return gaps_feedback, gap_score

    if auto_no is False:
        gaps_feedback = f"there are {int(num_gaps)} gaps of time ({gaps_text}) longer than 2 minutes"
    elif int(num_gaps) == 1:
        gaps_feedback = (f"there is a huge gap of time ({gaps_text}) longer than 5 minutes, "
                            f"which receives an automatic 'No' score")
    else:
        if int(num_gaps) == geq_6 == 2:
            geq_6 = "both"
        if int(num_gaps) == geq_6:
            geq_6 = "all"
        gaps_feedback = (f"there are {int(num_gaps)} gaps of time ({gaps_text}), {geq_6} of them longer than 5 minutes, "
                            f"which receives an automatic 'No' score")
        
    gap_score = "B" if num_gaps == 2  and auto_no == False else "C"
    
    return gaps_feedback, gap_score

def service_feedback(before_after, gaps_feedback, gap_score):

    service_feedback = "No feedback has been created"

    match (bool(before_after), bool(gaps_feedback)):
        case (False, False):  # No issues
            service_feedback = "All good"
        case (True, False):   # Only checking issue
            service_feedback = service_2_feedback(gaps_feedback)
        case (False, True):   # Only gaps issue
            service_feedback = (f"You received a {gap_score} score because {gaps_feedback}. "
                                "In future sessions, please do not let too much time pass between messages. Doing so will help you improve your score.")
        case (True, True):    # Both issues
            
            checking_feedback = service_2_feedback(True, before_after)
            
            if before_after != "Both" and gap_score == "B":
                service_score = "B"
            elif (before_after == "Both" and gap_score == "B") or (before_after != "Both" and gap_score == "C"):
                service_score = "C"
            else:
                service_score = "D"

            service_feedback = (f"You received a {service_score} score because "
                                f"1) there was no attempt to check the student's understanding {checking_feedback}, and "
                                f"2) {gaps_feedback}. "
                                f"In future sessions, please remember to check with students at least once before and after the final answer, and do not let too much time pass between messages. Doing so will help you improve your score.")
    return service_feedback