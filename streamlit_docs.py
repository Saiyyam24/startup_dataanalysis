import streamlit as st

st.title("My first demo")
st.header("random")
st.write("Hello, world!")
st.code('''
    def foo(x):
            return x * 2

''')
st.image("passport photo.jpg")
st.sidebar.title('side bar title')


col1,col2 = st.columns(2)
with col1:
    st.write("Hello, world!")
with col2:
    st.image("passport photo.jpg")