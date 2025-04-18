# WhatsApp Financial Planner Bot

Sebuah bot WhatsApp untuk perencanaan keuangan pribadi dengan dashboard real-time. Bot ini membantu Anda mencatat dan menganalisis keuangan menggunakan bahasa Indonesia.

## Fitur

- 💬 Integrasi dengan WhatsApp
- 💰 Pencatatan pemasukan dan pengeluaran
- 📊 Dashboard real-time untuk monitoring keuangan
- 📈 Analisis dan laporan keuangan
- 🎯 Perencanaan dan tracking budget
- 🔔 Notifikasi dan pengingat
- 📱 Responsive web interface

## Teknologi

- Python 3.8+
- FastAPI
- SQLAlchemy
- WebSocket
- TailwindCSS
- Chart.js

## Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/yourusername/financial-wa-bot.git
cd financial-wa-bot
```

2. Buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Buat file `.env` di root directory:
```env
DATABASE_URL=sqlite:///database/financial_bot.db
WEB_HOST=0.0.0.0
WEB_PORT=8000
DEBUG_MODE=True
SECRET_KEY=your-secret-key-here
```

5. Inisialisasi database:
```bash
python -c "from database.db_manager import db_manager; db_manager.init_db()"
```

## Penggunaan

1. Jalankan aplikasi:
```bash
python main.py
```

2. Scan QR code WhatsApp yang muncul untuk menghubungkan dengan WhatsApp Web

3. Akses dashboard di `http://localhost:8000`

### Perintah WhatsApp

Bot memahami perintah dalam bahasa Indonesia (formal dan informal):

1. Catat Pengeluaran:
   ```
   catat pengeluaran 50000 untuk makan
   keluar 50k buat makan
   ```

2. Catat Pemasukan:
   ```
   catat pemasukan 1000000 dari gaji
   masuk 1jt dr gaji
   ```

3. Cek Saldo:
   ```
   cek saldo
   saldo
   ```

4. Lihat Laporan:
   ```
   laporan bulanan
   report
   ```

5. Atur Budget:
   ```
   atur budget 2000000 per bulan
   set budget 2jt per bln
   ```

6. Buka Dashboard:
   ```
   buka dashboard
   dashboard
   ```

## Struktur Proyek

```
financial_wa_bot/
├── config/                 # Konfigurasi aplikasi
├── core/                  # Komponen inti (WhatsApp client, message handler)
├── database/              # Model dan manager database
├── features/              # Fitur utama (financial processor)
├── dashboard/             # Frontend dashboard
│   ├── static/           # Asset statis (CSS, JS, images)
│   └── templates/        # Template HTML
├── web/                  # Backend web (FastAPI, WebSocket)
│   └── api/             # API endpoints
├── utils/                # Utility functions
├── tests/                # Unit tests
├── requirements.txt      # Dependencies
└── main.py              # Entry point
```

## API Endpoints

### Transactions
- GET `/api/v1/transactions/{user_id}` - Get user transactions
- GET `/api/v1/balance/{user_id}` - Get current balance
- GET `/api/v1/budget/{user_id}` - Get budget status
- GET `/api/v1/report/{user_id}` - Get financial report
- GET `/api/v1/insights/{user_id}` - Get financial insights
- GET `/api/v1/notifications/{user_id}` - Get notifications

## Dashboard Features

1. Overview:
   - Saldo saat ini
   - Total pemasukan & pengeluaran
   - Status budget

2. Visualisasi:
   - Grafik kategori pengeluaran
   - Tren pemasukan vs pengeluaran
   - Progress budget

3. Transaksi:
   - Daftar transaksi terakhir
   - Filter & pencarian
   - Export data

4. Analisis:
   - Laporan keuangan
   - Insight & rekomendasi
   - Prediksi pengeluaran

## Kontribusi

Silakan buat issue atau pull request untuk kontribusi.

## Lisensi

MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## Kontak

- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
