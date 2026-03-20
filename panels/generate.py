"""Tab 1 — Generate.

Style cards → Generate → funscript curve preview → download.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Style presets
# ---------------------------------------------------------------------------

_STYLES: dict[str, dict] = {
    "rhythmic": {
        "label": "🥁 Rhythmic",
        "desc": "Locks tightly to the beat. Best for EDM and high-energy music.",
        "low": 10,
        "high": 90,
        "source": "percussive",
    },
    "sensual": {
        "label": "🌊 Sensual",
        "desc": "Softer strokes, wider trough. Suits slower or more melodic tracks.",
        "low": 20,
        "high": 75,
        "source": "full",
    },
    "intense": {
        "label": "⚡ Intense",
        "desc": "Maximum range. Every beat drives the full stroke.",
        "low": 5,
        "high": 95,
        "source": "percussive",
    },
    "chaotic": {
        "label": "🌪 Chaotic",
        "desc": "Full mix drives the curve — voice and energy create unpredictable peaks.",
        "low": 10,
        "high": 90,
        "source": "full",
    },
}

# Mode colours for the chart
_MODE_COLOURS: dict[str, str] = {
    "break":  "#424242",
    "tease":  "#7e57c2",
    "slow":   "#42a5f5",
    "steady": "#26a69a",
    "fast":   "#ef5350",
    "edging": "#ff7043",
}


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------

def _energy_chart(beat_map, modes):
    """Bar chart of beat energy, coloured by phrase mode."""
    import plotly.graph_objects as go

    # Build a colour per beat based on its phrase mode
    def _mode_for(t):
        for start, end, mode in modes:
            if start <= t < end:
                return mode
        return "steady"

    colours = [_MODE_COLOURS.get(_mode_for(b), "#26a69a") for b in beat_map.beats]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[b / 1000 for b in beat_map.beats],
        y=beat_map.energy,
        marker_color=colours,
        hovertemplate="<b>%{x:.2f}s</b><br>energy: %{y:.3f}<extra></extra>",
    ))

    # Phrase boundary lines
    for start_ms, end_ms in beat_map.phrases:
        fig.add_vline(
            x=start_ms / 1000,
            line_width=1,
            line_dash="dot",
            line_color="rgba(255,255,255,0.25)",
        )

    fig.update_layout(
        height=160,
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(
            title="time (s)",
            color="#aaa",
            gridcolor="rgba(255,255,255,0.06)",
        ),
        yaxis=dict(
            title="energy",
            range=[0, 1],
            color="#aaa",
            gridcolor="rgba(255,255,255,0.06)",
        ),
    )
    return fig


def _funscript_chart(curve):
    """Line chart of the generated funscript position curve."""
    import plotly.graph_objects as go

    if not curve:
        return go.Figure()

    times = [t / 1000 for t, _ in curve]
    positions = [p for _, p in curve]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=positions,
        mode="lines",
        line=dict(color="#ff7043", width=1.5),
        hovertemplate="<b>%{x:.2f}s</b><br>pos: %{y}<extra></extra>",
    ))

    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(
            title="time (s)",
            color="#aaa",
            gridcolor="rgba(255,255,255,0.06)",
        ),
        yaxis=dict(
            title="position",
            range=[0, 100],
            color="#aaa",
            gridcolor="rgba(255,255,255,0.06)",
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------

def render() -> None:
    bm = st.session_state.beat_map
    if bm is None:
        return

    from videoflow.generate import beats_to_curve, classify_modes, shape_curve, export_funscript

    # Compute modes once (used for chart colouring even before generate)
    if st.session_state.modes is None:
        st.session_state.modes = classify_modes(bm)
    modes = st.session_state.modes

    # -----------------------------------------------------------------------
    # Energy heatmap
    # -----------------------------------------------------------------------

    st.caption("Beat energy — coloured by phrase mode")
    st.plotly_chart(_energy_chart(bm, modes), use_container_width=True)

    # Mode legend
    active_modes = {m for _, _, m in modes}
    legend_cols = st.columns(len(active_modes))
    for col, mode in zip(legend_cols, sorted(active_modes)):
        colour = _MODE_COLOURS.get(mode, "#aaa")
        col.markdown(
            f"<span style='color:{colour}'>\u25a0</span> {mode}",
            unsafe_allow_html=True,
        )

    st.divider()

    # -----------------------------------------------------------------------
    # Style cards
    # -----------------------------------------------------------------------

    st.markdown("**Style**")
    style_cols = st.columns(len(_STYLES))
    for col, (key, preset) in zip(style_cols, _STYLES.items()):
        selected = st.session_state.style == key
        border = "2px solid #ff7043" if selected else "1px solid #444"
        bg = "rgba(255,112,67,0.08)" if selected else "rgba(255,255,255,0.03)"
        if col.button(
            preset["label"],
            key=f"style_{key}",
            use_container_width=True,
            help=preset["desc"],
            type="primary" if selected else "secondary",
        ):
            st.session_state.style = key
            st.session_state.low = preset["low"]
            st.session_state.high = preset["high"]
            st.session_state.source = preset["source"]
            st.session_state.curve = None
            st.session_state.funscript_bytes = None
            st.rerun()

    # Show active style description
    active = _STYLES[st.session_state.style]
    st.caption(active["desc"])

    st.divider()

    # -----------------------------------------------------------------------
    # Generate button
    # -----------------------------------------------------------------------

    if st.button("▶ Generate", type="primary", use_container_width=True):
        with st.spinner("Generating funscript…"):
            curve = beats_to_curve(
                bm,
                low=st.session_state.low,
                high=st.session_state.high,
            )
            shaped = shape_curve(curve, modes, low=st.session_state.low)
            st.session_state.curve = shaped

            # Build funscript bytes in memory via temp file
            with tempfile.NamedTemporaryFile(suffix=".funscript", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                title = Path(st.session_state.audio_name).stem
                export_funscript(shaped, tmp_path, title=title)
                st.session_state.funscript_bytes = tmp_path.read_bytes()
            finally:
                tmp_path.unlink(missing_ok=True)

    # -----------------------------------------------------------------------
    # Funscript preview + download
    # -----------------------------------------------------------------------

    if st.session_state.curve:
        st.caption("Generated funscript")
        st.plotly_chart(
            _funscript_chart(st.session_state.curve),
            use_container_width=True,
        )

        action_count = len(st.session_state.curve)
        st.caption(f"{action_count} actions · {bm.duration_ms / 1000:.1f}s")

        if st.session_state.funscript_bytes:
            stem = Path(st.session_state.audio_name).stem or "output"
            st.download_button(
                label="💾 Download .funscript",
                data=st.session_state.funscript_bytes,
                file_name=f"{stem}.funscript",
                mime="application/json",
                use_container_width=True,
            )
