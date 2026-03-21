# forgegen

Audio and video to funscript — in seconds, not hours.

forgegen is a haptic content generation engine. Drop in a music track or video file. It analyses the rhythm, phrase structure, and energy envelope, then outputs a `.funscript` file ready to drive any haptic device.

---

## Who is this for?

- **Content scripters** — get a quality draft in under a minute instead of 2–8 hours of manual keyframing
- **Music and EDM creators** — sync haptics to any track, no video or scripting tools required
- **FunScriptForge users** — start from a generated draft, spend your time on refinement instead of ground-up creation
- **Pipeline builders** — full CLI and importable Python library; fits into watch-folder pipelines, CI/CD, and batch workflows

## Why it exists

The existing toolchain is fragmented. OpenFunscripter is manual-only. PythonDancer produces mechanical beat-locked output with no phrase shaping. FunGen is VR-only. FunscriptFlow requires coding. No tool generates quality funscripts from arbitrary audio or video, with phrase-level mode shaping, offline, with a clean handoff to an editing tool.

forgegen is that tool.

---

## How it works

```text
Audio / Video → Beat & energy analysis → Phrase classification → Curve shaping → .funscript
```

1. **Analyse** — detect beat grid, BPM, phrase boundaries, and energy envelope
2. **Classify** — label each phrase: `break`, `tease`, `slow`, `steady`, `fast`, or `edging`
3. **Shape** — sculpt the motion curve per mode (tease = narrow, edging = builds 50→100%, break = minimal)
4. **Export** — validated `.funscript` JSON, compatible with all major players and editors

---

## Stack

```text
forgegen          (this repo — Streamlit UI)
  └── videoflow   (generation engine — beats, analysis, funscript export)
        └── media-tools  (low-level file ops — probe, clip, extract, concat)
              └── FFmpeg / librosa
```

---

## Quick start

```bash
# Clone alongside videoflow
git clone git@github-xolvco:xolvco/forgegen.git
git clone git@github-xolvco:xolvco/videoflow.git

cd forgegen
pip install -r requirements.txt

streamlit run app.py
```

Open `http://localhost:8501`. Drop in an audio file. Pick a style. Generate.

### CLI

```bash
# Generate a funscript from an audio file
videoflow generate-funscript track.mp3

# Full mix source, custom range
videoflow generate-funscript track.mp3 --source full --low 20 --high 75

# Batch (shell)
for f in media/*.mp3; do
    videoflow generate-funscript "$f" -o funscripts/"$(basename "$f" .mp3).funscript"
done
```

---

## Styles

| Style | Low | High | Source | Best for |
| --- | --- | --- | --- | --- |
| 🥁 Rhythmic | 10 | 90 | percussive | EDM, beat-locked |
| 🌊 Sensual | 20 | 75 | full mix | Slow, melodic |
| ⚡ Intense | 5 | 95 | percussive | Maximum range |
| 🌪 Chaotic | 10 | 90 | full mix | Complex mixes, unpredictable peaks |

---

## Where it fits

forgegen is the **generation** layer. FunScriptForge is the **editing** layer.

```text
forgegen  →  .funscript  →  FunScriptForge  →  any device
```

forgegen never edits funscripts. FunScriptForge never generates from scratch. Clean handoff at the `.funscript` boundary.

---

## Docs

Full documentation: `mkdocs serve` from the repo root, or see `docs/`.

---

## License

See [LICENSE](LICENSE).
