import streamlit as st

# ----- Page setup -----

home_page = st.Page(
    page='sections/Home.py',
    title='Home',
    default=True
)
math_page = st.Page(
    page='sections/Math.py',
    title='Math',
)
chem_page = st.Page(
    page='sections/Chem.py',
    title='Chem',
)
stats_page = st.Page(
    page='sections/Stats.py',
    title='Stats',
)


# ----- Navigation ---------

pages = st.navigation(pages=
    {
        '':[home_page],
        'Topics':[chem_page,math_page,stats_page]
        }
        )


# -------Run Navigation-------

if __name__== '__main__':

    pages.run()

    st.sidebar.text('Made by Samuel Rangel')

    col1, col2, col3 = st.columns(3)
    back_color = 'secondary'

    if col1.button('For multiple questions',type=back_color, use_container_width=True):
        st.code('Per policy of the platform, I can only help you with one question per session')
        st.code("""Per policy of the platform, I can only help you with one part of the question per session.
            Unless you tell me otherwise, I'll start and help you with the first one""")
        
    if col2.button('For direct answer requested', type=back_color, use_container_width=True):
        st.code('Per policy of the platform, I can not give you the answer without a complete explanation')

    if col3.button('Ending message',type=back_color, use_container_width=True):
        st.code("Please check and let me know if you have any questions.")
        st.code("If you're satisfied with the explanation provided, please don't forget to rate accordingly :)")

    

