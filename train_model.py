import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# 1. MEMBACA DATASET
# ==========================================

generation = pd.read_csv(
    "dataset/Plant_1_Generation_Data.csv"
)

weather = pd.read_csv(
    "dataset/Plant_1_Weather_Sensor_Data.csv"
)


# ==========================================
# 2. MENGUBAH FORMAT TANGGAL
# ==========================================

generation["DATE_TIME"] = pd.to_datetime(
    generation["DATE_TIME"],
    format="%d-%m-%Y %H:%M"
)

weather["DATE_TIME"] = pd.to_datetime(
    weather["DATE_TIME"],
    format="%Y-%m-%d %H:%M:%S"
)


# ==========================================
# 3. MENGGABUNGKAN DATA
# ==========================================

data = pd.merge(
    generation,
    weather,
    on="DATE_TIME",
    how="inner"
)


# ==========================================
# 4. MEMILIH KOLOM
# ==========================================

data = data[
    [
        "DATE_TIME",
        "AC_POWER",
        "AMBIENT_TEMPERATURE",
        "MODULE_TEMPERATURE",
        "IRRADIATION"
    ]
]


# ==========================================
# 5. MEMBERSIHKAN DATA
# ==========================================

data = data.dropna()


# ==========================================
# 6. MENENTUKAN FITUR DAN TARGET
# ==========================================

X = data[
    [
        "AMBIENT_TEMPERATURE",
        "MODULE_TEMPERATURE",
        "IRRADIATION"
    ]
]

y = data["AC_POWER"]


# ==========================================
# 7. MEMBAGI DATA TRAINING DAN TESTING
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("=== HASIL PEMBAGIAN DATA ===")
print("Data keseluruhan :", len(data))
print("Data training    :", len(X_train))
print("Data testing     :", len(X_test))
print("Jumlah fitur     :", X_train.shape[1])


# ==========================================
# 8. LINEAR REGRESSION
# ==========================================

model_lr = LinearRegression()

model_lr.fit(X_train, y_train)

y_pred_lr = model_lr.predict(X_test)


# Evaluasi Linear Regression
mae_lr = mean_absolute_error(y_test, y_pred_lr)

rmse_lr = np.sqrt(
    mean_squared_error(y_test, y_pred_lr)
)

r2_lr = r2_score(
    y_test,
    y_pred_lr
)


print("\n=== HASIL LINEAR REGRESSION ===")
print("MAE  :", mae_lr)
print("RMSE :", rmse_lr)
print("R2   :", r2_lr)


# ==========================================
# 9. RANDOM FOREST
# ==========================================

model_rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model_rf.fit(X_train, y_train)

y_pred_rf = model_rf.predict(X_test)


# Evaluasi Random Forest
mae_rf = mean_absolute_error(
    y_test,
    y_pred_rf
)

rmse_rf = np.sqrt(
    mean_squared_error(y_test, y_pred_rf)
)

r2_rf = r2_score(
    y_test,
    y_pred_rf
)


print("\n=== HASIL RANDOM FOREST ===")
print("MAE  :", mae_rf)
print("RMSE :", rmse_rf)
print("R2   :", r2_rf)

import os
import joblib

# Membuat folder model jika belum ada
os.makedirs("model", exist_ok=True)

# Menyimpan model Random Forest
joblib.dump(
    model_rf,
    "model/random_forest_model.pkl"
)

print("\n=== MODEL BERHASIL DISIMPAN ===")
print("Lokasi: model/random_forest_model.pkl")