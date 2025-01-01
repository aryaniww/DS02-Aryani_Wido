import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# -----------------------------
pg = st.navigation([st.Page("coba_insert_streamlit.py", title="Home"),
                    st.Page("file-4-model/UAS_DS02_Aryani.py", title="Docs")]) 
# -----------------------------
water_data = pd.read_csv('water_potability.csv')
wd = water_data.fillna(water_data.mean())
data = wd
X = data[["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]]
y = data["Potability"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)
model = RandomForestClassifier(random_state=42)
# -----------------------------

model.fit(X_train, y_train)
pg = st.navigation([st.Page("coba_insert_streamlit.py", title="Home"),
                    st.Page("file-4-model/UAS_DS02_Aryani.py", title="Docs")]) 

st.title("Prediksi Potabilitas Air Menggunakan Decision Tree")
st.write("Masukkan data air secara manual untuk memprediksi apakah air tersebut layak untuk diminum.")

ph = st.number_input("pH (keasaman air):", min_value=0.0, max_value=14.0, step=0.1)
hardness = st.number_input("Hardness (kadar kekerasan air, mg/L):", min_value=0.0)
solids = st.number_input("Solids (jumlah padatan terlarut, mg/L):", min_value=0.0)
chloramines = st.number_input("Chloramines (kadar kloramin, mg/L):", min_value=0.0)
sulfate = st.number_input("Sulfate (kadar sulfat, mg/L):", min_value=0.0)
conductivity = st.number_input("Conductivity (konduktivitas, µS/cm):", min_value=0.0)
organic_carbon = st.number_input("Organic Carbon (karbon organik, mg/L):", min_value=0.0)
trihalomethanes = st.number_input("Trihalomethanes (kadar trihalomethanes, µg/L):", min_value=0.0)
turbidity = st.number_input("Turbidity (kekeruhan, NTU):", min_value=0.0)

# if st.button("Prediksi Potabilitas"):
#     input_data = np.array([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])
#     prediction = model.predict(input_data)
#     if prediction[0] == 1:
#         st.success("Hasil prediksi: Air ini layak untuk diminum.")
#     else:
#         st.error("Hasil prediksi: Air ini tidak layak untuk diminum.")

if st.button("Prediksi Potabilitas"):
    input_data = np.array([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.success("Hasil prediksi: Air ini layak untuk diminum.")
    elif prediction[0] == 0:
        st.error("Hasil prediksi: Air ini tidak layak untuk diminum.")
    else:
        st.warning("Hasil prediksi: Status air tidak dapat dipastikan. Pastikan input data dengan benar")
