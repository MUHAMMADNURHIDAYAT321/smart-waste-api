
# Smart Waste Monitoring API

Smart Waste Monitoring API merupakan REST API berbasis
Internet of Things (IoT) untuk pemantauan tempat sampah
pintar menggunakan data sensor simulasi.

## Teknologi

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- MVC
- Postman
- Pytest

## Fitur Utama

- CRUD pengguna
- CRUD perangkat IoT
- CRUD sensor
- CRUD telemetri
- CRUD peringatan
- Search, filter, sorting, dan pagination
- Validasi input
- Automated testing

## Instalasi

Membuat virtual environment:

```bash
python -m venv venv
```

Mengaktifkan virtual environment pada Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Menginstal dependency:

```bash
python -m pip install -r requirements.txt
```

## Inisialisasi Database

```bash
python seed.py
```

## Menjalankan Aplikasi

```bash
python app.py
```

Base URL:

http://127.0.0.1:5000

## Endpoint API

| Resource | Endpoint |
|---|---|
| Users | /api/users |
| Devices | /api/devices |
| Sensors | /api/sensors |
| Telemetries | /api/telemetries |
| Alerts | /api/alerts |

Setiap resource mendukung operasi GET, POST, PUT,
dan DELETE. Untuk detail, update, dan delete,
tambahkan ID pada akhir URL.

## HTTP Status Code

| Code | Keterangan |
|---|---|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Internal Server Error |

## Contoh Request

POST /api/users

```json
{
    "name": "Andi",
    "email": "andi@example.com",
    "role": "operator"
}
```

## Contoh Response

```json
{
    "success": true,
    "message": "Data berhasil ditambahkan",
    "data": {
        "id": 2,
        "name": "Andi",
        "email": "andi@example.com",
        "role": "operator"
    }
}
```

## Pengujian Postman

Import file postman_collection.json ke Postman.
Collection berisi 12 request pengujian API.

## Automated Testing

```bash
python -m pytest -v
```

Hasil pengujian: 10 passed.

## Rencana Pengembangan UAS

- Autentikasi dan otorisasi JWT.
- Integrasi perangkat ESP32.
- Dashboard monitoring IoT.
- Visualisasi data sensor.
- Notifikasi kapasitas sampah.

## Referensi

- https://flask.palletsprojects.com/
- https://flask-sqlalchemy.palletsprojects.com/
- https://docs.pytest.org/

## Penggunaan AI

ChatGPT digunakan sebagai bantuan dalam perancangan,
implementasi, pengujian, dan dokumentasi proyek.