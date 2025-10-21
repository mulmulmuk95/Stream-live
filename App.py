import streamlit as st
import subprocess
import threading
import time
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="YouTube Live Loop", layout="centered")
st.title("📺 YouTube Live Streaming (1 Video Loop)")

# -------------------------
# Upload Video
# -------------------------
uploaded_file = st.file_uploader("Upload video (MP4/MOV)", type=["mp4", "mov"])

# Preview Thumbnail
if uploaded_file:
    video_path = Path("temp_video") / uploaded_file.name
    video_path.parent.mkdir(exist_ok=True)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video(str(video_path))  # preview video

# -------------------------
# Input Stream Key & Durasi
# -------------------------
stream_key = st.text_input("Stream Key YouTube Studio", placeholder="Masukkan Stream Key")
duration_hours = st.number_input("Durasi Live (jam)", min_value=0.1, max_value=24.0, value=1.0, step=0.1)

# Tombol Start / Stop
col1, col2 = st.columns(2)
start_button = col1.button("🚀 Start Live", use_container_width=True)
stop_button = col2.button("🛑 Stop Live", use_container_width=True)

# -------------------------
# Global Variables
# -------------------------
if "ffmpeg_proc" not in st.session_state:
    st.session_state.ffmpeg_proc = None
if "stop_flag" not in st.session_state:
    st.session_state.stop_flag = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "duration_seconds" not in st.session_state:
    st.session_state.duration_seconds = 0

# -------------------------
# Fungsi Loop Video
# -------------------------
def run_loop(video_path, rtmp_url, duration_seconds):
    st.session_state.stop_flag = False
    proc = subprocess.Popen([
        "ffmpeg", "-re", "-stream_loop", "-1", "-i", video_path,
        "-c:v", "libx264", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-f", "flv", rtmp_url
    ])
    st.session_state.ffmpeg_proc = proc
    st.session_state.start_time = time.time()
    st.session_state.duration_seconds = duration_seconds

    while True:
        elapsed = time.time() - st.session_state.start_time
        if st.session_state.stop_flag or elapsed >= duration_seconds:
            proc.terminate()
            st.session_state.ffmpeg_proc = None
            st.success("✅ Live streaming berhenti otomatis")
            break
        time.sleep(1)

# -------------------------
# Hitung Sisa Waktu Live
# -------------------------
def remaining_time():
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = st.session_state.duration_seconds - elapsed
        if remaining < 0:
            remaining = 0
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        seconds = int(remaining % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"

# -------------------------
# Main Logic
# -------------------------
if uploaded_file and stream_key:
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    if start_button and st.session_state.ffmpeg_proc is None:
        duration_seconds = duration_hours * 3600
        st.info("🔄 Mulai live streaming...")
        thread = threading.Thread(target=run_loop, args=(video_path, rtmp_url, duration_seconds))
        thread.start()

    if stop_button and st.session_state.ffmpeg_proc:
        st.session_state.stop_flag = True
        st.warning("🛑 Stop manual dijalankan...")

    if st.session_state.ffmpeg_proc:
        st.metric("⏱️ Sisa Waktu Live", remaining_time())

elif not uploaded_file:
    st.warning("Silakan upload video terlebih dahulu.")
elif not stream_key:
    st.warning("Silakan masukkan Stream Key YouTube Studio.")
