# -*- coding: utf-8 -*-
"""UAS_bengkod.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14f0HVdUzFYWDg-k6S9g2NbHQfh7pKM4u

Aryani Wido Werdani A11.2023.15476

---

## 1. Pengumpulan Data
"""

# %%writefile app.py

# ! wget -q -O - ipv4.icanhazip.com

# ! streamlit run app.py & npx localtunnel --port 8501

# !pip install -q streamlit

# pip show streamlit

# pip install scikit-learn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
import streamlit as st


pg = st.navigation([st.Page("coba_insert_streamlit.py", title="Home"),
                    st.Page("UAS_DS02_Aryani.py", title="Docs")]) 

# from google.colab import drive
# drive.mount('/content/drive')
# water_data = pd.read_csv('/content/drive/MyDrive/water_potability.csv')
water_data = pd.read_csv('water_potability.csv')
st.write(water_data.head())

"""## 2. Menelaah Data
(tampil jumlah baris, tipe data tiap kolom dan nilai unik)
________________________________________________
"""
# st.write(water_data.info())
water_data.info()

# Unique Data
st.write(water_data.info())
st.write(water_data.nunique())

"""## 3. Validasi dan Visualisasi Data
________________________________________________

- Cek Missing Value
"""

# Missing data
st.write(water_data.isnull().sum())
water_data.isnull().sum()

# """- Isi missing value dengan teknik mean"""

wd = water_data.fillna(water_data.mean())
missing = wd.isnull().sum()

"""- Cek Data Outliner"""

# # Data Outliner
# Q1 = wd.quantile(0.25)
# Q3 = wd.quantile(0.75)
# IQR = Q3 - Q1
# lower_bound = Q1 - 1.5 * IQR
# upper_bound = Q3 + 1.5 * IQR
# outlier = ((wd < lower_bound) | (wd > upper_bound)).sum()
# outlier

# Data Outliner
Q1 = wd.quantile(0.25)
Q3 = wd.quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outlier = (wd < lower_bound) | (wd > upper_bound)
outlier.sum()
st.write(outlier.sum())

# """- Isi data outliner"""

# Ganti nilai outliers dengan rata-rata (hanya untuk kolom numerik)
wd = wd.apply(lambda x: np.where((x < lower_bound[x.name]) | (x > upper_bound[x.name]), x.mean(), x)
              if x.name in lower_bound.index else x)

# Cek apakah ada outliers yang tersisa
outlier = ((wd < lower_bound) | (wd > upper_bound)).sum()

st.write("=> Missing Value setelah dibersihkan: \n",missing)
st.write("\n=> Data Outliner setelah dibersihkan: \n",outlier)

"""- Visualisasi distribusi data sebelum"""

# Cek data sample setelah sampling
cek_pota = wd['Potability']
cek_pota.value_counts()
st.write(cek_pota.value_counts())

plt.figure(figsize=(6, 4))
sns.countplot(x='Potability', data=wd)
plt.title("Distribution of Potability After Resampling")
plt.show()
st.pyplot()

"""- Visualisasi distribusi data setelah resampling

"""

ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(
    wd.drop('Potability', axis=1),
    wd['Potability'])

re_data = pd.DataFrame(X_resampled, columns=wd.drop('Potability', axis=1).columns)
re_data['Potability'] = y_resampled

# Cek data sample setelah sampling
y_resampled.value_counts()
st.write(y_resampled.value_counts())
# resampled_data['Potability'].value_counts()

plt.figure(figsize=(6, 4))
sns.countplot(x='Potability', data=re_data)
plt.title("Distribution of Potability After Resampling")
plt.show()
st.pyplot()

"""## 4. Menentukan Objek Data
________________________________________
(target data adalah potability)
"""

X = X_resampled
y = y_resampled

"""## 5. Membersihkan Data

- Visualisasi Korelasi Heatmap
"""

