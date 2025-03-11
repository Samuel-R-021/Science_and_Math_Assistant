import streamlit as st
from modules.module_topics import *
from modules.front_end_interface import front_interface,\
                                         unknown_value_selection, \
                                          data_given,\
                                           sc_notation_str_to_latex,\
                                         number_formatter, final_answer, check_given 
from formula_solver.chem_formulas import IdealGas

# ----------- LOS VALUE FUERON ORIGINALMENTE FUNCIONES, NO STRINGS ----------
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

# POR AHORA, PARA HACER QUE FUNCIONE
concept_class = IdealGas
if topic == 'basic_formulas':
  
  front_interface(concept_class)