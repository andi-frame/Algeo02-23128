# Algeo 2 - 23128

Jadi, dalam src ada dua folder, frontend dan backend

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