plt.figure(figsize=(10,5))
sns.heatmap(X.corr(), annot=True, cmap='coolwarm')
plt.title('Korelasi dengan Heatmap')
plt.show()
st.pyplot()

df = re_data
potable_data = df[df['Potability'] == 1]
non_potable_data = df[df['Potability'] == 0]

# Get the list of numerical features (attributes) for plotting
numerical_features = df.select_dtypes(include=['number']).columns.tolist()
numerical_features.remove('Potability')  # Remove 'Potability' as it's the target variable

fig, axes = plt.subplots(3, 3, figsize=(12, 8))
axes = axes.flatten()

for i, feature in enumerate(numerical_features):
    ax = axes[i]

    sns.kdeplot(non_potable_data[feature], ax=ax, label='Not Potable', color='blue', fill=False)
    sns.histplot(potable_data[feature], ax=ax, label='Potable', color='skyblue', stat="density", bins=20)

    ax.set_title(f'Distribution of {feature}')
    ax.set_xlabel(feature)
    ax.set_ylabel('Frekuensi')
    ax.legend()

# Hide any unused subplots (if there are fewer than 9 numerical features)
for j in range(len(numerical_features), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
st.pyplot(fig)

"""## 6. Kontruksi Data
(menyesuaikan semua tipe data)

***tidak diperlukan karena tipe data sudah sama yaitu float***
"""

df.dtypes
# st.write(df.dtypes)

"""## 7. Pemodelan
(min 3 klasifikasi)
"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)
(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

scaler = StandardScaler()
X_train_norm = scaler.fit_transform(X_train)
X_test_norm = LabelEncoder().fit_transform(y)

"""confussion matrix"""

# models = {
#     'Decision Tree': DecisionTreeClassifier(random_state=42),
#     'Random Forest': RandomForestClassifier(random_state=42),
#     'C4.5 (Decision Tree with Entropy)': DecisionTreeClassifier(criterion='entropy', random_state=42),
#     'XGBoost': XGBClassifier(random_state=42)
# }

# # Train and evaluate models
# results = {}
# for model_name, model in models.items():
#     # Train the model
#     model.fit(X_train, y_train)

#     # Predict on test data
#     y_pred = model.predict(X_test)

#     # Evaluate the model
#     accuracy = accuracy_score(y_test, y_pred)
#     cm = confusion_matrix(y_test, y_pred)

#     # Store results
#     results[model_name] = {
#         'accuracy': accuracy,
#         'confusion_matrix': cm
#     }

#     # Display results
#     print(f"{model_name} Accuracy: {accuracy:.2f}")
#     sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Potable', 'Potable'],
#                 yticklabels=['Non-Potable', 'Potable'])
#     fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Layout grid 2x2
#     axes = axes.flatten()
#     plt.title(f"Confusion Matrix for {model_name}")
#     plt.xlabel('Predicted')
#     plt.ylabel('Actual')
#     plt.show()

models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'C4.5 (Decision Tree with Entropy)': DecisionTreeClassifier(criterion='entropy', random_state=42),
    'XGBoost': XGBClassifier(random_state=42)
}

# Train and evaluate models
results = {}
fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Layout grid 2x2
axes = axes.ravel()  # Flatten array untuk iterasi

for i, (model_name, model) in enumerate(models.items()):
    # Train the model
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    # Store results
    results[model_name] = {
        'accuracy': accuracy,
        'confusion_matrix': cm
    }

    # Plot confusion matrix
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Potable', 'Potable'],
                yticklabels=['Non-Potable', 'Potable'], ax=axes[i])
    axes[i].set_title(f"{model_name} (Acc: {accuracy:.2f})")
    axes[i].set_xlabel('Predicted')
    axes[i].set_ylabel('Actual')

# Adjust layout
plt.tight_layout()
plt.show()
st.pyplot()

print("=> Hasil Akhir Akurasi Seluruh Model:")
for model_name, result in results.items():
    st.write(f"{model_name}:= {result['accuracy']*100:.2f}%")
