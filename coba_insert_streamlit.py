import streamlit as st
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# Membuat model Decision Tree
model = DecisionTreeClassifier()

# Contoh data untuk pelatihan (dapat diganti dengan dataset yang sebenarnya)
# Data terdiri dari fitur: [ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]
# Label potability: 1 (layak diminum), 0 (tidak layak diminum)
X_train = [
    [7.0, 200.0, 15000.0, 4.0, 300.0, 400.0, 10.0, 80.0, 4.0],
    [6.5, 180.0, 12000.0, 3.5, 250.0, 350.0, 9.0, 70.0, 3.5],
    [8.0, 220.0, 17000.0, 5.0, 320.0, 450.0, 11.0, 90.0, 5.0],
    [5.5, 150.0, 10000.0, 2.5, 200.0, 300.0, 8.0, 60.0, 2.5]
]
y_train = [1, 1, 0, 0]

# Melatih model
model.fit(X_train, y_train)


pg = st.navigation([st.Page("coba_insert_streamlit.py", title="Home"),
                    st.Page("file-4-model/UAS_DS02_Aryani.py", title="Docs")]) 

# Judul aplikasi
st.title("Prediksi Potabilitas Air Menggunakan Decision Tree")

# Deskripsi aplikasi
st.write("Masukkan data air secara manual untuk memprediksi apakah air tersebut layak untuk diminum.")

# Form input data
ph = st.number_input("pH (keasaman air):", min_value=0.0, max_value=14.0, step=0.1)
hardness = st.number_input("Hardness (kadar kekerasan air, mg/L):", min_value=0.0)
solids = st.number_input("Solids (jumlah padatan terlarut, mg/L):", min_value=0.0)
chloramines = st.number_input("Chloramines (kadar kloramin, mg/L):", min_value=0.0)
sulfate = st.number_input("Sulfate (kadar sulfat, mg/L):", min_value=0.0)
conductivity = st.number_input("Conductivity (konduktivitas, µS/cm):", min_value=0.0)
organic_carbon = st.number_input("Organic Carbon (karbon organik, mg/L):", min_value=0.0)
trihalomethanes = st.number_input("Trihalomethanes (kadar trihalomethanes, µg/L):", min_value=0.0)
turbidity = st.number_input("Turbidity (kekeruhan, NTU):", min_value=0.0)

# Tombol prediksi
if st.button("Prediksi Potabilitas"):
    # Data yang dimasukkan pengguna
    input_data = np.array([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])

    # Prediksi menggunakan model
    prediction = model.predict(input_data)

    # Menampilkan hasil prediksi
    if prediction[0] == 1:
        st.success("Hasil prediksi: Air ini layak untuk diminum.")
    else:
        st.error("Hasil prediksi: Air ini tidak layak untuk diminum.")
