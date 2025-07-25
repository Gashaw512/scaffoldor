# 🚀 scaffoldor

**A Python CLI to scaffold secure fullstack application projects (FastAPI + React + Keycloak)**

---

## 📦 What It Does

Generate a ready-to-use secure app structure with:

- 🔧 Backend (FastAPI, Python)
- 🎨 Frontend (React + Tailwind)
- 🔐 Auth (Keycloak)
- 🛠️ Infra (Docker Compose)
- 📄 Docs & Env examples

---

## ⚙️ Installation

```bash
# Clone & install locally
git clone https://github.com/yourusername/scaffoldor.git
cd scaffoldor
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
pip install -e .
```
## Usage
```bash
scaffoldor my-awesome-project
```

Creates this:

my-awesome-project/
├── backend/
├── frontend/
├── auth/
├── infra/
├── docs/
├── .env.example
├── docker-compose.yml
└── README.md
