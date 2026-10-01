# SolarCast

## Sistem Peramalan Produksi Energi Panel Surya Berbasis Web

SolarCast adalah aplikasi berbasis web yang digunakan untuk memperkirakan **daya AC yang dihasilkan panel surya** berdasarkan kondisi lingkungan. Sistem menggunakan model **Linear Regression** dan **Random Forest** yang dilatih menggunakan data pembangkitan panel surya dan data cuaca.

Project ini dibuat sebagai tugas mata kuliah **Rekayasa Perangkat Lunak (RPL)** oleh **Kelompok 7**.

---

## Identitas Project

| Keterangan      | Detail                                        |
| --------------- | --------------------------------------------- |
| Nama Project    | SolarCast                                     |
| Mata Kuliah     | Rekayasa Perangkat Lunak                      |
| Universitas     | Universitas Halu Oleo                         |
| Fakultas        | Fakultas Matematika dan Ilmu Pengetahuan Alam |
| Program Studi   | Ilmu Komputer                                 |
| Kelompok        | 7                                             |
| Teknologi Utama | Python, Flask, HTML, CSS, JavaScript          |
| Model           | Linear Regression & Random Forest             |

---

## Anggota Kelompok

1. **Muh. Azriel Fabian** — F1G125064
2. **Intan Aulia Zalzabila** — F1G125008
3. **Fitria Rizki Oktavia** — F1G125006

---

## Latar Belakang

Energi matahari merupakan salah satu sumber energi terbarukan yang dapat dimanfaatkan melalui panel surya. Jumlah daya yang dihasilkan panel surya dapat berubah berdasarkan kondisi lingkungan seperti suhu dan intensitas radiasi matahari.

Oleh karena itu, diperlukan suatu sistem yang dapat membantu memperkirakan daya yang dihasilkan berdasarkan kondisi tersebut.

SolarCast dibuat sebagai aplikasi sederhana yang menggabungkan pengembangan perangkat lunak berbasis web dengan model pembelajaran mesin untuk menghasilkan perkiraan daya panel surya.

---

## Tujuan

SolarCast memiliki beberapa tujuan, yaitu:

* Membuat aplikasi web untuk memperkirakan daya panel surya.
* Menggunakan data kondisi lingkungan sebagai input prediksi.
* Menerapkan Linear Regression dan Random Forest.
* Membandingkan hasil dari kedua model.
* Menampilkan hasil prediksi melalui antarmuka web yang mudah digunakan.

---

## Fitur

SolarCast menyediakan beberapa fitur utama:

* **Prediksi daya panel surya**
* Input suhu lingkungan
* Input suhu modul panel
* Input iradiasi matahari
* **Gunakan Kondisi Saat Ini**
* Perhitungan menggunakan model Random Forest
* Status hasil pembangkitan
* Riwayat prediksi
* Tampilan web responsif
* Penyimpanan riwayat menggunakan SQLite

---

## Input Prediksi

Sistem menggunakan tiga fitur utama:

| Fitur               | Keterangan                  |
| ------------------- | --------------------------- |
| Ambient Temperature | Suhu lingkungan             |
| Module Temperature  | Suhu modul panel            |
| Irradiation         | Intensitas radiasi matahari |

Target prediksi yang digunakan adalah:

**AC Power**

Hasil prediksi ditampilkan dalam satuan **Watt (W)**.

---

## Dataset

Dataset yang digunakan berasal dari **Solar Power Generation Data** dan **Solar Power Plant Weather Sensor Data**.

Data yang digunakan dalam project berasal dari **Plant 1**.

Dataset terdiri dari data pembangkitan panel surya dan data sensor cuaca yang kemudian digabungkan berdasarkan `DATE_TIME`.

Fitur yang digunakan:

```text
AMBIENT_TEMPERATURE
MODULE_TEMPERATURE
IRRADIATION
```

Target:

```text
AC_POWER
```

---

## Model Machine Learning

