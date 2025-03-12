import streamlit as st
# from abc import ABC, abstractmethod
import re
# from modules.variable_input_classes import *
# import pandas as pd
# from dataclasses import dataclass
from fractions import Fraction

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