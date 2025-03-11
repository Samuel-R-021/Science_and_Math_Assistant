import streamlit as st
from abc import ABC, abstractmethod
import re
import chemparse as cp
import pandas as pd
from dataclasses import dataclass
from fractions import Fraction

# -------------- CLASS VARIABLES --------------------
@dataclass
class GeneralInput:
    value: str
    unit: str

    conversion_dic = {}

    @classmethod
    def units_list(cls):
        return list(cls.conversion_dic.keys())

    def str_to_latex(self, variable_name):
        return fr'{variable_name} = {self.value}\ {self.unit}' if self.value != '' else fr'{variable_name} =\ \ \ \textbf{{?}}'

    def convert(self, unit_out, decimals=12):
        conversion_dic = self.conversion_dic
        unit_in = self.unit
        self.value = round(float(self.value), ndigits=decimals)

        self.value *= conversion_dic[unit_in] / conversion_dic[unit_out]
        self.unit = unit_out
        return self

    def latex_convert(self, unit_out, decimals=12):
        conversion_dic = self.conversion_dic
        value_in = float(self.value) if decimals == 0 else round(float(self.value), ndigits=decimals)
        unit_in = self.unit
        value_out = value_in * conversion_dic[unit_in] / conversion_dic[unit_out]

        numerator = round(conversion_dic[unit_in] / conversion_dic[unit_out], ndigits=6) if conversion_dic[unit_out] <= conversion_dic[unit_in] else 1
        numerator = int(numerator) if int(numerator) - numerator == 0 else numerator

        denominator = round(conversion_dic[unit_out] / conversion_dic[unit_in], ndigits=6) if conversion_dic[unit_out] > conversion_dic[unit_in] else 1
        denominator = int(denominator) if int(denominator) - denominator == 0 else denominator

        return fr'{value_in}\ {unit_in}\times \frac{{{numerator}\ {unit_out}}}{{{denominator}\ {unit_in}}}= {value_out}\ {unit_out}'


class PressureInput(GeneralInput):
    str_name = 'Pressure'
    conversion_dic = {'atm': 1,
                      'Pa': 1/101325,
                      'kPa': 1/101.325,
                      'mmHg': 1/760}


class VolumeInput(GeneralInput):
    str_name = 'Volume'
    conversion_dic = {'L': 1,
                      'mL': 0.001,
                      'cm^3': 0.001,
                      'm^3': 1000}


class MolesInput(GeneralInput):
    str_name = 'Moles'
    conversion_dic = {'mol': 1,
                      'mmol': 0.001,
                      r'\mu mol': 0.000001}


class TemperatureInput(GeneralInput):
    str_name = 'Temperature'
    conversion_dic = {'K': 0,
                      r'^\circ \text{C}': 273.15}

    def convert(self, unit_out, decimals=2):
        conversion_dic = self.conversion_dic
        unit_in = self.unit

        self.value = round(float(self.value), ndigits=decimals) + (conversion_dic[unit_in] - conversion_dic[unit_out])
        self.unit = unit_out
        return self

    def latex_convert(self, unit_out, decimals=2):
        conversion_dic = self.conversion_dic
        value_in = round(float(self.value), ndigits=decimals)
        unit_in = self.unit
        value_out = value_in + (conversion_dic[unit_in] - conversion_dic[unit_out])
        sign = '-' if conversion_dic[unit_in] - conversion_dic[unit_out] < 0 else '+'

        # returns conversion steps
        return fr"""\begin{{array}}{{l}}{unit_out} = {unit_in} {sign} 273.15
                                    \\{unit_out} = {value_in} {sign} 273.15
                                    \\{unit_out} = {value_out}\ {unit_out} \end{{array}}""" if unit_in != unit_out else r'\text{Pick a different unit}'


class MolarityInput(GeneralInput):
    str_name = 'Molarity'
    conversion_dic = {r'\frac{mol}{L}': 1,
                      'M': 1,
                      r'\frac{mmol}{L}': 0.001,
                      'mM': 0.001}


class MolalityInput(GeneralInput):
    str_name = 'Molality'
    conversion_dic = {r'\frac{mol}{kg}': 1,
                      'm': 1}


class MassInput(GeneralInput):
    str_name = 'Mass'
    conversion_dic = {'g': 1,
                      'kg': 1000,
                      'mg': 0.001,
                      r'\mu g': 0.000001,
                      'ng': 0.000000001}


