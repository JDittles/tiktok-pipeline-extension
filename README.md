# TikTok Crisis Classification Pipeline

A multimodal AI pipeline that classifies TikTok videos of natural disasters into a structured crisis response taxonomy. Given a TikTok URL, it downloads the video, extracts frames, and uses a vision-capable LLM to determine what supplies, personnel, and actions are being requested or offered.

Deployed as a REST API on Google Cloud Run with CI/CD via GitHub Actions.

---

## How It Works

1. **Download** — `yt-dlp` fetches the video and metadata into a temporary directory
2. **Extract** — OpenCV samples one frame per second, resizes to 448×448, and base64-encodes each frame
3. **Classify** — Frames and post text are sent to a vision LLM with a structured prompt grounded in a humanitarian crisis taxonomy
4. **Return** — The LLM returns a JSON object with labels, confidence score, and visual evidence summary
5. **Cleanup** — The temporary video file is deleted

---

## Output Format

```json
{
  "text": "post title and description",
  "type": ["Request"],
  "action_request": ["Search and Rescue"],
  "personnel_request": ["Search and Rescue Teams"],
  "supplies_request": [],
  "action_offer": [],
  "personnel_offer": [],
  "supplies_offer": [],
  "actionability": true,
  "explanation": "...",
  "visual_evidence": "...",
  "confidence": 0.91,
  "insufficient_visual_evidence": false
}
```

The taxonomy covers three top-level categories — **Supplies**, **Emergency Personnel**, and **Actions** — each with detailed subcategories drawn from humanitarian response frameworks.

---

## API

**Live endpoint:** `https://tiktok-pipeline-747586044805.us-central1.run.app`

### `POST /classify`

```json
{
  "url": "https://www.tiktok.com/@user/video/...",
  "provider": "gemini",
  "api_key": "YOUR_API_KEY"
}
```

| Field      | Required | Values                                 |
| ---------- | -------- | -------------------------------------- |
| `url`      | Yes      | Any public TikTok URL                  |
| `provider` | No       | `gemini` (default), `openai`, `claude` |
| `api_key`  | No       | Falls back to environment variable     |

### `GET /health`

Returns `{"status": "ok"}`.

Interactive docs available at `/docs`.

---

## Local Development

**Prerequisites:** Python 3.11+, [uv](https://github.com/astral-sh/uv)

```bash
git clone https://github.com/JDittles/tiktok-pipeline-extension
cd tiktok-pipeline-extension
uv sync
cp .env.example .env   # fill in your API keys
```

**Run the API server:**

```bash
ENV=development python main.py --serve
```

**Classify a single video via CLI:**

```bash
python main.py "https://www.tiktok.com/@user/video/..."
```

**Test against the local server:**

Edit `TIKTOK_URL` and `PROVIDER` in `experimental/test_classify.py`, then:

```bash
python experimental/test_classify.py
```

---

## Supported Providers

| Provider   | Model             | Notes                              |
| ---------- | ----------------- | ---------------------------------- |
| `gemini`   | gemini-2.0-flash  | Default. Requires `GEMINI_API_KEY` |
| `openai`   | gpt-4o            | Requires `OPENAI_API_KEY`          |
| `claude`   | claude-sonnet-4-6 | Requires `ANTHROPIC_API_KEY`       |
| `ollama`   | gemma4:e4b        | Local only. Requires Ollama        |

---

## Deployment

The project deploys automatically to Google Cloud Run on every push to `main`.

**Stack:** Docker → Google Artifact Registry → Cloud Run

**Required GitHub Secrets:**

| Secret               | Description               |
| -------------------- | ------------------------- |
| `GOOGLE_CREDENTIALS` | Service account JSON key  |
| `GCP_PROJECT_ID`     | GCP project ID            |
| `GCP_REGION`         | e.g. `us-central1`        |
| `CLOUD_RUN_SERVICE`  | Cloud Run service name    |

To deploy manually:

```bash
docker build -t tiktok-pipeline .
docker run -p 8000:8000 --env-file .env tiktok-pipeline
```

---

## Project Structure

```text
src/
├── api.py                  # FastAPI app
└── pipeline/
    ├── classify.py         # Orchestrates the full pipeline
    ├── download.py         # yt-dlp video download
    ├── video.py            # Frame extraction via OpenCV
    └── prompts.py          # Taxonomy, prompt construction
main.py                     # CLI + server entry point
Dockerfile
.github/workflows/deploy.yml
```
