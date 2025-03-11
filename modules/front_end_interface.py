import streamlit as st
import re

#-----------------------------------------------------------------------

def unknown_value_selection(concept_str_name, variables_list):
    return st.selectbox(concept_str_name, ['Choose a variable'] + variables_list)

def check_given(latex_input_list):
    for latex_input in latex_input_list:
        latex_input = sc_notation_str_to_latex(latex_input)
        if latex_input.endswith('{?}'):
            st.error(f'${latex_input}$')
        else:
            st.info(f'${latex_input}$')


def data_given(latex_input_list):

    data_output = r'\begin{array}{l}\textit{Given}:\\\\'
    data_output += r'\\'.join(latex_input_list)
    data_output += r'\end{array}'

    return sc_notation_str_to_latex(data_output)


def sc_notation_str_to_latex(latex_string):
    if sc_notation_findings := re.findall(r'[0-9]+\.?[0-9]*e\+?-?[0-9]+', latex_string):
        for sc_notation_value in sc_notation_findings:
            base, power = re.match(r'([0-9]+\.?[0-9]*)e\+?(-?[0-9]+)', sc_notation_value).groups()
            latex_string = latex_string.replace(sc_notation_value, fr'{base} \times 10^{{{power}}}')
            # re.escape es para "escapar" todos los metacaracteres para no hacerlo manualmente, por el problema de
            # usar re.sub y el metacaracter "+"
            # latex_string = re.sub(re.escape(sc_notation_value), fr'{base} \\times 10^{{{power}}}', latex_string)
    return latex_string


def number_formatter(result_value):
    number_format = st.selectbox('format', ['default', 'rounded', 'scientific notation'])

    if number_format == 'default':
        return result_value
    elif number_format == 'rounded':
        place = st.number_input('place to round', -10, 10, 5)
        return round(result_value, ndigits=place)
    else: # scientific notation
        return f'{result_value:.6e}'


def final_answer(unknown_value, result_object):

    st.subheader('**Final answer**',divider='red')
    format_type = st.radio('Final Answer:', ['Default', 'Standard rounding', 'Scientific notation'])
    if format_type == 'Default':
        st_output = fr'${unknown_value} = {result_object.value:.5f}\ {result_object.unit}$'
        answer = sc_notation_str_to_latex(fr'\begin{{array}}{{l}}\textit{{Final answer}}:\\\\{unknown_value}={result_object.value:.5f}\ {result_object.unit}\end{{array}}')
    elif format_type == 'Scientific notation':
        decimals = st.number_input('# Decimales', 0, 10, 3)
        rounding_type = st.radio('type of rounding', ['Decimals', 'Sig figs'])
        if rounding_type == 'Decimals':
            rounding_text = f'{decimals} decimals'
        elif rounding_type == 'Sig figs':
            rounding_text = f'{decimals + 1} Sig figs'
        st_output = fr'${unknown_value} = {result_object.value:.{decimals}e}\ {result_object.unit}$'
        answer = sc_notation_str_to_latex(fr'\begin{{array}}{{l}}\textit{{The final answer (rounded to}}\\\textit{{{rounding_text}) is}}:\\\\{unknown_value}={result_object.value:.{decimals}e}\ {result_object.unit}\end{{array}}')
    else: # standard rounding
        decimals = st.number_input('# Decimales', -10, 10, 5)
        result_value = f'{result_object.value:.{decimals}f}' if decimals >= 0 else int(round(result_object.value, ndigits=decimals))
        rounding_type = st.radio('type of rounding', ['Decimals', 'Sig figs'])
        if rounding_type == 'Decimals' and decimals >= 0:
            rounding_text = f'{decimals} decimals'
        elif rounding_type == 'Sig figs':
            length_str = len(str(result_value))
            rounding_text = f'{length_str + decimals} Sig figs' if decimals <= 0 else f'{length_str - 1} Sig figs'

        st_output = fr'${unknown_value} = {result_value}\ {result_object.unit}$'
        answer = sc_notation_str_to_latex(fr'\begin{{array}}{{l}}\textit{{The final answer (rounded to}}\\\textit{{{rounding_text}) is}}:\\\\{unknown_value}={result_value}\ {result_object.unit}\end{{array}}')

    return st_output, answer

# ------------------------------------------------------------------------



# Main function to run the Streamlit app
def front_interface(concept_class):
    # ----------------------------- Concept phase --------------------------------------
    concept = concept_class.concept_phase_text()

    st.subheader(concept['subheader'],divider='red')
    for text in concept['concept']:
        st.code(text)

    # ------------------------------------ Inputs ----------------------------------------
    st.subheader('**_Variable Inputs_**',divider='red')
    variables_list = concept_class.variables_list()
    unknown_value = unknown_value_selection(concept_class.str_name, variables_list)

    if unknown_value != 'Choose a variable':
        input_objects_list, latex_input_list = concept_class.concept_constructor(variables_list, unknown_value)

        # Formula-Concept object creation
        concept_object = concept_class(*input_objects_list)

        # DataInput checking
        check_given(latex_input_list)
    
    # ----------------------------- Calculation ------------------------------------------------------
        result_object = concept_object.calcular(unknown_value)
        
        incomplete_inputs = type(result_object) == str
        
        st.warning(result_object) if incomplete_inputs else None

        if not incomplete_inputs and st.checkbox(f'Cálculo de "{unknown_value}" paso a paso', disabled= incomplete_inputs):

            st.subheader('**_Step-by-Step_**',divider='red')
            st.success(sc_notation_str_to_latex(fr'${unknown_value} = {result_object.value}\ {result_object.unit}$'))

            # GIVEN DATA
            data_output = data_given(latex_input_list)
            # data_output = sc_notation_str_to_latex(data_output) REDUNDANTE
            st.write('**Given**')
            st.latex(data_output)
            st.code(data_output)

            # DESPEJE
            if unknown_value in list(concept_object.despeje_strings.keys()): # unknown_value != concept_object.str_name and (previous code, just in case)
                despeje = concept_object.despeje(unknown_value)

                st.write('**Despeje**')
                st.latex(despeje)
                st.code(despeje)

            # SUSTITUCION Y CALCULO
            st.write('**Sustitucion y Cálculo**')
            decimals = st.number_input('# Decimales', -6, 15, 5  )
            calculation = concept_object.calc_steps(unknown_value, result_object, decimals)
            calculation = sc_notation_str_to_latex(calculation)
            st.latex(calculation)
            st.code(calculation)

            # CONVERSIONES
            if st.checkbox('Convertir'  ):

                unit_out = st.selectbox('Unit out', result_object.units_list()  )

                conversion_steps = result_object.latex_convert(unit_out, decimals)
                conversion_steps = sc_notation_str_to_latex(conversion_steps)

                result_object = result_object.convert(unit_out, decimals)

                st.latex(conversion_steps)
                st.code(conversion_steps)

        # FINAL ANSWER
        if not incomplete_inputs:
            st_output, answer = final_answer(unknown_value, result_object)
            answer = sc_notation_str_to_latex(answer)
            st.success(st_output)
            st.latex(answer)
            st.code(answer)
            

    
