import streamlit as st

def session_intro():
    col1, col2, col3 = st.columns(3)

    if col1.button('For multiple questions', use_container_width=True):
        st.code('Per policy of the platform, I can only help you with one question per session')
        st.code("""Per policy of the platform, I can only help you with one part of the question per session.
            Unless you tell me otherwise, I'll start and help you with the first one""")
        
    if col2.button('For direct answer requested', use_container_width=True):
        st.code('Per policy of the platform, I can not give you the answer without a complete explanation')

    if col3.button('Ending message', use_container_width=True):
        st.code("Please check and let me know if you have any questions.")
        st.code("If you're satisfied with the explanation provided, please don't forget to rate accordingly :)")

def topic_selection(topics):
    # topics = {'Choose one': '',
    #         #   'Basic Common Formulas': basic_formulas,
    #         #   'Gas Laws': gas_laws,
    #         #   'Thermodynamic Formulas': thermo_formulas,
    #         #   'Chemical Reaction Equations': chem_equation,
    #         #   'Formula maker': formula_maker,
    #           'Algebra testing': 'the_quadratic_formula'}

    selected_topic = st.sidebar.selectbox('Topic', list(topics.keys()))

    # returns topic selected
    return topics[selected_topic] if selected_topic != 'Choose one' else ''