import streamlit as st

pg = st.navigation([st.Page("Home.py", title="Home"),
                    st.Page("file-4-model/UAS_DS02_Aryani.py", title="Docs")])
# pg.run()
st.title("Welcome")
st.write("Insert your data here:")
