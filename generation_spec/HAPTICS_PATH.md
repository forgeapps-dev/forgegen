# The Path to Haptics

## What This Is

forgegen is a **haptic content generation engine**.

A funscript is just motion data — position values over time. What device plays it, and what media syncs to it, is entirely up to you. The format is the same. The devices are different. The content has no restrictions.

```
Audio / Video / Music
        ↓
    forgegen
        ↓
    funscript
        ↓
  Handy / OSR2 / estim / bHaptics / Owo / any device
```

---

## The Demo Use Case — Music → Haptics

**Drop a song. Feel it.**

1. Add an MP3 (or any audio file)
2. forgegen detects beats, BPM, energy, spectral content
3. Generates a funscript matched to the music
4. Export to any haptic device
5. Play the song — feel the rhythm, drops, builds

This is:
- **Completely SFW** — works for any music, any genre
- **Universal** — everyone has music they love
- **30-second demo** — drop file → generate → feel
- **No video required** — pure audio-to-haptics path
- **Any device** — Handy, OSR2, estim, bass shakers, haptic suits

This is the door. It works for anyone with a haptic device and a music library.

---

## Why This Goes Fast

forgegen's audio pipeline is already specced:

```
MP3/WAV
  ↓
Beat & BPM detection      → pulse timing
Energy & spectral analysis → intensity envelope
Bass / transients         → impact points
Build / drop detection    → tension and release
  ↓
funscript
```

No video analysis needed. No LLM. Pure DSP.
Beat detection → funscript is a solved problem. The pipeline is deterministic and fast.

---

## The Broader Picture

Music→haptics is the demo. The same engine handles:

| Input | Use Case | Notes |
|---|---|---|
| Music (MP3) | Feel the music | The demo. SFW. Universal. |
| Beat track | Sync haptics to rhythm content | Audio-locked precision |
| Video | Sync haptics to motion | Full pipeline with optional LLM semantic layer |
| Video + Audio | Hybrid — best of both | Weighted blend, user controls dominance |
| Video + Audio + Captions | Semantic haptics | Language meaning shapes the pattern |
| Existing funscript | Tone / reshape | FunScriptForge workflow |

Every path ends in the same place: a funscript, exported to any device.

---

## The Stack

```
forgegen (generation engine)
    ↓ produces
funscript
    ↓ toned and shaped by
FunScriptForge (authoring tool)
    ↓ exported to
Device folders (Handy / OSR2 / estim-foc / estim-stereo / ...)
    ↓ published to
Distribution Hub (content discovery + delivery)
    ↓ played by
SyncPlayer (synced playback — video + audio + haptics)
```

Each tool is independent. Each does one thing well.
Together they are the complete path from any media to any haptic device.

---

## forgegen App — Music Haptics Tab

The music→haptics use case deserves a first-class tab in the forgegen app:

```
[ Media ]  [ Generate ]  [ Preview ]  [ Export ]
```

**Media tab:**
- Drop music file (MP3, WAV, FLAC)
- Optional: drop video to sync playback with
- Instant waveform + BPM detection on load

**Generate tab:**
- Tone selection (same six cards as FunScriptForge)
- One slider: Energy sensitivity (how hard the drops hit)
- [ Generate ] button
- Shows funscript plotly + heatmap as it builds

**Preview tab:**
- Play music + funscript simultaneously
- Waveform aligned with funscript timeline
- See beats → haptic pulses in real time

**Export tab:**
- Device selection (or all)
- Standard export to output folder

---

## Positioning Line

> **Turn any audio into a haptic experience.**
> Drop a song. Feel the beat.
> forgegen generates haptic content from music, video, or both.
> Any device. Any genre. Any content.
