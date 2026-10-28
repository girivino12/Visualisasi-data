import pandas as pd
from sqlalchemy import create_engine

# Membaca data mentah
file_path = 'idm_jml_prltn_tknlg_tepat_guna_ikan_di_desa__des_kel.xlsx'
df = pd.read_excel(file_path)

# Memisahkan tabel
df_master = df[['bps_kode_desa_kelurahan', 'bps_nama_desa_kelurahan', 'bps_nama_kecamatan', 'bps_nama_kabupaten_kota']].drop_duplicates()
df_metrik = df[['bps_kode_desa_kelurahan', 'jumlah_alat_teknologi_tepat_guna_perikanan', 'satuan', 'tahun']]

# Menyimpan ke SQLite (Lokal)
sqlite_engine = create_engine('sqlite:///database_perikanan.db')
df_metrik.to_sql('metrik_perikanan', sqlite_engine, if_exists='replace', index=False)
print("Berhasil menyimpan 'metrik_perikanan' ke SQLite!")

# Menyimpan ke Supabase (Ganti dengan string kosong setelah dijalankan)
SUPABASE_URL =
supabase_engine = create_engine(SUPABASE_URL)
df_master.to_sql('master_desa', supabase_engine, if_exists='replace', index=False)
print("Berhasil menyimpan 'master_desa' ke Supabase!")