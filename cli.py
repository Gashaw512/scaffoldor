import argparse
from .scaffold import create_structure

def main():
    parser = argparse.ArgumentParser(
        description="scaffoldor - CLI tool to scaffold secure fullstack app structures"
    )
    parser.add_argument("project_name", help="Name of the project directory to create")
    args = parser.parse_args()

    create_structure(args.project_name)

if __name__ == "__main__":
    main()
