"""forgegen — Streamlit UI entry point.

Launch with:
    streamlit run app.py

Layout
------
Sidebar
  • Audio file uploader
  • Track info once loaded (BPM, duration, phrases)

Main area (tabs)
  1. Generate  — style cards → Generate → funscript preview → download
  2. Details   — beat map, per-phrase mode overrides, advanced controls
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# videoflow must be importable — install with: pip install -e ../videoflow
import streamlit as st

from panels import generate as generate_panel
from panels import details as details_panel

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="forgegen",
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------

if "beat_map" not in st.session_state:
    st.session_state.beat_map = None
if "curve" not in st.session_state:
    st.session_state.curve = None
if "modes" not in st.session_state:
    st.session_state.modes = None
if "funscript_bytes" not in st.session_state:
    st.session_state.funscript_bytes = None
if "audio_name" not in st.session_state:
    st.session_state.audio_name = ""
if "style" not in st.session_state:
    st.session_state.style = "rhythmic"
if "low" not in st.session_state:
    st.session_state.low = 10
if "high" not in st.session_state:
    st.session_state.high = 90
if "source" not in st.session_state:
    st.session_state.source = "percussive"

# ---------------------------------------------------------------------------
# Sidebar — file upload and track info
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("🔨 forgegen")
    st.caption("audio → funscript")

    st.divider()

    uploaded = st.file_uploader(
        "Drop an audio or video file",
        type=["mp3", "wav", "flac", "ogg", "m4a", "aac", "mp4", "mkv", "mov"],
        help="Audio or video file. Audio is extracted automatically from video.",
    )

    if uploaded is not None and uploaded.name != st.session_state.audio_name:
        # New file — analyse
        st.session_state.audio_name = uploaded.name
        st.session_state.beat_map = None
        st.session_state.curve = None
        st.session_state.modes = None
        st.session_state.funscript_bytes = None

        with st.spinner("Analysing beats…"):
            suffix = Path(uploaded.name).suffix or ".mp3"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name
            try:
                from videoflow.audio import BeatError, analyze_beats
                beat_map = analyze_beats(
                    tmp_path,
                    source=st.session_state.source,
                )
                st.session_state.beat_map = beat_map
            except BeatError as exc:
                st.error(f"Beat analysis failed: {exc}")
            except Exception as exc:
                st.error(f"Error: {exc}")
            finally:
                os.unlink(tmp_path)

    # Track info
    bm = st.session_state.beat_map
    if bm is not None:
        st.divider()
        st.metric("BPM", f"{bm.bpm:.1f}")
        col1, col2 = st.columns(2)
        col1.metric("Beats", len(bm.beats))
        col2.metric("Phrases", len(bm.phrases))
        mins = bm.duration_ms // 60_000
        secs = (bm.duration_ms % 60_000) / 1000
        st.metric("Duration", f"{mins}:{secs:04.1f}")
        st.caption(f"Source: {st.session_state.source}")

# ---------------------------------------------------------------------------
# Main area — tabs
# ---------------------------------------------------------------------------

if st.session_state.beat_map is None:
    st.markdown("## Drop an audio file to get started")
    st.markdown(
        "Upload a track in the sidebar. forgegen will detect the beat grid, "
        "analyse phrase energy, and generate a `.funscript` matched to the music."
    )
    st.markdown(
        "**Supports:** MP3, WAV, FLAC, OGG, M4A, AAC — and MP4/MKV/MOV "
        "(audio is extracted automatically)."
    )
else:
    tab_gen, tab_details = st.tabs(["Generate", "Details"])

    with tab_gen:
        generate_panel.render()

    with tab_details:
        details_panel.render()
