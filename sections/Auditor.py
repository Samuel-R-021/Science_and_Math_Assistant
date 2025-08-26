import streamlit as st

# Set the title of the Streamlit app
st.title("Service Section Templates")

col1, col2 = st.columns(2, vertical_alignment="center")

# --- First Widget: Number of time gaps ---
# Create a number input for the user to select a positive integer for the number of time gaps.
# The `min_value` is set to 1 to ensure a positive integer.
with col2:
    num_gaps = st.number_input(
        label="Number of time gaps",
        min_value=2,
        step=1,
        help="Select the total number of gaps between messages."
    )

# --- Second Widget: Inputs for each gap ---
# Create a container to hold the gap inputs. This keeps the UI organized.
with col1:
    st.subheader(f"Define the {num_gaps} gaps")

# The widgets for each gap are created in a loop based on the number selected above.
# The `key` parameter is crucial here to ensure each widget is unique when rendered in a loop.
# It is a best practice in Streamlit to provide unique keys for dynamically generated widgets.
# This variable will store the last end message number to use for the next gap's start message.
# It is initialized to 0, so the first gap can start with message number 1.
cols = st.columns(int(num_gaps))

previous_end_msg = -1

# A list to store the data for each gap
gaps_data = []

for i in range(int(num_gaps)):
    # Use the 'with' statement to place all subsequent widgets inside the current column.
    with cols[i]:
        st.write(f"**Gap {i + 1}**")
        
        # The min_value for the start message is set to the previous gap's end message plus 1.
        start_msg = st.number_input(
            label="Start",
            min_value=previous_end_msg + 1,
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
            min_value=3,
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

# Add a separator at the end for a cleaner look
st.markdown("---")

# --- Output Section: Generate the summary text ---
st.subheader("Generated Template")

# Determine the score based on the number of gaps
score = "B" if num_gaps == 2 else "C"

# Format the list of gaps for the output string
formatted_gaps = []
for gap in gaps_data:
    formatted_gaps.append(f"#{gap['start']}-{gap['end']} {gap['length']} min")

# Join the formatted gap strings with commas
gaps_text = ", ".join(formatted_gaps)

# Generate the final output string
output_text = (
    f"You received a {score} score because there are {int(num_gaps)} gaps of time "
    f"({gaps_text}) longer than 2 minutes. In future sessions, please do not let too "
    "much time pass between messages. Doing so will help you improve your score."
)

st.code(output_text)
# Display the generated text
if st.button("Service Feedback"):
    st.markdown(output_text)