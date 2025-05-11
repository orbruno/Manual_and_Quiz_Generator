# Manual & Quiz Generator

This repository contains a **FastAPI** backend and a **React + TypeScript** frontend (bundled with Vite) that together let you:

1. **Upload** 2+ PDF or TXT documents and a text prompt
2. **Generate** a styled training manual via OpenAI
3. **Generate** a mixed single- and multiple-choice quiz based on that manual

Everything runs in Docker for zero-hassle local setup.

---

## 🚀 Prerequisites

- [Docker Engine](https://docs.docker.com/get-docker/) (v20+)
- [Docker Compose](https://docs.docker.com/compose/) (v1.29+)

---

## 🔧 Configuration

1. **Clone** this repo:

   ```bash
   git clone https://github.com/your-username/manual-quiz-generator.git
   cd manual-quiz-generator
   ```

2. **Create your `.env`** file for the backend:

   In `backend/.env`, add your OpenAI API key:

   ```dotenv
   OPENAI_API_KEY=sk-…
   ```

   > **Note:** Never commit your real API key into source control. Make sure `.env` is listed in `.gitignore`.

---

## Running with Docker Compose

From the **project root** (where `docker-compose.yml` lives), run:

```bash
docker-compose up --build
```

This will:

- **Build** two images:
  - `manual-quiz-backend` (FastAPI + Uvicorn)
  - `manual-quiz-frontend` (Vite + React)
- **Start** two containers, exposing:
  - Backend → `http://localhost:8000`
  - Frontend → `http://localhost:5173`

To stop & remove the containers, press `Ctrl+C` and then:

```bash
docker-compose down
```

---

## 🎯 Usage

1. Open your browser at:
   ```
   http://localhost:5173
   ```
2. **Upload** at least two `.pdf` or `.txt` files and enter your prompt.
3. Click **Generate** → wait for the spinner → see your manual on the right.
4. Under the form, a quiz will appear once the manual is ready.

---

## 📝 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI routes (/api/manual, /api/quiz)
│   │   └── ai_client.py   # OpenAI helper functions
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env               # your OPENAI_API_KEY goes here
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── UploadForm.tsx
│   │   │   ├── ManualDisplay.tsx
│   │   │   └── Quiz.tsx
│   │   └── index.css      # includes Tailwind base/components/utilities
│   ├── vite.config.ts
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## Tips

- If you change your backend code, rebuild with:
  ```bash
  docker-compose up --build backend
  ```
- To view backend logs:
  ```bash
  docker-compose logs -f backend
  ```
- To view frontend logs:
  ```bash
  docker-compose logs -f frontend
  ```

---