class DensityInput(GeneralInput):
    str_name = 'Density'
    conversion_dic = {r'\frac{g}{mL}': 1,
                      r'\frac{g}{cm^3}': 1,
                      r'\frac{kg}{L}': 1}


# class MolarMassInput(GeneralInput):
#     str_name = r'Molar\ Mass'
#     conversion_dic = {r'\frac{g}{mol}': 1}
#     pt = pd.read_csv('periodicTable(ChemCalc).csv', index_col='symbol')

#     def __init__(self, given, unit):
#         super().__init__(given, unit)
#         self.chemical_formula = self.molar_mass_calculator()

#     def molar_mass_calculator(self):

#         if re.match(r'\(?[A-Z]', self.value):
# #            from ClassChemEq import LatexCompoundFactory
#             input_chemical_formula = LatexCompoundFactory.str_to_latex(self.value)
#             compound = cp.parse_formula(self.value)
#             molar_mass = sum(value * float(self.pt.loc[key, 'atomicMass']) for key, value in compound.items())
#             self.value = str(round(molar_mass, ndigits=3))
#         else:
#             input_chemical_formula = ''
#         return input_chemical_formula

#     def str_to_latex(self, variable_name):
#         return fr'{variable_name}\ {self.chemical_formula} = {self.value}\ {self.unit}' if self.value != '' else fr'{variable_name}\ {self.chemical_formula}=\ \ \ \textbf{{?}}'


# class AtomicMassInput(MolarMassInput):
#     str_name = r'Atomic\ Mass'


class PercentYieldInput(GeneralInput):
    str_name = r'Percent\ yield'
    conversion_dic = {r'\%': 1}


class EnergyInput(GeneralInput):
    str_name = 'Energy'
    conversion_dic = {'J': 1,
                      'kJ': 1000,
                      'cal': 4.184,
                      'kcal': 4184,
                      'Cal': 4184}


class UnitlessInput(GeneralInput):
    str_name = 'Unitless'
    conversion_dic = {'': 1}


class EnthalpyInput(GeneralInput):
    str_name = 'Enthalpy'
    conversion_dic = {r'\frac{J}{g}': 1}


class SpecificHeatInput(GeneralInput):
    str_name = 'Specific Heat'
    conversion_dic = {r'\frac{J}{g\times ^\circ C}': 1,
                      r'\frac{J}{g\times K}': 1}


class HeatConstantsInput(GeneralInput):              # Evaluar si se dejan aqui o se mueven a ClassConstants
    str_name = 'Heat Constants'
    conversion_dic = {r'\frac{^\circ C\times kg}{mol}': 1}

class ConstantR:
    str_name = 'R'
    units_list = [r'\frac{L\times atm}{K \times mol}']

    def __init__(self):
        self.value = 0.08206
        self.unit = r'\frac{L\times atm}{K \times mol}'

    def custom_constant(self):
        if st.sidebar.checkbox('Custom R'):       # Para cuando haya que usar una constante especifica segun la pregunta
            self.value = st.sidebar.text_input('R Constant:', '0.08206')
        st.sidebar.info(fr'${self.value}\ {self.unit}$')
        return ConstantR

    def str_to_latex(self, variable_name):
        return fr'{variable_name} = {self.value}\ {self.unit}' if self.value != '' else fr'{variable_name} =\ \ \ \textbf{{?}}'

# ------------- END VARIABLES - START FORMULAS -------------------

