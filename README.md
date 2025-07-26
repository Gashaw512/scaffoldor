# 🚀 scaffoldor

**A Python CLI to scaffold secure fullstack application projects (FastAPI + React + Keycloak)**

[![PyPI](https://img.shields.io/pypi/v/scaffoldor)](https://pypi.org/project/scaffoldor/)
[![License](https://img.shields.io/github/license/Gashaw512/scaffoldor)](LICENSE)
[![Build Status](https://github.com/Gashaw512/scaffoldor/actions/workflows/ci.yml/badge.svg)](https://github.com/Gashaw512/scaffoldor/actions)

---

## 📦 What It Does

`scaffoldor` streamlines the creation of secure full-stack application structures. It generates a ready-to-use project with pre-configured boilerplate for:

-   🔧 **Backend**: FastAPI (Python), including SQLAlchemy, Alembic, and Pydantic.
-   🎨 **Frontend**: React (JavaScript/TypeScript), with Axios and React Router DOM. Tailwind CSS for development.
-   🔐 **Auth**: Basic setup for Keycloak integration (using `python-keycloak`).
-   🛠️ **Infra**: Docker Compose for easy environment setup.
-   📄 **Dev Tools**: Pre-configured `requirements.txt`, `package.json`, and `.env.example`.
-   🧪 **Testing**: Includes pytest for backend and ESLint/Prettier for frontend development.

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
### From GitHub (editable code for development)
```bash
git clone [https://github.com/Gashaw512/scaffoldor.git](https://github.com/Gashaw512/scaffoldor.git)
cd scaffoldor
python -m venv .venv # Using .venv for consistency
# Activate env:
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (Cmd):
.\.venv\Scripts\activate.bat
pip install -e .

```
## Usage
`scaffoldor`  is a command-line interface tool. Here's how to use its main functionalities:
```bash
scaffoldor my-awesome-project --path ./projects --verbose

```
### 🚀 Create a New Project

```bash
# Basic usage with default template in current directory
scaffoldor create my-new-project

# Specify a parent directory and enable verbose output
scaffoldor --verbose create my-awesome-project --path ./projects

# Use a specific template (if you have created custom ones)
scaffoldor create my-app --template my-custom-template --path ./apps

# Perform a dry run to see what would be created without making changes
scaffoldor --dry-run create test-project-dry-run
```
### 📋 List Available Templates
See all templates scaffoldor can use to create projects.
```bash
scaffoldor list-templates
```
### 🆕 Initialize a Custom Template
Create a new boilerplate template configuration and content files based on the default, which you can then customize.
```bash
scaffoldor init my-new-template
```
After running this, you'll find `my-new-template.json` in `scaffoldor/templates/` and example content in `scaffoldor/templates/content/my-new-template_example/.` Remember to `pip install -e . ` again after modifying templates for them to be recognized by your installed scaffoldor tool.

### CLI Options (Global Flags & Command-Specific)

| Flag/Argument    | Command Applies To | Description                                                | Default           |
| :--------------- | :----------------- | :--------------------------------------------------------- | :---------------- |
| `scaffoldor`     | Global             | The main command-line entry point.                         | N/A               |
| `-h, --help`     | Global, Sub-command| Show the help message for the CLI or a specific command.   | N/A               |
| `--version`      | Global             | Show `scaffoldor`'s current version.                       | N/A               |
| `--dry-run`      | `create`           | Simulate project creation without making any changes.      | `False`           |
| `-v, --verbose`  | All commands       | Display detailed logging output during execution.          | `False`           |
|                  |                    |                                                            |                   |
| **`create` command specific:** |                    |                                                            |                   |
| `project_name`   | `create`           | **Required.** The name of the project directory to create. | N/A               |
| `-p, --path`     | `create`           | Parent directory to create the project in.                 | Current directory |
| `-t, --template` | `create`           | Project template to use (e.g., `default`, `my-custom-template`). | `default`         |
|                  |                    |                                                            |                   |
| **`init` command specific:** |                    |                                                            |                   |
| `template_name`  | `init`             | **Required.** Name of the new template to initialize.      | N/A               |

**Important Note on Global Flags:** Global flags like `--verbose` and `--dry-run` must be placed **before** the command name:
`scaffoldor --verbose create my-app`
`scaffoldor --dry-run create another-project`



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




