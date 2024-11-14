import streamlit as st

st.write("Hello world")
name = st.text_input("Your name", key="name")
age = st.number_input("Your age", key="age", min_value = 0.0, step = 0.5)
taille = st.number_input("Your taille", key="taille", min_value = 0.00)
if st.button("Submit"):
    st.write("Name Input: ",name)
    st.write("Age Input: ", age)
    st.write("Taille Input",taille)
    print(name)