class LatexCompoundFactory:

    @classmethod
    def str_to_latex(cls, coeff_compound_charge_state, add_ones=False):
        """ This take the coefficient/compound/charge/state (Ex. 2CO3{2-}{aq}) as text and rewrites it as Latex code
        """
        coeff, compound, charge, state = cls.compound_spliter(coeff_compound_charge_state)

        # Modificamos y agregamos el coeficiente
        coeff = Fraction(coeff) if coeff else 1
        latex_coeff_compound_charge_state = cls.add_coeff(coeff, add_ones)

        # separando el compuesto en una lista de tuplas, cada tupla tiene 2 item: letras y subindices
        latex_coeff_compound_charge_state += cls.add_latex_compound(compound)

        # Agregamos la carga si la tiene
        if charge is not None:
            latex_coeff_compound_charge_state += cls.add_charge(charge)

        # Agregamos estado de agregacion
        if state is not None:
            latex_coeff_compound_charge_state = fr'{{{latex_coeff_compound_charge_state}}}_{{({state})}}'

        return latex_coeff_compound_charge_state

    @staticmethod
    def compound_spliter(coeff_compound_charge_state):
        """ This separates the text like 2CO3{2-}{aq} into coefficient/compound/charge/state"""
        list_of_matches = re.match(r'(\d*\.*/*\d*)([a-zA-Z0-9()]+)({-?[0-9]*-?})?({s}|{l}|{g}|{aq})?', coeff_compound_charge_state)
        coeff, compound, charge, state = list_of_matches.groups()
        return coeff, compound, charge, state

    @staticmethod
    def add_coeff(coeff, add_ones):
        """ This returns coefficient in red and Latex if needed"""
        return '' if coeff == 1 and add_ones is False else fr'\color{{red}}{str(coeff)}\color{{black}}'

    @staticmethod
    def add_latex_compound(compound):
        """This one rewrites chemical formulas (Ex. CH4) from text to Latex code"""
        all_element_subscript = re.findall('(\D+)(\d*)', compound)
        return ''.join(fr'{element0_subscript1[0]}' if element0_subscript1[1] == '' else fr'{element0_subscript1[0]}_{{{element0_subscript1[1]}}}'for element0_subscript1 in all_element_subscript)

    @staticmethod
    def add_charge(charge):
        """This one rewrites compounds charges, if any, from text to Latex code"""
        if re.search('-', charge) is None:
            if charge == '{1}':
                charge = '+'
            elif charge != '{0}':
                charge = f'{charge}+'
        return fr'^{{{charge}}}'
    

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

        for variable_name, (variable_class, default_unit) in cls.variables_dic.items():

            if variable_name == unknown_value:
                input_object = variable_class('', default_unit)
                to_latex = input_object.str_to_latex(variable_name)
            elif hasattr(variable_class, 'custom_constant'):
                input_object = variable_class()
                input_object.custom_constant()
                to_latex = input_object.str_to_latex(variable_name)
            elif variable_name in variables_list:
                index = variable_class.units_list().index(default_unit) if default_unit != '' else 0
                value_input = st.sidebar.text_input(variable_name, ''  )
                unit_input = st.sidebar.radio(variable_name, variable_class.units_list(), index=index  )

                input_object = variable_class(value_input, unit_input)
                to_latex = input_object.str_to_latex(variable_name)

                # Para convertir el input a una unidad de conveniencia
                if st.sidebar.checkbox(f'Convert {variable_name}'  ):
                    new_unit = st.sidebar.selectbox(f'New {variable_name} unit', input_object.units_list() )

                    input_object = input_object.convert(new_unit, decimals=12)
                    to_latex += fr'={input_object.value}\ {input_object.unit}'
            else:  # #variable_name not in variables_list
                input_object = variable_class(None, None)
                to_latex = None

            input_objects_list.append(input_object)
            latex_input_list.append(to_latex) if variable_name in variables_list else None

            # el que funcionaba, por si acaso
            # if hasattr(variable_class, 'custom_constant'):
            #     input_object = variable_class()
            #     input_object.custom_constant()
            #     to_latex = input_object.str_to_latex(variable_name)
            # elif variable_name not in variables_list:
            #     input_object = variable_class(None, None)
            #     to_latex = None
            # elif variable_name == unknown_value:
            #     input_object = variable_class('', default_unit)
            #     to_latex = input_object.str_to_latex(variable_name)
            # else:  # Si el input es una variable
            #     index = variable_class.units_list().index(default_unit) if default_unit != '' else 0
            #     value_input = st.sidebar.text_input(variable_name, ''  )
            #     unit_input = st.sidebar.radio(variable_name, variable_class.units_list(), index=index  )
            #
            #     input_object = variable_class(value_input, unit_input)
            #     to_latex = input_object.str_to_latex(variable_name)
            #
            #
            #     # Para convertir el input a una unidad de conveniencia
            #     if st.sidebar.checkbox(f'Convert {variable_name}'  ):
            #         new_unit = st.sidebar.selectbox(f'New {variable_name} unit', input_object.units_list() )
            #
            #         input_object = input_object.convert(new_unit, decimals=12)
            #         to_latex += fr'={input_object.value}\ {input_object.unit}'
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