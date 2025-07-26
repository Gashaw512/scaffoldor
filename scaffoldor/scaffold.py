# scaffoldor/scaffold.py
import sys
from pathlib import Path
import json
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape, PackageLoader

logger = logging.getLogger("scaffoldor")

def load_template_config(template_name: str) -> dict:
    """Load project structure template from JSON file."""
    # Use PackageLoader to load templates from within the installed package
    template_path = Path(__file__).parent / "templates" / f"{template_name}.json"

    if not template_path.exists():
        logger.error(f"Template '{template_name}' not found at {template_path}.")
        available_templates = list_templates_available()
        if available_templates:
            logger.info(f"Available templates: {', '.join(available_templates)}")
        else:
            logger.info("No templates found. Use 'scaffoldor init <name>' to create one.")
        sys.exit(1)

    try:
        with template_path.open(encoding='utf-8') as f:
            template_config = json.load(f)
        
        # Basic validation for template config
        if "structure" not in template_config:
            raise ValueError(f"Template '{template_name}.json' is missing the 'structure' key.")
        
        return template_config
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing template JSON '{template_name}.json': {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid template configuration in '{template_name}.json': {e}")
        sys.exit(1)


def list_templates_available() -> list[str]:
    """Lists all available project templates."""
    templates_dir = Path(__file__).parent / "templates"
    template_files = [f.stem for f in templates_dir.glob("*.json") if f.is_file()]
    return sorted(template_files)


def create_files(
    project_root: Path,
    project_name: str,
    template_config: dict,
    dry_run: bool = False,
    verbose: bool = False,
) -> None:
    """Creates boilerplate files using Jinja2 templates."""
    
    # Set up Jinja2 environment to load templates from the package's templates/content directory
    # The first argument is the package name, the second is the subdirectory within the package
    env = Environment(
        loader=PackageLoader("scaffoldor", "templates/content"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True, # Remove extra newlines for control structures
        lstrip_blocks=True # Remove leading whitespace from the start of a block
    )

    content_files = template_config.get("content_files", {})
    
    if dry_run and verbose:
        logger.info("[Dry-run] Would create the following files:")

    for output_filename, template_relative_path in content_files.items():
        file_path = project_root / output_filename
        
        # Determine the correct template path for Jinja2 loader
        # If template_relative_path is like "content/README.md.jinja", Jinja2 loader expects "README.md.jinja"
        # because the loader's base is already "scaffoldor/templates/content"
        # However, if template_relative_path is "my_template_example/README.md.jinja"
        # the loader expects "my_template_example/README.md.jinja"
        
        template_name_in_loader = template_relative_path # By default, assume the path as given is relative to the loader's base

        if dry_run:
            if verbose:
                logger.info(f"  - {file_path} (from template: {template_name_in_loader})")
            continue

        try:
            template = env.get_template(template_name_in_loader)
            content = template.render(project_name=project_name)

            if verbose:
                logger.debug(f"Creating file: {file_path}")
            file_path.write_text(content, encoding='utf-8')
        except Exception as e:
            logger.error(f"Error generating file '{output_filename}' from template '{template_name_in_loader}': {e}")
            sys.exit(1)

    if not dry_run:
        logger.info(f"\n🎉 Project '{project_name}' scaffolded successfully!")
        logger.info(f"Next steps:\n  cd {project_name}\n  # Start building your secure app!\n")


def create_structure(
    project_path: Path,
    template_name: str = "default",
    dry_run: bool = False,
    verbose: bool = False,
) -> None:
    """
    Creates the project directory structure and files based on a template.
    """
    if project_path.exists():
        logger.error(f"Directory '{project_path}' already exists. Choose a different name or path.")
        sys.exit(1)

    template_config = load_template_config(template_name)
    structure = template_config.get("structure", {})

    if dry_run:
        logger.info(f"[Dry-run] Would create project at {project_path}")
        logger.info("[Dry-run] Directory structure:")
        for folder, subfolders in structure.items():
            logger.info(f"  - {project_path.name}/{folder}/")
            for subfolder in subfolders:
                logger.info(f"    - {project_path.name}/{folder}/{subfolder}/")
        create_files(project_path, project_path.name, template_config, dry_run=True, verbose=True)
        logger.info("[Dry-run] No files or directories were actually created.")
        return

    logger.info(f"Creating project at {project_path}")
    try:
        project_path.mkdir(parents=True)
        logger.debug(f"Created root project directory: {project_path}")
    except OSError as e:
        logger.error(f"Failed to create project directory '{project_path}': {e}")
        sys.exit(1)

    for folder, subfolders in structure.items():
        folder_path = project_path / folder
        try:
            if verbose:
                logger.debug(f"Creating folder: {folder_path}")
            folder_path.mkdir(exist_ok=True)
            for subfolder in subfolders:
                subfolder_path = folder_path / subfolder
                if verbose:
                    logger.debug(f"Creating subfolder: {subfolder_path}")
                subfolder_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create directory '{folder_path}' or its subfolders: {e}")
            # Attempt to clean up partially created project
            shutil.rmtree(project_path, ignore_errors=True)
            sys.exit(1)

    create_files(project_path, project_path.name, template_config, dry_run=dry_run, verbose=verbose)