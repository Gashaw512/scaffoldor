import sys
from pathlib import Path

BASE_STRUCTURE = {
    "backend": ["app/api/v1", "app/core", "app/models", "app/schemas", "app/services"],
    "frontend": ["src/components", "src/pages", "src/services", "src/context"],
    "auth": ["keycloak-config"],
    "infra": [],
    "docs": [],
}

README_TEMPLATE = """\
# {project_name}

Welcome to the {project_name} project!

## Overview

This project scaffolded by scaffoldor CLI tool.

## Project Structure

- backend/ - FastAPI backend service
- frontend/ - React + Tailwind frontend app
- auth/ - Keycloak or authentication-related configs
- infra/ - Docker, Kubernetes manifests, and deployment configs
- docs/ - Project documentation

## Getting Started

Instructions to setup and run your project...

---

## Author

Your Name  
your.email@example.com
"""

ENV_EXAMPLE = """\
# Environment variables example

DATABASE_URL=postgresql://user:password@localhost:5432/dbname
KEYCLOAK_URL=http://localhost:8080
REDIS_URL=redis://localhost:6379
"""

DOCKER_COMPOSE_YML = """\
version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - keycloak
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    ports:
      - "5432:5432"
  keycloak:
    image: quay.io/keycloak/keycloak:20.0.3
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
    ports:
      - "8080:8080"
    command: start-dev
"""

def create_files(project_root: Path, project_name: str):
    (project_root / "README.md").write_text(README_TEMPLATE.format(project_name=project_name))
    (project_root / ".env.example").write_text(ENV_EXAMPLE)
    (project_root / "docker-compose.yml").write_text(DOCKER_COMPOSE_YML)

def create_structure(project_name: str):
    project_root = Path(project_name).resolve()
    if project_root.exists():
        print(f"[Error] Directory '{project_root}' already exists. Please choose a different project name.")
        sys.exit(1)

    print(f"Creating project folder at {project_root}")
    project_root.mkdir(parents=True, exist_ok=False)

    for folder, subfolders in BASE_STRUCTURE.items():
        folder_path = project_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        for subfolder in subfolders:
            (folder_path / subfolder).mkdir(parents=True, exist_ok=True)

    create_files(project_root, project_name)

    print(f"\n🎉 Project '{project_name}' scaffolded successfully!")
    print(f"Next steps:\n  cd {project_name}\n  # Start building your secure app!\n")
