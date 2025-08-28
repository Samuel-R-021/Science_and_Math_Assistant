import streamlit as st

st.title('_Science and Math Assistant_')

# ---------------------- CODE FOR TESTING ------------------------

from test import Permutation, Combination




# Example usage
st.title("Combinations and Permutations Calculator")

col1, col2 = st.columns(2)

n = col1.number_input("Enter n value:", min_value=1)
r = col2.number_input("Enter r value:", min_value=0, max_value=n)

perm = Permutation(n, r)
perm.display()

comb = Combination(n, r)
comb.display()