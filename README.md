# YouTube Live Loop - Streamlit App

Aplikasi ini memungkinkan streaming **1 video loop otomatis** ke YouTube dari HP atau browser, menggunakan Stream Key dari YouTube Studio.

## Cara Deploy di HP (Streamlit Cloud)

1. Buka [https://share.streamlit.io](https://share.streamlit.io) di browser HP
2. Klik **New App → GitHub**
3. Pilih repo ini dan file `app.py`
4. Streamlit Cloud akan otomatis deploy aplikasi

## Cara Pakai

1. Upload video MP4/MOV
2. Masukkan **Stream Key YouTube Studio**
3. Pilih **Durasi Live (jam)**
4. Klik **Start Live**
5. Streaming akan berjalan **loop video terus-menerus** sampai durasi habis
6. Klik **Stop Live** jika ingin menghentikan manual

## Catatan

- Audio video akan terdengar oleh penonton
- Pastikan FFmpeg terinstall di server (untuk Streamlit Cloud biasanya sudah tersedia)
- Mobile-friendly: bisa dibuka dan dikontrol sepenuhnya dari HP
