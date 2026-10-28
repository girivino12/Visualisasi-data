import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

st.set_page_config(page_title="Dashboard Perikanan Jabar", layout="wide")
st.title("Teknologi Tepat Guna Perikanan di Jawa Barat")

# Koneksi ke DBMS
sqlite_engine = create_engine('sqlite:///database_perikanan.db')

@st.cache_resource
def init_supabase():
    return create_engine(st.secrets["SUPABASE_URL"])

supabase_engine = init_supabase()

# Menarik dan Menggabungkan Data
df_metrik = pd.read_sql("SELECT * FROM metrik_perikanan", sqlite_engine)
df_master = pd.read_sql("SELECT * FROM master_desa", supabase_engine)
df_gabungan = pd.merge(df_metrik, df_master, on='bps_kode_desa_kelurahan', how='left')
df_gabungan['jumlah_alat'] = pd.to_numeric(df_gabungan['jumlah_alat_teknologi_tepat_guna_perikanan'], errors='coerce').fillna(0)

# Slicer / Filter
st.sidebar.header("Filter Data")
opsi_tahun = ["Semua"] + list(sorted(df_gabungan['tahun'].unique()))
opsi_kab = ["Semua"] + list(sorted(df_gabungan['bps_nama_kabupaten_kota'].dropna().unique()))

tahun_pilihan = st.sidebar.selectbox("Pilih Tahun:", options=opsi_tahun)
kab_pilihan = st.sidebar.selectbox("Pilih Kabupaten/Kota:", options=opsi_kab)

df_filter = df_gabungan.copy()
if tahun_pilihan != "Semua":
    df_filter = df_filter[df_filter['tahun'] == tahun_pilihan]
if kab_pilihan != "Semua":
    df_filter = df_filter[df_filter['bps_nama_kabupaten_kota'] == kab_pilihan]

# Tampilan Tabel
st.subheader("Data Rincian")
kolom_tampil = ['tahun', 'bps_nama_kabupaten_kota', 'bps_nama_kecamatan', 'bps_nama_desa_kelurahan', 'jumlah_alat']
st.dataframe(df_filter[kolom_tampil], use_container_width=True, height=250)

# Visualisasi Grafik
col1, col2 = st.columns(2)
with col1:
    st.subheader("10 Wilayah dengan Alat Terbanyak")
    agg_kab = df_filter.groupby('bps_nama_kabupaten_kota')['jumlah_alat'].sum().reset_index()
    agg_kab = agg_kab.sort_values(by='jumlah_alat', ascending=False).head(10)
    fig1 = px.bar(agg_kab, x='jumlah_alat', y='bps_nama_kabupaten_kota', orientation='h')
    fig1.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Tren Kepemilikan Alat per Tahun")
    agg_thn = df_filter.groupby('tahun')['jumlah_alat'].sum().reset_index()
    fig2 = px.line(agg_thn, x='tahun', y='jumlah_alat', markers=True)
    fig2.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig2, use_container_width=True)