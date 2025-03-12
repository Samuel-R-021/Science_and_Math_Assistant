import streamlit as st
from abc import ABC, abstractmethod
import re
from modules.variable_input_classes import *
# import pandas as pd
from dataclasses import dataclass
from fractions import Fraction



    

class GeneralConcept(ABC):
    variables_dic = {}
    str_name = ''
    despeje_strings = {}

    @classmethod
    def variables_list(cls ):
        return list(cls.variables_dic.keys())

    @classmethod
    def concept_constructor(cls, variables_list, unknown_value ):
        input_objects_list = []
        latex_input_list = []

        columns = st.columns(len(variables_list))
        
        for column_index, (variable_name, (variable_class, default_unit)) in enumerate(cls.variables_dic.items()):
            with columns[column_index]:
                if variable_name == unknown_value:
                    input_object = variable_class('', default_unit)
                    to_latex = input_object.str_to_latex(variable_name)
                elif hasattr(variable_class, 'custom_constant'):
                    input_object = variable_class()
                    input_object.custom_constant()
                    to_latex = input_object.str_to_latex(variable_name)
                elif variable_name in variables_list:
                    index = variable_class.units_list().index(default_unit) if default_unit != '' else 0
                    value_input = st.text_input(variable_name, ''  ) #sidebar
                    unit_input = st.radio(variable_name, variable_class.units_list(), index=index, horizontal=True  )#sidebar

                    input_object = variable_class(value_input, unit_input)
                    to_latex = input_object.str_to_latex(variable_name)

                    # Para convertir el input a una unidad de conveniencia
                    if st.checkbox(f'Convert {variable_name}', disabled = value_input == ''):#sidebar
                        new_unit = st.selectbox(f'New {variable_name} unit', input_object.units_list() ) #sidebar

                        input_object = input_object.convert(new_unit, decimals=12)
                        to_latex += fr'={input_object.value}\ {input_object.unit}'
                else:  #variable_name not in variables_list
                    input_object = variable_class(None, None)
                    to_latex = None
            input_objects_list.append(input_object)
            latex_input_list.append(to_latex) if variable_name in variables_list else None

        return input_objects_list, latex_input_list

    def despeje(self, unknown_variable):

        despeje = fr"\begin{{array}}{{l}}\textit{{Clearing for '${unknown_variable}$', this way}}:\\\\{self.despeje_strings['formula']}\\"
        despeje += self.despeje_strings[unknown_variable]
        despeje += r'\end{array}'
        return despeje

    @abstractmethod
    def calcular(self, unknown_value):
        pass

    def calc_steps(self, unknown_variable, result_object, decimals):

        steps = r'\begin{array}{l}\textit{Solving}:\\\\'
        steps += self.get_step_string(unknown_variable)
        steps += fr'={round(result_object.value, ndigits=decimals)}\ {result_object.unit}\end{{array}}'
        return steps

    @abstractmethod
    def get_step_string(self, unknown_variable):
        pass


@dataclass
class IdealGas(GeneralConcept):
    P: object
    V: object
    n: object
    R: object
    T: object

    variables_dic = {'P': (PressureInput, 'atm'),
                     'V': (VolumeInput, 'L'),
                     'n': (MolesInput, 'mol'),
                     'R': (ConstantR, r'\frac{L\times atm}{K \times mol}'),
                     'T': (TemperatureInput, 'K')}

    str_name = 'Ideal Gas'

    despeje_strings = {'formula': 'PV=nRT',
                       'P': r'P=\frac{nRT}V',
                       'V': r'V=\frac{nRT}P',
                       'n': r'\frac{PV}{RT}=n\\n=\frac{PV}{RT}',
                       'R': r'\frac{PV}{nT}=R\\R=\frac{PV}{nT}',
                       'T': r'\frac{PV}{nR}=T\\T=\frac{PV}{nR}'}

    @staticmethod
    def concept_phase_text():

        return {'subheader': '**_Ideal Gas Concept_**',
                 'concept': ['''An ideal gas is a gas whose particles undergo perfectly elastic collisions (no energy lost upon collision) and experience no intermolecular attractions. Given a confined gas under these conditions (ie. an ideal gas), the number of gas particles, its volume, pressure, and temperature can all be related into a single equation called the Ideal Gas Law: PV=nRT. P represents Pressure, V represents Volume, n represents number of particles in moles, T represents temperature (K), and R is the universal gas constant, and can assume multiple values depending on the units of the other variables.''',
                             r"""\begin{array}{l}\begin{array}{c}\textit{The Ideal Gas equation is}\\PV=nRT\end{array}\\\begin{array}{rl}\textit{Where}:&\\P=&\textit{Pressure}\\V=&\textit{Volume}\\n=&\textit{Number of moles}\\R=&\textit{Gas constant}\\T=&\textit{Temperature}\end{array}\end{array}"""]}
        
        
    def calcular(self, unknown_value):
        try:
            if unknown_value == 'P':
                self.P.value = float(self.n.value) * float(self.R.value) * float(self.T.value) / float(self.V.value)
                return self.P
            elif unknown_value == 'V':
                self.V.value = float(self.n.value) * float(self.R.value) * float(self.T.value) / float(self.P.value)
                return self.V
            elif unknown_value == 'n':
                self.n.value = float(self.P.value) * float(self.V.value) / (float(self.R.value) * float(self.T.value))
                return self.n
            elif unknown_value == 'R':
                self.R.value = float(self.P.value) * float(self.V.value) / (float(self.n.value) * float(self.T.value))
                return self.R
            elif unknown_value == 'T':
                self.T.value = float(self.P.value) * float(self.V.value) / (float(self.n.value) * float(self.R.value))
                return self.T
        except Exception:
            return 'Please provide the necessary inputs.'

    def get_step_string(self, unknown_variable):
        steps_strings = {'P': fr'P=\frac{{nRT}}{{V}}\\P=\frac{{{self.n.value}\times{self.R.value}\times{self.T.value}}}{{{self.V.value}}}\\P',
                         'V': fr'V=\frac{{nRT}}{{P}}\\V=\frac{{{self.n.value}\times{self.R.value}\times{self.T.value}}}{{{self.P.value}}}\\V',
                         'n': fr'n=\frac{{PV}}{{RT}}\\n=\frac{{{self.P.value}\times {self.V.value}}}{{{self.R.value}\times {self.T.value}}}\\n',
                         'R': fr'R=\frac{{PV}}{{nT}}\\R=\frac{{{self.P.value}\times {self.V.value}}}{{{self.n.value}\times {self.T.value}}}\\R',
                         'T': fr'T=\frac{{PV}}{{nR}}\\T=\frac{{{self.P.value}\times {self.V.value}}}{{{self.n.value}\times {self.R.value}}}\\T'}
        return steps_strings[unknown_variable]