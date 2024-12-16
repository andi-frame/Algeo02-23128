# Tugas besar Aljabar Linear dan Geometri 2
Tugas besar kali ini adalah membuat website yang meminta input lagu dan web tersebut mendeteksi apa nama dari lagu tersebut dan beberapa detail lainnya. Selain itu website ini menyediakan fitur Album Finder, yaitu website ini dapat meminta input gambar album dan website tersebut akan mendeteksi nama album tersebut.
## Setup frontend

Pertama masuk ke directory frontend:

```bash
cd src/frontend
```

Lalu, lakukan instalasi packages dan jalankan program frontend (pastikan telah menginstall node.js)

```bash
npm install
npm run dev
```

Program telah berjalan dan dapat diakses melalui route berikut:\
http://localhost:3000/


## Setup backend

Pertama, masuk ke directory backend:

```bash
cd src/backend
```

Lalu, lakukan insialisasi .venv

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Pastikan telah terdapat '(venv)' pada terminal.\
Selanjutnya, lakukan instalasi library dari requirements.txt

```bash
pip install -r requirements.txt
```

Selanjutnya jalankan server:

```bash
fastapi dev main.py
```

Server telah dapat berjalan pada:\
http://127.0.0.1:8000

Kemudian buka link dokumentasi otomatis berikut untuk melihat daftar API yang telah dibuat:\
http://127.0.0.1:8000/docs

## Fitur
- Image Retrieval
- Music Information Retrieval
- Store Data to Firebase Storage
- Store Data to Supabase Database

## Kontribusi
- Muhammad Aulia Azka (13523137) : Image Retrieval
- Ahmad Syafiq (13523135) : Music Information Retrieval
- Andi Farhan Hidayat (13523128) : FrontEnd, BackEnd
