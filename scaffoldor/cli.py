import argparse
import sys
from pathlib import Path
import logging
import json
import shutil
import os # <--- ADD THIS LINE

from .scaffold import create_structure, load_template_config, list_templates_available
from . import __version__

logger = logging.getLogger("scaffoldor")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def main():
    parser = argparse.ArgumentParser(
        description="scaffoldor - CLI tool to scaffold secure fullstack app structures."
    )

    # Define global arguments here
    parser.add_argument(
        "--dry-run", action="store_true", help="Print actions without creating files or directories (applies to 'create')."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print detailed logs."
    )
    parser.add_argument(
        "--version", action="version", version=f"scaffoldor {__version__}"
    )

    # Subparsers for different commands
    # Added required=True so that argparse will show an error if no command is given.
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Main scaffolding command
    scaffold_parser = subparsers.add_parser(
        "create",
        help="Create a new project structure.",
        description="Creates a new project directory with a predefined structure and boilerplate files."
    )
    scaffold_parser.add_argument(
        "project_name", help="Name of the project directory to create."
    )
    scaffold_parser.add_argument(
        "-p", "--path", default=".", help="Parent directory to create the project in (default: current directory)."
    )

    # Init template command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new boilerplate template.",
        description="Creates a new template directory and files that you can customize."
    )
    init_parser.add_argument(
        "template_name", help="Name of the new template to initialize."
    )

    # List templates command
    list_parser = subparsers.add_parser(
        "list-templates",
        help="List all available project templates.",
        description="Shows a list of all templates Scaffoldor can use to create new projects."
    )

    args = parser.parse_args()

    # Set verbosity level globally after parsing all args
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Ensure a command was chosen. 'required=True' in add_subparsers handles this for newer argparse versions.
    # if not args.command: # This check is redundant with required=True
    #     parser.print_help()
    #     sys.exit(1)

    if args.command == "create":
        base_path = Path(args.path).resolve()
        project_path = base_path / args.project_name

        create_structure(
            project_path=project_path,
            template_name=getattr(args, 'template', 'default'), # Safely get template, defaults to 'default' if not present for some reason
            dry_run=args.dry_run, # Global dry_run
            verbose=args.verbose, # Global verbose
        )
    elif args.command == "init":
        templates_dir = Path(__file__).parent / "templates"
        new_template_json_path = templates_dir / f"{args.template_name}.json"
        new_template_content_dir = templates_dir / "content" / f"{args.template_name}_example"

        if new_template_json_path.exists():
            logger.error(f"Template '{args.template_name}' already exists at {new_template_json_path}. Choose a different name.")
            sys.exit(1)

        logger.info(f"Initializing new template '{args.template_name}'...")

        try:
            default_template_path = templates_dir / "default.json"
            if not default_template_path.exists():
                 logger.critical(f"Default template not found at {default_template_path}. Cannot initialize new template.")
                 sys.exit(1)

            with default_template_path.open('r', encoding='utf-8') as f: # Added encoding
                default_config = json.load(f)

            new_content_files = {}
            default_content_base = templates_dir / "content"

            for filename, relative_path_in_default_content in default_config.get("content_files", {}).items():
                # Correctly map the new template's content files
                # Extract the base filename and the directory structure under templates/content/
                # e.g., "backend/requirements.txt.jinja" -> Path("backend/requirements.txt.jinja")
                # .relative_to(Path("")) will not change it if it's already relative
                # Then prepend the new template's content directory name
                new_content_files[filename] = str(Path(new_template_content_dir.name) / Path(relative_path_in_default_content))


            new_config = {
                "name": f"{args.template_name}-template", # Provide a default name
                "description": f"A custom template for {args.template_name}",
                "author": default_config.get("author", "Your Name"),
                "version": "0.1.0",
                "license": default_config.get("license", "MIT"),
                "keywords": default_config.get("keywords", []) + [args.template_name],

                "structure": default_config.get("structure", {}),
                "content_files": new_content_files,
                "dependencies": default_config.get("dependencies", {}),
                "dev_dependencies": default_config.get("dev_dependencies", {}),
                "scripts": default_config.get("scripts", {}),
                "post_creation_messages": [
                    "",
                    f"🎉 New template '{args.template_name}' initialized successfully!",
                    "",
                    f"You can now customize the structure in '{new_template_json_path.name}'",
                    f"and add/modify content files in the '{new_template_content_dir.name}' directory.",
                    "",
                    "Remember to re-install your 'scaffoldor' package (e.g., `pip install -e .`)",
                    "to make your new template available for use."
                ]
            }

            with new_template_json_path.open('w', encoding='utf-8') as f: # Added encoding
                json.dump(new_config, f, indent=2)
            logger.info(f"Created template configuration: {new_template_json_path}")

            new_template_content_dir.mkdir(parents=True, exist_ok=True)
            
            default_content_dir = templates_dir / "content"

            # Use shutil.copytree for a simpler and more robust copy of the entire content directory
            # It handles subdirectories automatically
            # However, we only want .jinja files. os.walk is still better for filtering.
            
            # If the target directory already exists and is not empty, shutil.copytree will fail.
            # We already created it with mkdir(exist_ok=True)
            # So, we need to iterate with os.walk and copy file by file.

            for root, dirs, files in os.walk(default_content_dir):
                # Calculate the relative path from default_content_dir
                relative_path = Path(root).relative_to(default_content_dir)
                target_dir = new_template_content_dir / relative_path
                target_dir.mkdir(parents=True, exist_ok=True) # Ensure target subdirectories exist

                for file in files:
                    if file.endswith(".jinja"): # Only copy Jinja templates
                        src_file = Path(root) / file
                        dst_file = target_dir / file
                        shutil.copy(src_file, dst_file)
                        logger.info(f"Copied example content file: {dst_file}")

            # Consolidated and moved post_creation_messages into new_config
            # logger.info(f"\n🎉 Template '{args.template_name}' initialized successfully!")
            # logger.info(f"You can now customize the structure in '{new_template_json_path}' and content in '{new_template_content_dir}'")
            # logger.info("Remember to re-install the package (e.g., `pip install -e .`) if you modify templates locally for development mode.")
            
            # Print the post_creation_messages defined in the new_config
            for msg in new_config["post_creation_messages"]:
                logger.info(msg)


        except Exception as e:
            logger.error(f"Failed to initialize template '{args.template_name}': {e}")
            # Clean up partially created template files if an error occurs
            if new_template_json_path.exists():
                new_template_json_path.unlink()
            if new_template_content_dir.exists():
                shutil.rmtree(new_template_content_dir)
            sys.exit(1)

    elif args.command == "list-templates":
        templates = list_templates_available()
        if templates:
            logger.info("\nAvailable templates:")
            for tpl in templates:
                logger.info(f"- {tpl}")
        else:
            logger.info("No templates found.")