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
git clone https://github.com/yourusername/scaffoldor.git
cd scaffoldor
python -m venv env
# Activate env:
# macOS/Linux:
source env/bin/activate
# Windows:
.\env\Scripts\activate
pip install -e .

```
## Usage
```bash
scaffoldor my-awesome-project --path ./projects --verbose

```

## CLI Options
```text
-p, --path: Parent directory to create the project in (default: current directory)

-t, --template: Project template to use (default: default)

--dry-run: Show actions without creating files or directories

-v, --verbose: Show detailed output

```

### 📁 Creates This Structure

```text
my-awesome-project/
├── backend/
│   └── app/
│       ├── api/v1/
│       ├── core/
│       ├── models/
│       ├── schemas/
│       └── services/
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── context/
├── auth/
│   └── keycloak-config/
├── infra/
├── docs/
├── .env.example
├── docker-compose.yml
└── README.md


