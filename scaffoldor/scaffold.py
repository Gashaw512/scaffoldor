import sys
from pathlib import Path
import json

def load_template(template_name: str) -> dict:
    """Load project structure template from JSON file."""
    templates_dir = Path(__file__).parent / "templates"
    template_path = templates_dir / f"{template_name}.json"
    if not template_path.exists():
        print(f"[Error] Template '{template_name}' not found. Available templates: default")
        sys.exit(1)
    with template_path.open() as f:
        return json.load(f)

README_TEMPLATE = """\
# {project_name}

Welcome to the {project_name} project scaffolded by scaffoldor!

## Project Structure

- backend/ - FastAPI backend
- frontend/ - React + Tailwind frontend
- auth/ - Keycloak configs
- infra/ - Docker, deployment configs
- docs/ - Documentation

## Getting Started

1. Navigate to the project folder: `cd {project_name}`
2. Customize your project
3. Build & run your app!

---

## Author

Your Name  
your.email@example.com
"""

ENV_EXAMPLE = """\
# Example environment variables

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

def create_files(project_root: Path, project_name: str, dry_run: bool = False, verbose: bool = False) -> None:
    files_to_create = {
        "README.md": README_TEMPLATE.format(project_name=project_name),
        ".env.example": ENV_EXAMPLE,
        "docker-compose.yml": DOCKER_COMPOSE_YML,
    }
    for filename, content in files_to_create.items():
        file_path = project_root / filename
        if dry_run:
            if verbose:
                print(f"[Dry-run] Would create file: {file_path}")
            continue
        if verbose:
            print(f"Creating file: {file_path}")
        file_path.write_text(content)

    print(f"\n🎉 Project '{project_name}' scaffolded successfully!")
    print(f"Next steps:\n  cd {project_name}\n  # Start building your secure app!\n")

def create_structure(
    project_path: Path,
    template_name: str = "default",
    dry_run: bool = False,
    verbose: bool = False,
) -> None:
    if project_path.exists():
        print(f"[Error] Directory '{project_path}' already exists. Choose a different name or path.")
        sys.exit(1)

    if verbose or dry_run:
        print(f"{'[Dry-run] ' if dry_run else ''}Creating project at {project_path}")

    if dry_run:
        print("[Dry-run] Skipping actual creation.")
        return

    project_path.mkdir(parents=True)

    structure = load_template(template_name)

    for folder, subfolders in structure.items():
        folder_path = project_path / folder
        if verbose:
            print(f"Creating folder: {folder_path}")
        folder_path.mkdir(exist_ok=True)
        for subfolder in subfolders:
            subfolder_path = folder_path / subfolder
            if verbose:
                print(f"Creating subfolder: {subfolder_path}")
            subfolder_path.mkdir(parents=True, exist_ok=True)

    create_files(project_path, project_path.name, dry_run=dry_run, verbose=verbose)

    if verbose:
        print(f"Project '{project_path.name}' scaffolded successfully!\n")
        print(f"Next steps:\n  cd {project_path}\n  # Start building your secure app!\n")


  

