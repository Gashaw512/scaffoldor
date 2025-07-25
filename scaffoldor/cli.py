import argparse
import sys
from pathlib import Path
from .scaffold import create_structure

VERSION = "0.1.1"  # update this as needed

def main():
    parser = argparse.ArgumentParser(
        description="scaffoldor - CLI tool to scaffold secure fullstack app structures"
    )
    parser.add_argument(
        "project_name", nargs="?", help="Name of the project directory to create"
    )
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
    parser.add_argument(
        "--version", action="store_true", help="Show scaffoldor version and exit"
    )

    args = parser.parse_args()

    if args.version:
        print(f"scaffoldor version {VERSION}")
        sys.exit(0)

    if not args.project_name:
        parser.error("the following arguments are required: project_name")

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
