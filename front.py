import streamlit as st

# I want a white background and in the middle of the page i want a form when you can enter your age


age = st.number_input('Enter your age', 0, 100, 25)
st.write('Your age is: ', age)
salary = st.slider('Enter your salary in k$', 0, 100, 50)
st.write('Your salary is: ', salary, 'k$')
