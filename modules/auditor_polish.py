import streamlit as st

def polish(instances):

    polish_feedback = "All good"
    
    entire_session = st.radio("All messages?",["No", "Yes"],horizontal=True)
    if entire_session == "Yes":
        polish_feedback = "You received a D score because the entire session is incorrectly formatted. In future sessions, please -. Doing so will help you improve your score."
        
    num_msg = st.number_input(
    label="Number of messages",
    min_value= 0,
    value=100 if entire_session== "Yes" else 0,
    step=1,
    help="Select the total number of messages incorrectly formatted.",
    disabled=True if entire_session== "Yes" else False
    )

    text_type = st.radio("Only text?",["No", "Yes"],
                            horizontal=True,
                            disabled=True if entire_session == "Yes" or num_msg >=1 else False,
                            index=  0)
    polish_feedback = "No problems here" if text_type == "Yes" else polish_feedback

    if entire_session == "No" and num_msg >= 0:
        with instances:
            instance_data = []


            previous_instance = 1
            disabled = False

            if num_msg == 0:
                previous_instance = 0
                num_msg = 1
                disabled = True

            for i in range(int(num_msg)):
                # Use the 'with' statement to place all subsequent widgets inside the current column.
                
                instance_msg = st.number_input(
                    label="Message",
                    min_value=previous_instance,
                    step=1,
                    key=f"msg_{i}",
                    disabled=disabled,
                    help="The number of the message that starts this gap."
                )
                
                
                instance_data.append(str(instance_msg))

                # Update the previous_end_msg variable for the next iteration.
                # This is done after all the widgets for the current gap have been created.
                previous_instance = instance_msg + 1

            # Join the formatted gap strings with commas
            instance_text = ", ".join(instance_data)
            if num_msg == 2:
                polish_score = "B" 
            elif num_msg == 3:
                polish_score = "C"
            else:
                polish_score = "D"
            polish_feedback = (f"You received a {polish_score} score because there are {num_msg} instances (messages #{instance_text}) " 
                                "where the messages are incorrectly formatted. In future sessions, please -. Doing so will help you improve your score.")

    return polish_feedback