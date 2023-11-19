import streamlit as st
import pandas as pd

age = st.number_input('Enter your age', 0, 100, 25)
st.write('Your age is: ', age)
salary = st.slider('Enter your desired monthly salary in k$', 0, 100, 50)
st.write("Your desired monthly salary is: {0} k{2} which represents {1} 000 dollars per year".format(salary, salary*12,"$"))
st.write("Here are the selected jobs that match your desired salary +/- 10%")
df = pd.read_csv('/data/salaries.csv')
df_perso = df.loc[(df['salary']>=salary*1000*12*0.9) & (df['salary']<=salary*1000*12*1.1),['job_title','salary']]
df_print = df_perso.groupby('job_title')['salary'].mean().reset_index().sort_values(by='salary',ascending=False).reset_index(drop=True)
st.dataframe(df_print.rename({'salary':'Average annual salary'},axis=1))