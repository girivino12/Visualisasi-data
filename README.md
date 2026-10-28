Dashboard Interaktif Teknologi Tepat Guna Perikanan Jawa Barat (Multi-DBMS)
Deskripsi Proyek
Proyek ini merupakan aplikasi web interaktif yang memvisualisasikan persebaran dan penggunaan alat teknologi tepat guna perikanan di tingkat desa/kelurahan di wilayah Provinsi Jawa Barat. Sistem ini dirancang menggunakan arsitektur Multi-DBMS Data Pipeline, yang memisahkan data master wilayah geografis dan data metrik operasional ke dalam dua sistem basis data berbeda untuk mensimulasikan praktik tata kelola data modern (Data Federation).

Ringkasan Arsitektur (Multi-DBMS)
Supabase (PostgreSQL Cloud)

Fungsi: Menyimpan data master wilayah untuk menjamin konsistensi entitas geografis secara terpusat di cloud.

Struktur: Tabel master_desa yang mencakup bps_kode_desa_kelurahan, bps_nama_desa_kelurahan, bps_nama_kecamatan, dan bps_nama_kabupaten_kota.

SQLite (Lokal Embedded)

Fungsi: Menyimpan log fakta metrik operasional perikanan yang bersifat dinamis.

Struktur: Tabel metrik_perikanan yang memuat bps_kode_desa_kelurahan, jumlah_alat_teknologi_tepat_guna_perikanan, satuan, dan tahun.

Alur Integrasi (Data Pipeline)
Ekstraksi & Transformasi: Skrip siapkan_data.py membaca dataset mentah Excel, memisahkan entitas master wilayah dan metrik peralatan, lalu mendistribusikannya ke Supabase dan SQLite.

Konektivitas & Federation: Saat aplikasi app.py dijalankan, pustaka SQLAlchemy menarik data dari kedua DBMS. Koneksi ke Supabase dioptimalkan menggunakan @st.cache_resource pada port 6543 guna mencegah penumpukan sesi koneksi (pool exhaustion).

Penggabungan Data: Pustaka Pandas melakukan penggabungan data di tingkat aplikasi (application-level join) menggunakan fungsi pd.merge() berdasarkan kunci bps_kode_desa_kelurahan.

Fitur Interaktivitas Visualisasi
Slicer / Filter Dinamis: Pengguna dapat menyaring data berdasarkan parameter Tahun dan Kabupaten/Kota.

Tabel Rincian Responsif: Menampilkan rincian data tabular terfilter hingga tingkat desa secara real-time.

Grafik Batang (Bar Chart): Visualisasi komparasi 10 Kabupaten/Kota dengan kepemilikan alat teknologi perikanan terbanyak.

Grafik Garis (Line Chart): Menampilkan tren perkembangan total alat perikanan dari tahun ke tahun.

Link Visualisai data: https://visualisasi-data-nw3rfqgjaah75t9oczsjsp.streamlit.app/

Link Github: https://visualisasi-data-nw3rfqgjaah75t9oczsjsp.streamlit.app/

Data Sumber: https://galura.jabarprov.go.id/dataset/jumlah-peralatan-teknologi-tepat-guna-perikanan-di-desa-berdasarkan-desakelurahan-di-jawa-barat
