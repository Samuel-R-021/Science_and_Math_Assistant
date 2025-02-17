import streamlit as st
from modules.module_topics import *
from formula_solver.math_formulas import *


topics = {'Choose one': '',
            #   'Basic Common Formulas': basic_formulas,
            #   'Gas Laws': gas_laws,
            #   'Thermodynamic Formulas': thermo_formulas,
            #   'Chemical Reaction Equations': chem_equation,
            #   'Formula maker': formula_maker,
              'The Quadratic Formula': 'the_quadratic_formula'}

st.title('_Math Assistant_')
session_intro()

st.sidebar.subheader('Choose a topic')


topic = topic_selection(topics)

if topic == 'the_quadratic_formula':
    the_quadratic_formula()