import streamlit as st

def service():
    col1, col2 = st.columns(2, vertical_alignment="top")
    
    with col1:
        missing_checks = st.number_input(
            label="Number of missing checkings",
            min_value=0,
            max_value=2,
            step=1,
            help="Select the total number of missing checkings during the session."
        )

        num_gaps = st.number_input(
            label="Number of time gaps",
            min_value=0,
            step=1,
            help="Select the total number of gaps between messages."
        )
        
        

    with col2:
        
        # st.container is used to define variables in one order, but to show them in a different order
        container = st.container()

        long_gap = st.radio("\> 5 min?",["No", "Yes"],
                            horizontal=True,
                            disabled=True if num_gaps != 1 else False
                            )
         
        # It is defined after long_gap, but shown first using st.container
        before_after = container.radio("Before or after the final answer?",
                                    ["before","after"],
                                    horizontal=True,
                                    disabled=False if missing_checks == 1 and num_gaps >= 1 and long_gap== "Yes" else True
                                    )
        if missing_checks > 1:
            before_after = "Both"
        elif missing_checks == 0:
            before_after = None
        
        # long_gap = st.radio("\> 5 min?",["No", "Yes"],
        #                     horizontal=True,
        #                     disabled=True if num_gaps != 1 else False
        #                     )
        if long_gap == "No" and num_gaps == 1:
            num_gaps = 0    
        

    return before_after, num_gaps

def service_2_check():    
    feedback_checking = ("Remember to always check with students in the form of a clear direct question at least once during "
            "the concept/explanation and another after the final answer or during discussion "
            "(avoid sending 2 or more messages together at the end after the final answer, just to fulfill the criteria."
            " In that case, it will be considered as 1)")
    return feedback_checking

def service_3_time(num_gaps):

    if num_gaps < 1:
        gap_score = "A"
        gaps_feedback = None
        return gaps_feedback, gap_score
    
    # Add a separator at the end for a cleaner look
    st.markdown("---")


    # This variable will store the last end message number to use for the next gap's start message.
    # It is initialized to 0, so the first gap can start with message number 0 (which is the start of the session).
    previous_end_msg = 0
    
    # A list to store the data for each gap
    gaps_data = []

    # We create as columns as number of gaps, to then input the data about each gap
    cols = st.columns(int(num_gaps))

    # Initial values for automatic No score and number of gaps equal or greater than 6 minutes
    auto_no = False
    geq_6 = 0

    # Initial value of time gap: 6 min if it's only 1 gap, 3 min for more gaps
    min_time_gap = 6 if num_gaps == 1 else 3

    for i in range(int(num_gaps)):
        # Use the 'with' statement to place all subsequent widgets inside the current column.
        
        with cols[i]:
            st.write(f"**Gap {i + 1}**")
            
            # The min_value for the start message is set to the previous gap's end message plus 1.
            start_msg = st.number_input(
                label="Start",
                min_value=previous_end_msg,
                step=1,
                key=f"start_msg_{i}",
                help="The number of the message that starts this gap."
            )
            
            # The min_value for the end message is still based on the current start message.
            end_msg = st.number_input(
                label="End",
                min_value=start_msg + 1,
                step=1,
                key=f"end_msg_{i}",
                help="The number of the message that ends this gap."
            )
            
            # A number input for the length of the gap.
            gap_length = st.number_input(
                label="Length",
                min_value=min_time_gap,
                step=1,
                key=f"gap_length_{i}",
                help="The length of the gap in a positive integer (e.g., minutes)."
            )

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

    

    # Format the list of gaps for the output string
    formatted_gaps = []
    for gap in gaps_data:
        formatted_gaps.append(f"#{gap['start']}-{gap['end']} {gap['length']} min")

    # Join the formatted gap strings with commas
    gaps_text = ", ".join(formatted_gaps)

    if not auto_no:
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
        
    gap_score = "B" if num_gaps == 2 and auto_no == False else "C"
    
    return gaps_feedback, gap_score

def service_feedback(before_after, gaps_feedback, gap_score):

    service_feedback = "No text has been created"

    match (bool(before_after), bool(gaps_feedback)):
        case (False, False):  # No issues
            service_feedback = "All good"
        case (True, False):   # Only checking issue
            service_feedback = service_2_check()
        case (False, True):   # Only gaps issue
            service_feedback = (f"You received a {gap_score} score because {gaps_feedback}. "
                                "In future sessions, please do not let too much time pass between messages. Doing so will help you improve your score.")
        case (True, True):    # Both issues
            checking_feedback = "during the session" if before_after == "Both" else f"{before_after} the final answer"
            service_score = "D" if before_after == "Both" and gap_score == "C" else "C"

            service_feedback = (f"You received a {service_score} score because 1) there was no attempt to check the student's understanding {checking_feedback}, and "
                           f"2) {gaps_feedback}. "
                           f"In future sessions, please remember to check with students at least once before and after the final answer, and do not let too much time pass between messages. Doing so will help you improve your score.")
    return service_feedback