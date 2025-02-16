import streamlit as st
from modules.module_topics import *

# ----------- LOS VALUE FUERON ORIGINALMENTE FUNCIONES, NO STRIGS ----------
topics = {'Choose one': '',
              'Basic Common Formulas': 'basic_formulas',
              'Gas Laws': 'gas_laws',
              'Thermodynamic Formulas': 'thermo_formulas',
              'Chemical Reaction Equations': 'chem_equation',
            #   'Formula maker': formula_maker,
            #   'Algebra testing': 'the_quadratic_formula'
              }

st.title('_Chem Assistant_')
session_intro()

st.sidebar.subheader('Choose a topic')


topic = topic_selection(topics)  # Recibe el valor de la llave seleccionada en la funcion 


# -------  REVISAR ORIGINAL ------------
# if topic == 'the_quadratic_formula':
#     the_quadratic_formula()

st.subheader(topic, divider=True)

