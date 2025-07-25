import argparse
from pathlib import Path
from .scaffold import create_structure

def main():
    parser = argparse.ArgumentParser(
        description="scaffoldor - CLI tool to scaffold secure fullstack app structures"
    )
    parser.add_argument("project_name", help="Name of the project directory to create")
    parser.add_argument(
        "-p", "--path", default=".", help="Parent directory to create the project in (default: current directory)"
    )
    parser.add_argument(
        "-t", "--template", default="default", help="Project template to use (default: default)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print actions without creating files or directories"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print detailed logs"
    )
    args = parser.parse_args()

    base_path = Path(args.path).resolve()
    project_path = base_path / args.project_name

    create_structure(
        project_path=project_path,
        template_name=args.template,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

if __name__ == "__main__":
    main()
