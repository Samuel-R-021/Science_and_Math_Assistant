import streamlit as st
import re

# ---------------------- FUNCTION TOOLS ----------------------------
def unknown_value_selection(concept_str_name, variables_list):
    return st.selectbox(concept_str_name, ['Choose a variable'] + variables_list)


def check_given(latex_input_list):
    columns = st.columns(len(latex_input_list))
    for index, latex_input in enumerate(latex_input_list):
        with columns[index]:            
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


def final_answer(unknown_value: str, result_object: object) -> tuple[str, str]:
    """
    Generate the final answer in different formats and return LaTeX formatted strings.

    Parameters:
    unknown_value (str): The variable name to be used in the output.
    result_object (any): An object containing value and unit properties.

    Returns:
    tuple[str, str]: A tuple containing the formatted output and LaTeX string.
    """
    try:
        st.subheader('**Final answer**', divider='red')
        format_type = st.radio('Final Answer:', ['Default', 'Standard notation', 'Scientific notation'], horizontal=True, label_visibility='collapsed')
        
        col1, col2 = st.columns(2)
        if format_type == 'Default':
            st_output = fr'${unknown_value} = {result_object.value:.5f}\ {result_object.unit}$'
            answer = sc_notation_str_to_latex(fr'\begin{{array}}{{l}}\textit{{Final answer}}:\\\\{unknown_value}={result_object.value:.5f}\ {result_object.unit}\end{{array}}')
        elif format_type == 'Scientific notation':
            rounding_type = col1.radio('Type of rounding', ['Decimals', 'Sig figs'], horizontal=True)
            decimals = col2.number_input('# Decimales', 0, 10, 3)
            rounding_text = f'{decimals} decimals' if rounding_type == 'Decimals' else f'{decimals + 1} Sig figs'
            st_output = fr'${unknown_value} = {result_object.value:.{decimals}e}\ {result_object.unit}$'
            answer = sc_notation_str_to_latex(fr'\begin{{array}}{{l}}\textit{{The final answer (rounded to}}\\\textit{{{rounding_text}) is}}:\\\\{unknown_value}={result_object.value:.{decimals}e}\ {result_object.unit}\end{{array}}')
        else: # Standard notation
            rounding_type = col1.radio('Type of rounding', ['Decimals', 'Sig figs'], horizontal=True)
            decimals = col2.number_input('# Decimales', -10, 10, 5)
            result_value = f'{result_object.value:.{decimals}f}' if decimals >= 0 else int(round(result_object.value, ndigits=decimals))
            length_str = len(str(result_value))
            rounding_text = f'{decimals} decimals' if rounding_type == 'Decimals' and decimals >= 0 else f'{length_str + decimals} Sig figs' if decimals <= 0 else f'{length_str - 1} Sig figs'
            st_output = fr'${unknown_value} = {result_value}\ {result_object.unit}$'
            answer = sc_notation_str_to_latex(fr'\begin{{array}}{{l}}\textit{{The final answer (rounded to}}\\\textit{{{rounding_text}) is}}:\\\\{unknown_value}={result_value}\ {result_object.unit}\end{{array}}')
        return st_output, answer
    except AttributeError:
        st.error("The result_object is missing the required attributes 'value' or 'unit'.")
        return "", ""


# --------------------------- COPILOT MAIN FUNCTION---------------------------------------------

def front_interface(concept_class):
    display_concept_phase(concept_class)
    variables_list, unknown_value = gather_inputs(concept_class)
    if unknown_value != 'Choose a variable':
        process_and_display_results(concept_class, variables_list, unknown_value)

def display_concept_phase(concept_class):
    concept = concept_class.concept_phase_text()
    st.subheader(concept['subheader'], divider='red')
    for text in concept['concept']:
        st.code(text)

def gather_inputs(concept_class):
    st.subheader('**_Variable Inputs_**', divider='red')
    variables_list = concept_class.variables_list()
    unknown_value = unknown_value_selection(concept_class.str_name, variables_list)
    return variables_list, unknown_value

def process_and_display_results(concept_class, variables_list, unknown_value):
    
    input_objects_list, latex_input_list = concept_class.concept_constructor(variables_list, unknown_value)
    concept_object = concept_class(*input_objects_list)
    
    check_given(latex_input_list)
    result_object = concept_object.calcular(unknown_value)
    incomplete_inputs = type(result_object) == str
    st.warning(result_object) if incomplete_inputs else None

    if not incomplete_inputs:
        display_step_by_step(concept_class, concept_object, unknown_value, result_object, latex_input_list)
        display_final_answer(unknown_value, result_object)

def display_step_by_step(concept_class, concept_object, unknown_value, result_object, latex_input_list):
    if st.checkbox(f'Cálculo de "{unknown_value}" paso a paso'):
        display_step_by_step_header(result_object)
        col1, col2, col3= st.columns(3)
        with col1:
            display_given_data(latex_input_list)
        with col2:
            if unknown_value in concept_object.despeje_strings:
                display_despeje(concept_object, unknown_value)
        with col3:
            display_calculation(concept_object, unknown_value, result_object)
        if st.checkbox('Convertir'):
            display_conversion(result_object)

def display_step_by_step_header(result_object):
    st.subheader('**_Step-by-Step_**', divider='red')
    st.success(sc_notation_str_to_latex(fr'${result_object.value}\ {result_object.unit}$'))

def display_given_data(latex_input_list):
    data_output = data_given(latex_input_list)
    st.write('**Given**')
    st.latex(data_output)
    st.code(data_output)

def display_despeje(concept_object, unknown_value):
    despeje = concept_object.despeje(unknown_value)
    st.write('**Despeje**')
    st.latex(despeje)
    st.code(despeje)

def display_calculation(concept_object, unknown_value, result_object):
    st.write('**Sustitucion y Cálculo**')
    decimals = st.number_input('# Decimales', -5, 15, 5)
    calculation = concept_object.calc_steps(unknown_value, result_object, decimals)
    calculation = sc_notation_str_to_latex(calculation)
    st.latex(calculation)
    st.code(calculation)

def display_conversion(result_object):
    col1, col2= st.columns(2)
    unit_out = col1.selectbox('Unit out', result_object.units_list())
    decimals = col2.number_input('# Decimales', -6, 15, 5)
    conversion_steps = result_object.latex_convert(unit_out, decimals)
    conversion_steps = sc_notation_str_to_latex(conversion_steps)
    result_object = result_object.convert(unit_out, decimals)
    st.latex(conversion_steps)
    st.code(conversion_steps)



def display_final_answer(unknown_value, result_object):
    st_output, answer = final_answer(unknown_value, result_object)
    col1, col2, col3 = st.columns(3)
    col1.success(st_output)
    col2.latex(answer)
    col3.code(answer,wrap_lines=True)    