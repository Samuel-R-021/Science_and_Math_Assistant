import streamlit as st
from sympy import *
import re


def the_quadratic_formula():

    if not (eq_input := st.text_input('enter quadratic polynomial', '')):
        return
    eq_input = sympify(eq_input)
    a = eq_input.coeff('x', 2)
    b = eq_input.coeff('x', 1)
    c = eq_input.coeff('x', 0)

    col1, col2, col3 = st.columns(3)

    col1.success(f'a = {a}')
    col2.success(f'b = {b}')
    col3.success(f'c = {c}')

    w = fr"""\begin{{array}}{{l}}Comparing:\\
            \\ {latex(eq_input)}\\
            \\to\ \ \ ax^2+bx+c\\
            \\we\ get\ that:\\
            \\a={a},\ b={b},\ c={c}
            \end{{array}}
            """
    st.latex(w)
    st.code(w)

    x = fr"""\begin{{array}}{{l}}x=\frac{{-b\pm \sqrt{{b^2-4ac}}}}{{2a}}\\
    \\x=\frac{{-({b})\pm \sqrt{{({b})^2-4\cdot({a})\cdot({c})}} }}{{2({a})}}\\
    \\x=\frac{{{-b}\pm \sqrt{{ {b ** 2}-({4 * a * c}) }} }}{{ {2 * a} }}\\
    \\x=\frac{{{-b}\pm \sqrt{{ {b ** 2 - 4 * a * c} }} }}{{ {2 * a} }}
    \end{{array}}
    """

    st.latex(x)
    st.code(x)

    det = b ** 2 - 4 * a * c
    if det > 0:
        evaluated_root= sqrt(det, evaluate=True)
        y = fr"""\begin{{array}}{{l}}x=\frac{{{-b}\pm {latex(evaluated_root)} }} {{ {2 * a} }}\\\
        \\x=\frac{{{-b}}} {{ {2 * a} }}+ \frac{{{latex(evaluated_root)} }}{{ {2 * a} }}\ \ or\ \ x=\frac{{{-b}}} {{ {2 * a} }}- \frac{{{latex(evaluated_root)} }}{{ {2 * a} }}\\
        \\x={latex(-b/(2 * a))}+ {latex(evaluated_root/(2*a))}\ \ or\ \ x={latex(-b/(2 * a))}-{latex(evaluated_root/(2*a))}\\
        \\x={latex(-b/(2 * a) + evaluated_root/(2*a))}\ \ or\ \ x={latex(-b/(2 * a) - evaluated_root/(2*a))}
        \end{{array}}
        """
        answer = fr"""\begin{{array}}{{l}}Final\ answer:\\\
        \\x={latex(-b/(2 * a) + evaluated_root/(2*a))}\ \ or\ \ x={latex(-b/(2 * a) - evaluated_root/(2*a))}
        \end{{array}}
        """
    elif det == 0:
        y = fr"""\begin{{array}}{{l}}x=\frac{{{-b}\pm 0}} {{ {2 * a} }}\\\
        \\x=\frac{{{-b}}} {{ {2 * a} }}
        \\\\x={latex(-b/(2*a))}
        \end{{array}}
        """
        answer = fr"""\begin{{array}}{{l}}Final\ answer:\\\
        \\x={latex(-b/(2*a))}
        \end{{array}}
        """
    else:
        complex_root= sqrt(det, evaluate=True)

        y = fr"""\begin{{array}}{{l}}\textit{{Next, we rewrite the square root, this way:}}\\
        \\x=\frac{{{-b}\pm \sqrt{{ {-(b ** 2 - 4 * a * c)} \times (-1)}} }}{{ {2 * a} }}=\frac{{{-b}\pm \sqrt{{ {-(b ** 2 - 4 * a * c)} }}\times\sqrt{{-1}} }}{{ {2 * a} }}\\
        \\x=\frac{{{-b}\pm \sqrt{{ {-(b ** 2 - 4 * a * c)} }}i }}{{ {2 * a} }}\ \ \ \ (since:\ \sqrt{{-1}}=i) \\
        \\x=\frac{{{-b}\pm {latex(complex_root)}}}{{ {2 * a} }}\\
        \\x=\frac{{{-b}}} {{ {2 * a} }}+ \frac{{{latex(complex_root)} }}{{ {2 * a} }}\ \ or\ \ x=\frac{{{-b}}} {{ {2 * a} }}- \frac{{{latex(complex_root)} }}{{ {2 * a} }}\\
        \\x={latex(-b/(2 * a))}+ {latex(complex_root/(2*a))}\ \ or\ \ x={latex(-b/(2 * a))}-{latex(complex_root/(2*a))}
        \end{{array}}
        """
        answer = fr"""\begin{{array}}{{l}}Final\ answer:\\\
        \\x={latex(-b/(2 * a))}+ {latex(complex_root/(2*a))}\ \ or\ \ x={latex(-b/(2 * a))}-{latex(complex_root/(2*a))}
        \end{{array}}
        """

    st.latex(y)
    st.code(y)

    st.latex(answer)
    st.code(answer)