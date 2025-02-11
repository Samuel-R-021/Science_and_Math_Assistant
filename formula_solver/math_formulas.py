import streamlit as st
from sympy import *
import re


def the_quadratic_formula():

    if eq_input := st.text_input('enter quadratic polynomial', ''):
        eq_input = sympify(eq_input)
        a = eq_input.coeff('x', 2)
        b = eq_input.coeff('x', 1)
        c = eq_input.coeff('x', 0)

        st.success(a)
        st.success(b)
        st.success(c)

        w = fr"""\begin{{array}}{{l}}We\ have:\ {latex(eq_input)}\\
        \\that\ compared\ to:\ ax^2+bx+c\\\
        \\we\ get\ that:\\
        \\a={a},\ b={b},\ c={c}
        \end{{array}}
        """
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
        \\x=\frac{{-({b})\pm \sqrt{{({b})^2-[4({a})({c})]}} }}{{2({a})}}\\
        \\x=\frac{{{-b}\pm \sqrt{{ {b ** 2}-({4 * a * c}) }} }}{{ {2 * a} }}\\
        \\x=\frac{{{-b}\pm \sqrt{{ {b ** 2 - 4 * a * c} }} }}{{ {2 * a} }}
        \end{{array}}
        """

        st.latex(x)
        st.code(x)
        det = b ** 2 - 4 * a * c
        if det >= 0:
            evaluated_root= latex(sqrt(det, evaluate=True))
            y = fr"""\begin{{array}}{{l}}x=\frac{{{-b}\pm {evaluated_root} }} {{ {2 * a} }}\\\
            \\x=\frac{{{-b}+ {evaluated_root} }} {{ {2 * a} }}\ \ or\ \ x=\frac{{{-b}- {evaluated_root} }} {{ {2 * a} }}
            \end{{array}}
            """
        else:
            y = fr"""\begin{{array}}{{l}}\textit{{Next, we rewrite the square root, this way:}}
            \\x=\frac{{{-b}\pm \sqrt{{ {-(b ** 2 - 4 * a * c)} \times (-1)}} }}{{ {2 * a} }}\\
            \\x=\frac{{{-b}\pm \sqrt{{ {-(b ** 2 - 4 * a * c)} }}\sqrt{{-1}} }}{{ {2 * a} }}\\
            \\x=\frac{{{-b}\pm \sqrt{{ {-(b ** 2 - 4 * a * c)} }}i }}{{ {2 * a} }}\ \ \ \ (since:\ \sqrt{{-1}}=i) \\
            \end{{array}}
            """

        st.latex(y)
        st.code(y)