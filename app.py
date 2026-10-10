from flask import Flask, render_template, request, jsonify, redirect, url_for
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
import urllib.request
import json

app = Flask(__name__)

# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load("model/random_forest_model.pkl")


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect("solarcast.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ambient_temperature REAL NOT NULL,
            module_temperature REAL NOT NULL,
            irradiation REAL NOT NULL,
            prediction REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================================================
# STATUS PREDIKSI
# =========================================================

def get_status(prediction, irradiation):
    """
    Menentukan status berdasarkan hasil prediksi.
    """

    if irradiation <= 0:
        return {
            "label": "TIDAK ADA PEMBANGKITAN",
            "class": "no-power",
            "icon": "fa-moon",
            "description": (
                "Iradiasi matahari saat ini bernilai 0 W/m² "
                "sehingga sistem tidak memperkirakan adanya pembangkitan daya."
            )
        }

    if prediction < 500:
        return {
            "label": "RENDAH",
            "class": "low",
            "icon": "fa-arrow-down",
            "description": (
                "Perkiraan daya berada pada tingkat rendah. "
                "Kondisi matahari belum menghasilkan daya yang tinggi."
            )
        }

    if prediction < 1000:
        return {
            "label": "CUKUP",
            "class": "medium",
            "icon": "fa-minus",
            "description": (
                "Perkiraan daya berada pada tingkat cukup "
                "untuk kondisi lingkungan saat ini."
            )
        }

    return {
        "label": "BAIK",
        "class": "good",
        "icon": "fa-arrow-up",
        "description": (
            "Kondisi lingkungan mendukung pembangkitan daya "
            "panel surya dengan baik."
        )
    }


# =========================================================
# AMBIL RIWAYAT
# =========================================================

def get_history():
    conn = get_db()

    rows = conn.execute("""
        SELECT
            id,
            ambient_temperature,
            module_temperature,
            irradiation,
            prediction,
            created_at
        FROM predictions
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =========================================================
# HALAMAN UTAMA
# =========================================================

@app.route("/")
def home():
    history = get_history()
    return render_template("index.html", history=history)


@app.route("/prediksi")
def prediction_page():
    # Halaman prediksi tetap menggunakan index.html asli.
    history = get_history()
    return render_template("index.html", history=history)


@app.route("/dashboard")
def dashboard():
    # Riwayat lengkap dipakai untuk total; tabel/grafik menampilkan 10 terbaru.
    history = get_history()
    latest = history[0] if history else None
    return render_template(
        "dashboard.html",
        history=history[:10],
        latest=latest,
        total_predictions=len(history)
    )


# =========================================================
# PREDIKSI
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # -------------------------------------------------
        # Ambil data
        # -------------------------------------------------

        if request.is_json:
            data = request.get_json()

            ambient_temperature = float(
                data.get("ambient_temperature", 0)
            )

            module_temperature = float(
                data.get("module_temperature", 0)
            )

            irradiation = float(
                data.get("irradiation", 0)
            )

        else:
            ambient_temperature = float(
                request.form["ambient_temperature"]
            )

            module_temperature = float(
                request.form["module_temperature"]
            )

            irradiation = float(
                request.form["irradiation"]
            )


        # -------------------------------------------------
        # Validasi input dan batas operasional
        import math

        values = [
            ambient_temperature,
            module_temperature,
            irradiation
        ]

        if not all(math.isfinite(value) for value in values):
            raise ValueError("Semua input harus berupa angka yang valid.")

        if not 0 <= ambient_temperature <= 50:
            raise ValueError("Suhu lingkungan harus antara 0 sampai 50 ?C.")

        if not 0 <= module_temperature <= 85:
            raise ValueError("Suhu modul panel harus antara 0 sampai 85 ?C.")

        if not 0 <= irradiation <= 1.5:
            raise ValueError("Iradiasi matahari harus antara 0 sampai 1.5 kW/m?.")

        warning_messages = []

        if not 20.3985 <= ambient_temperature <= 35.2525:
            warning_messages.append("suhu lingkungan di luar rentang data pelatihan")

        if not 18.1404 <= module_temperature <= 65.5457:
            warning_messages.append("suhu modul panel di luar rentang data pelatihan")

        if irradiation > 1.2217:
            warning_messages.append("iradiasi di luar rentang data pelatihan")

        warning = ""
        if warning_messages:
            warning = (
                "Peringatan: "
                + "; ".join(warning_messages)
                + ". Hasil prediksi mungkin kurang akurat."
            )


        # Prediksi
        # -------------------------------------------------

        if irradiation <= 0:

            prediction = 0.0

        else:

            input_data = pd.DataFrame([{
                "AMBIENT_TEMPERATURE": ambient_temperature,
                "MODULE_TEMPERATURE": module_temperature,
                "IRRADIATION": irradiation
            }])

            prediction = model.predict(input_data)[0]

            # Hindari nilai negatif
            prediction = max(float(prediction), 0.0)

            prediction = round(prediction, 2)


        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        status = get_status(
            prediction,
            irradiation
        )


        # -------------------------------------------------
        # Simpan database
        # -------------------------------------------------

        created_at = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        conn = get_db()

        cursor = conn.execute("""
            INSERT INTO predictions (
                ambient_temperature,
                module_temperature,
                irradiation,
                prediction,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ambient_temperature,
            module_temperature,
            irradiation,
            prediction,
            created_at
        ))

        prediction_id = cursor.lastrowid

        conn.commit()
        conn.close()


        # -------------------------------------------------
        # Response JSON
        # -------------------------------------------------

        response_data = {
            "success": True,
            "id": prediction_id,
            "ambient_temperature": ambient_temperature,
            "module_temperature": module_temperature,
            "irradiation": irradiation,
            "prediction": prediction,
            "created_at": created_at,
            "status": status,
            "warning": warning
        }


        # AJAX / JSON
        if request.is_json or request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return jsonify(response_data)


        # Fallback jika form biasa digunakan
        return render_template(
            "index.html",
            history=get_history(),
            prediction=prediction,
            status=status
        )


    except Exception as e:

        error_message = str(e)

        if request.is_json or request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return jsonify({
                "success": False,
                "error": error_message
            }), 400

        return render_template(
            "index.html",
            history=get_history(),
            error=error_message
        )


# =========================================================
# KONDISI CUACA SAAT INI
# =========================================================

@app.route("/current-weather")
def current_weather():

    try:

        # Koordinat wilayah Kendari
        latitude = -3.9985
        longitude = 122.5129

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            "&current=temperature_2m,shortwave_radiation"
            "&timezone=Asia%2FJakarta"
        )

        request_api = urllib.request.Request(
            url,
            headers={
                "User-Agent": "SolarCast-UHO/1.0"
            }
        )

        with urllib.request.urlopen(
            request_api,
            timeout=10
        ) as response:

            weather_data = json.loads(
                response.read().decode("utf-8")
            )


        current = weather_data.get(
            "current",
            {}
        )

        ambient_temperature = current.get(
            "temperature_2m"
        )

        irradiation = current.get(
            "shortwave_radiation"
        )


        if ambient_temperature is None:
            raise ValueError(
                "Data suhu dari layanan cuaca tidak tersedia."
            )

        if irradiation is None:
            raise ValueError(
                "Data iradiasi dari layanan cuaca tidak tersedia."
            )


        ambient_temperature = float(
            ambient_temperature
        )

        irradiation = float(
            irradiation
        )


        # -------------------------------------------------
        # Perkiraan suhu modul
        # -------------------------------------------------
        #
        # Dataset tidak menyediakan sensor modul real-time.
        # Oleh karena itu suhu modul diperkirakan dari
        # suhu lingkungan dan iradiasi.
        #

        module_temperature = (
            ambient_temperature +
            (irradiation * 0.03)
        )

        module_temperature = round(
            module_temperature,
            2
        )


        # -------------------------------------------------
        # Prediksi
        # -------------------------------------------------

        if irradiation <= 0:

            prediction = 0.0

        else:

            input_data = pd.DataFrame([{
                "AMBIENT_TEMPERATURE": ambient_temperature,
                "MODULE_TEMPERATURE": module_temperature,
                "IRRADIATION": irradiation
            }])

            prediction = model.predict(
                input_data
            )[0]

            prediction = max(
                float(prediction),
                0.0
            )

            prediction = round(
                prediction,
                2
            )


        status = get_status(
            prediction,
            irradiation
        )


        return jsonify({
            "success": True,
            "ambient_temperature": round(
                ambient_temperature,
                2
            ),
            "module_temperature": module_temperature,
            "irradiation": round(
                irradiation,
                2
            ),
            "prediction": prediction,
            "status": status
        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": (
                "Kondisi saat ini belum dapat diambil. "
                + str(e)
            )
        }), 500


# =========================================================
# JALANKAN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )