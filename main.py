import streamlit as st


st.title('_Testing Repository_')


back_color = 'primary'

if st.button('For multiple questions',type=back_color):
    st.code('Per policy of the platform, I can only help you with one question per session')
    st.code("""Per policy of the platform, I can only help you with one part of the question per session.
                Unless you tell me otherwise, I'll start and help you with the first one""")

if st.button('For direct answer requested', type=back_color):
    st.code('Per policy of the platform, I can not give you the answer without a complete explanation')

if st.button('Ending message',type=back_color):
    st.code("Please check and let me know if you have any questions.")
    st.code("If you're satisfied with the explanation provided, please don't forget to rate accordingly :)")

