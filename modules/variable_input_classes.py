import streamlit as st
# from abc import ABC, abstractmethod
# import re
# import chemparse as cp
# import pandas as pd
from dataclasses import dataclass
# from fractions import Fraction

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
        if st.checkbox('Custom R'): #sidebar      # Para cuando haya que usar una constante especifica segun la pregunta
            self.value = st.text_input('R Constant:', '0.08206') # sidebar
        st.info(fr'${self.value}\ {self.unit}$') #sidebar
        return ConstantR

    def str_to_latex(self, variable_name):
        return fr'{variable_name} = {self.value}\ {self.unit}' if self.value != '' else fr'{variable_name} =\ \ \ \textbf{{?}}'
