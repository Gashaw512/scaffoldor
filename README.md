


# 🚀 scaffoldor

**A Python CLI to scaffold secure fullstack application projects (FastAPI + React + Keycloak)**

[![PyPI](https://img.shields.io/pypi/v/scaffoldor)](https://pypi.org/project/scaffoldor/)
[![License](https://img.shields.io/github/license/Gashaw512/scaffoldor)](LICENSE)
[![Build Status](https://github.com/Gashaw512/scaffoldor/actions/workflows/ci.yml/badge.svg)](https://github.com/Gashaw512/scaffoldor/actions)

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

### From PyPI (official, when published)
```bash
pip install scaffoldor
```

### From TestPyPI (for testing latest unpublished versions)
```bash
pip install -i https://test.pypi.org/simple/ scaffoldor==0.1.1

```
### From Github (edditable code)
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
```

Tomorrow task
📚 Usage Example
bash
Copy
Edit
# Install from PyPI
pip install scaffoldor

# Scaffold a new project
scaffoldor my-app --template default --path ./apps --verbose
✨ Bonus Polish Features
You should:

✅ Add --version to your CLI:


parser.add_argument("-v", "--version", action="version", version="scaffoldor 0.1.0")
✅ Add --init option to define new templates:


scaffoldor --init my-custom-template


Updated CLI with --version, --init, --help flags?

A test case using pytest?




