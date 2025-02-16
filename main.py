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
        'Topics':[chem_page, math_page, stats_page]
        }
        )

# -------Run Navigation-------

if __name__== '__main__':

    pages.run()