Dua model digunakan dalam proses pengembangan:

### 1. Linear Regression

Linear Regression digunakan sebagai salah satu model untuk memperkirakan hubungan antara kondisi lingkungan dengan daya AC yang dihasilkan.

### 2. Random Forest

Random Forest digunakan sebagai model utama pada aplikasi karena memberikan hasil evaluasi yang lebih baik pada pengujian project.

Hasil pengujian:

| Model             |   MAE |  RMSE |     R² |
| ----------------- | ----: | ----: | -----: |
| Linear Regression | 26.31 | 55.51 | 0.9800 |
| Random Forest     | 16.37 | 45.67 | 0.9865 |

Berdasarkan hasil pengujian pada dataset yang digunakan, Random Forest memperoleh nilai MAE dan RMSE yang lebih rendah serta nilai R² yang lebih tinggi dibandingkan Linear Regression.

---

## Alur Sistem

```text
Data Sensor / Input Pengguna
            ↓
   Suhu Lingkungan
   Suhu Modul Panel
   Iradiasi Matahari
            ↓
      Model Random Forest
            ↓
       Hasil Prediksi
            ↓
      Perkiraan AC Power
            ↓
       Status Pembangkitan
```

---

## Teknologi yang Digunakan

### Backend

* Python
* Flask

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

### Frontend

* HTML
* CSS
* JavaScript
* Font Awesome

### Database

* SQLite

### Development

* Visual Studio Code
* Git
* GitHub

---

## Struktur Project

```text
SolarCast/
│
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── model/
│   └── random_forest_model.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   └── img/
│       └── logo-uho.png
│
└── .gitignore
```

---

## Cara Menjalankan Project

### 1. Clone Repository

```bash
git clone https://github.com/elwaa27/SolarCast.git
```

Masuk ke folder project:

```bash
cd SolarCast
```

### 2. Buat Virtual Environment

Windows:

```bash
python -m venv venv
```

Aktifkan:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python app.py
```

Kemudian buka:

```text
http://127.0.0.1:5000
```

---

## Cara Kerja Prediksi

Pengguna memasukkan:

1. Suhu lingkungan
2. Suhu modul panel
3. Iradiasi matahari

Sistem kemudian memproses data tersebut menggunakan model Random Forest yang telah dilatih.

Jika nilai iradiasi tidak tersedia atau bernilai nol, sistem menganggap tidak terdapat pembangkitan daya pada kondisi tersebut.

Hasil prediksi kemudian ditampilkan dalam satuan Watt dan disimpan ke dalam riwayat prediksi.

---

## Kondisi Saat Ini

SolarCast menyediakan fitur **Gunakan Kondisi Saat Ini** yang mengambil kondisi cuaca terkini untuk membantu mengisi nilai suhu lingkungan dan iradiasi.

Nilai suhu modul kemudian diperkirakan berdasarkan kondisi lingkungan dan iradiasi sebelum digunakan oleh model prediksi.

---

## Tujuan Pengembangan

Project ini dikembangkan sebagai implementasi sederhana penerapan teknologi perangkat lunak dan pembelajaran mesin pada bidang energi terbarukan.

SolarCast juga berkaitan dengan upaya pemanfaatan teknologi untuk mendukung penggunaan energi bersih dan terjangkau.

---

## Status Project

**Status:** Selesai dikembangkan untuk kebutuhan tugas mata kuliah RPL.

Project masih dapat dikembangkan lebih lanjut, misalnya dengan:

* penggunaan database online,
* penyimpanan data yang lebih permanen,
* integrasi sensor panel surya secara langsung,
* peningkatan model prediksi,
* dan deployment pada server produksi.

---

## Repository

**GitHub:**
https://github.com/elwaa27/SolarCast

---

## Lisensi

Project ini dibuat untuk keperluan akademik pada mata kuliah **Rekayasa Perangkat Lunak, Universitas Halu Oleo**.
