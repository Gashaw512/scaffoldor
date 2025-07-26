# tests/test_scaffoldor.py
import subprocess
import sys
from pathlib import Path
import pytest
import json
import shutil

# Assuming scaffoldor is installed in editable mode for testing
from scaffoldor.scaffold import create_structure, load_template_config, list_templates_available
from scaffoldor import __version__ as scaffoldor_version

# --- CLI Tests ---

def test_version_flag_global(capsys):
    """Test the global --version flag."""
    result = subprocess.run([sys.executable, "-m", "scaffoldor.cli", "--version"], capture_output=True, text=True, check=True)
    assert f"scaffoldor {scaffoldor_version}" in result.stdout
    assert result.returncode == 0

def test_create_command_no_project_name_error(capsys):
    """Test 'create' command without project name raises an error."""
    result = subprocess.run([sys.executable, "-m", "scaffoldor.cli", "create"], capture_output=True, text=True)
    assert "the following arguments are required: project_name" in result.stderr
    assert result.returncode != 0

def test_list_templates_command(capsys):
    """Test --list-templates command."""
    result = subprocess.run([sys.executable, "-m", "scaffoldor.cli", "list-templates"], capture_output=True, text=True, check=True)
    assert "Available templates:" in result.stdout
    assert "- default" in result.stdout # Ensure default template is listed
    assert result.returncode == 0

def test_init_template_command(tmp_path):
    """Test --init command to create a new template."""
    # Temporarily change the working directory for the test to avoid polluting actual package
    original_cwd = Path.cwd()
    package_path = Path(__file__).parent.parent # Points to the root of the scaffoldor package
    template_dir = package_path / "scaffoldor" / "templates"

    # Create a temporary template directory for this test
    # We need to simulate the package structure for the `init` command to find templates
    tmp_templates_dir = tmp_path / "scaffoldor" / "templates"
    tmp_templates_dir.mkdir(parents=True)
    shutil.copy(template_dir / "default.json", tmp_templates_dir / "default.json")
    (tmp_templates_dir / "content").mkdir()
    shutil.copy(template_dir / "content" / "README.md.jinja", tmp_templates_dir / "content" / "README.md.jinja")
    shutil.copy(template_dir / "content" / ".env.example.jinja", tmp_templates_dir / "content" / ".env.example.jinja")
    shutil.copy(template_dir / "content" / "docker-compose.yml.jinja", tmp_templates_dir / "content" / "docker-compose.yml.jinja")


    new_template_name = "my-new-test-template"
    
    # We need to run the cli from a location where it can find the temporary templates
    # This is a bit tricky for testing `init` as it modifies the source
    # For a robust test, it's better to isolate the scaffoldor package itself
    # or mock parts of `scaffold.py`.
    # For simplicity, we'll run it as if scaffoldor is at `tmp_path`'s root
    # but the init command expects to write into `scaffoldor/templates` relative to itself.

    # Option 1: Mocking Path. The most robust way for init testing.
    # However, this is more complex.

    # Option 2: Run in a temp directory with a symlink/copy of scaffoldor's core logic
    # This example takes a slightly less clean but functional approach
    # by directly calling the main function with modified arguments if possible,
    # or by running `subprocess` from a carefully constructed temp env.

    # For now, let's test the side effects in `tmp_path` by simulating the cli behavior
    # This is not a direct CLI call test for init but a functional one.

    # Instead of subprocess, let's call the `main` function directly and mock sys.argv
    from unittest.mock import patch
    from scaffoldor.cli import main as cli_main

    # Backup original template_dir and content_dir paths
    original_scaffoldor_templates_dir = (Path(__file__).parent.parent / "scaffoldor" / "templates").resolve()
    original_scaffoldor_templates_content_dir = (original_scaffoldor_templates_dir / "content").resolve()

    # Temporarily change scaffoldor's internal paths to point to tmp_path for the test
    with patch('scaffoldor.scaffold.Path', wraps=Path) as mock_path, \
         patch('scaffoldor.cli.Path', wraps=Path) as mock_cli_path:

        # Make sure that any Path(__file__).parent operations resolve to our temporary structure
        # This is a hacky way, mocking sys.modules for scaffoldor is better for isolation
        # but this might work for a quick test.
        # This part is complex because __file__ is hardcoded.
        # A better approach is to mock `Path(__file__).parent` in `scaffold.py` and `cli.py`
        # Or, pass a base_templates_path to the scaffold functions for testing.

        # Given the complexity of mocking __file__ and module imports for subprocess,
        # let's write a functional test for the init process by directly manipulating paths
        # that `scaffoldor.cli.main` would interact with, but outside of subprocess.

        # Setup for direct call to cli.main for `init`
        # Create a mock environment for scaffoldor itself
        mock_scaffoldor_root = tmp_path / "mock_scaffoldor_package"
        (mock_scaffoldor_root / "scaffoldor").mkdir(parents=True)
        (mock_scaffoldor_root / "scaffoldor" / "__init__.py").touch()
        (mock_scaffoldor_root / "scaffoldor" / "cli.py").touch() # Dummy file
        (mock_scaffoldor_root / "scaffoldor" / "scaffold.py").touch() # Dummy file

        # Copy the actual template files to the mock package's template directory
        mock_template_dir = mock_scaffoldor_root / "scaffoldor" / "templates"
        mock_template_dir.mkdir()
        shutil.copy(original_scaffoldor_templates_dir / "default.json", mock_template_dir / "default.json")
        mock_content_dir = mock_template_dir / "content"
        mock_content_dir.mkdir()
        shutil.copy(original_scaffoldor_templates_content_dir / "README.md.jinja", mock_content_dir / "README.md.jinja")
        shutil.copy(original_scaffoldor_templates_content_dir / ".env.example.jinja", mock_content_dir / ".env.example.jinja")
        shutil.copy(original_scaffoldor_templates_content_dir / "docker-compose.yml.jinja", mock_content_dir / "docker-compose.yml.jinja")


        # Now, patch sys.path so that scaffoldor.cli and scaffoldor.scaffold can find these mock templates
        with patch.object(sys, 'argv', ['scaffoldor', 'init', new_template_name]), \
             patch('scaffoldor.cli.Path', wraps=Path) as mock_cli_path_obj, \
             patch('scaffoldor.scaffold.Path', wraps=Path) as mock_scaffold_path_obj:

            # Make the mocked Path objects return paths relative to our temporary scaffoldor root
            # This is still tricky and might be brittle.
            # The most robust way is to make `scaffold.py` and `cli.py` accept a `templates_base_path` argument
            # for testing purposes, or use a testing tool like `cli_test_helpers`.

            # For now, let's directly call `create_template_boilerplate` from `scaffold.py` if it existed,
            # but since `init` logic is in `cli.py`, it's harder.
            # Let's simplify and just check the side effects of running the init.
            # We assume the cli is running from the root of the mock_scaffoldor_package.

            # We need to simulate the `__file__` for scaffoldor/cli.py
            # This is a very deep mock, usually avoided.
            # Simpler approach: Test the *effect* of `init`
            # and verify the files are created where they *should* be if `scaffoldor` was installed.

            # Let's assume `init` creates files in the CWD's `scaffoldor/templates` if run
            # without being installed.
            # This is a functional test for init, not strictly a CLI call.

            # We'll run `init` in `tmp_path` to verify it generates new template files correctly.
            # The `init` command should write to `scaffoldor/templates` relative to `sys.executable -m` path.
            # So, we'll setup `tmp_path` as a fake site-packages and then execute.

            # Temporarily modify sys.path to point to our mock scaffoldor root
            sys.path.insert(0, str(mock_scaffoldor_root))
            
            try:
                # Call the main function directly
                cli_main()
            finally:
                sys.path.pop(0) # Clean up sys.path


    # Verify the new template JSON file exists
    new_template_json_file = mock_template_dir / f"{new_template_name}.json"
    assert new_template_json_file.exists()

    # Verify its content is correct (basic check)
    with new_template_json_file.open() as f:
        config = json.load(f)
        assert config["description"] == f"A custom template for {new_template_name}"
        assert "structure" in config
        assert "content_files" in config
        assert config["content_files"]["README.md"] == f"{new_template_name}_example/README.md.jinja"


    # Verify the new content directory and files exist
    new_template_content_dir = mock_template_dir / "content" / f"{new_template_name}_example"
    assert new_template_content_dir.exists()
    assert (new_template_content_dir / "README.md.jinja").exists()
    assert (new_template_content_dir / ".env.example.jinja").exists()
    assert (new_template_content_dir / "docker-compose.yml.jinja").exists()


# --- Scaffolding Logic Tests ---

def test_create_structure_default(tmp_project_dir: Path):
    """Test default project structure creation."""
    project_name = "test_project_default"
    project_path = tmp_project_dir / project_name

    create_structure(project_path, template_name="default", dry_run=False, verbose=False)

    assert project_path.exists()
    assert (project_path / "backend" / "app" / "api" / "v1").exists()
    assert (project_path / "frontend" / "src" / "components").exists()
    assert (project_path / "auth" / "keycloak-config").exists()
    assert (project_path / "docs").exists()
    assert (project_path / "infra").exists()

    # Verify files created
    readme_path = project_path / "README.md"
    env_example_path = project_path / ".env.example"
    docker_compose_path = project_path / "docker-compose.yml"

    assert readme_path.exists()
    assert env_example_path.exists()
    assert docker_compose_path.exists()

    # Verify content (basic check)
    readme_content = readme_path.read_text()
    assert f"# {project_name}" in readme_content
    assert "Welcome to the" in readme_content

    env_content = env_example_path.read_text()
    assert f"DATABASE_URL=postgresql://user:password@localhost:5432/{project_name.lower()}_db" in env_content

    docker_compose_content = docker_compose_path.read_text()
    assert f"POSTGRES_DB: {project_name.lower()}_db" in docker_compose_content


def test_create_structure_dry_run(tmp_project_dir: Path, capsys):
    """Test dry-run mode, ensuring no files are created."""
    project_name = "test_project_dry_run"
    project_path = tmp_project_dir / project_name

    create_structure(project_path, template_name="default", dry_run=True, verbose=True)

    assert not project_path.exists() # Crucial: nothing should be created
    
    # Check for dry-run messages in output
    captured = capsys.readouterr()
    assert "[Dry-run] Would create project at" in captured.out
    assert "[Dry-run] Skipping actual creation." in captured.out
    assert f"  - {project_name}/backend/" in captured.out
    assert f"  - {project_name}/README.md" in captured.out
    assert "[Dry-run] No files or directories were actually created." in captured.out


def test_create_structure_existing_directory_error(tmp_project_dir: Path, capsys):
    """Test error handling when target directory already exists."""
    project_name = "existing_project"
    project_path = tmp_project_dir / project_name
    project_path.mkdir() # Create an existing directory

    with pytest.raises(SystemExit) as excinfo:
        create_structure(project_path, template_name="default", dry_run=False, verbose=False)

    assert excinfo.value.code == 1 # Expect SystemExit with code 1
    captured = capsys.readouterr()
    assert f"[Error] Directory '{project_path}' already exists." in captured.err # Error logged to stderr


def test_create_structure_invalid_template_error(tmp_project_dir: Path, capsys):
    """Test error handling when an invalid template is specified."""
    project_name = "invalid_template_project"
    project_path = tmp_project_dir / project_name

    with pytest.raises(SystemExit) as excinfo:
        create_structure(project_path, template_name="non_existent_template", dry_run=False, verbose=False)

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Template 'non_existent_template' not found." in captured.err


def test_load_template_config_missing_structure_key(tmp_path: Path, capsys):
    """Test template validation for missing 'structure' key."""
    bad_template_dir = tmp_path / "scaffoldor" / "templates"
    bad_template_dir.mkdir(parents=True)
    bad_json_path = bad_template_dir / "bad_template.json"
    
    # Create a dummy scaffoldor package structure for test to find template
    shutil.copytree(Path(__file__).parent.parent / "scaffoldor", tmp_path / "scaffoldor", dirs_exist_ok=True)
    
    with bad_json_path.open('w') as f:
        json.dump({"description": "Missing structure"}, f)

    # Temporarily modify the internal paths for the test
    # This is a common pattern for testing functions that rely on package-relative paths
    original_templates_dir_path = (Path(__file__).parent.parent / "scaffoldor" / "templates").resolve()
    
    with patch('scaffoldor.scaffold.Path', wraps=Path) as mock_path_obj:
        # Mock the Path(__file__).parent in scaffold.py to point to our temporary scaffoldor root
        # This is a bit advanced, but ensures the `load_template_config` finds our test template
        
        # We need to ensure that when `Path(__file__).parent` is called within `scaffold.py`,
        # it points to our `tmp_path / "scaffoldor"`.
        # This can be done by replacing `scaffoldor` in `sys.modules` with a mock
        # or by making `scaffoldor.scaffold`'s `__file__` point to a temporary location.
        
        # A simpler way for a unit test: directly call load_template_config with modified `__file__` context
        # This is hard. A better way: make `load_template_config` accept a `base_path` for templates.
        
        # For now, let's just make sure the error message is correct, assuming the file is read.
        # This test needs `bad_template.json` to be found as if it's in a template directory.
        # For this to work without major refactoring, `load_template_config` needs to be more flexible.

        # Direct test of load_template_config assuming `bad_template_dir` is the templates base.
        # We simulate the file path being found in the "templates" directory
        
        # First, ensure the actual scaffoldor templates are not interfering
        # We'll need to create a temporary fake package structure for scaffoldor
        temp_scaffoldor_root = tmp_path / "temp_scaffoldor_package"
        (temp_scaffoldor_root / "scaffoldor" / "templates").mkdir(parents=True)
        (temp_scaffoldor_root / "scaffoldor" / "__init__.py").touch()
        (temp_scaffoldor_root / "scaffoldor" / "scaffold.py").touch()
        # Copy the bad template to this fake location
        shutil.copy(bad_json_path, temp_scaffoldor_root / "scaffoldor" / "templates" / "bad_template.json")
        
        # Temporarily add the fake package to sys.path
        sys.path.insert(0, str(temp_scaffoldor_root))
        
        # Import the function after modifying sys.path to ensure it uses the "fake" scaffoldor
        # from scaffoldor.scaffold import load_template_config # Re-import might be needed
        
        try:
            with pytest.raises(SystemExit) as excinfo:
                # Mock Path(__file__).parent in scaffold.py to point to the temporary package
                with patch('scaffoldor.scaffold.Path', wraps=Path) as mock_path_lib:
                    # When Path(__file__).parent is called in scaffold.py, it should return
                    # the path to our temporary `scaffoldor` directory
                    # This mock is for `Path(__file__).parent` specifically
                    mock_path_lib.return_value = temp_scaffoldor_root / "scaffoldor"
                    load_template_config("bad_template")

            assert excinfo.value.code == 1
            captured = capsys.readouterr()
            assert "Invalid template configuration in 'bad_template.json': Template 'bad_template.json' is missing the 'structure' key." in captured.err
        finally:
            sys.path.pop(0) # Clean up sys.path


def test_dynamic_readme_content(tmp_project_dir: Path):
    """Test that project_name is correctly injected into README."""
    project_name = "dynamic-readme-app"
    project_path = tmp_project_dir / project_name

    create_structure(project_path, template_name="default", dry_run=False, verbose=False)

    readme_path = project_path / "README.md"
    assert readme_path.exists()

    content = readme_path.read_text()
    assert f"# {project_name}" in content
    assert f"Welcome to the {project_name} project" in content
    assert f"`cd {project_name}`" in content

def test_dynamic_env_and_docker_compose_content(tmp_project_dir: Path):
    """Test dynamic content for .env.example and docker-compose.yml."""
    project_name = "my-awesome-app"
    project_path = tmp_project_dir / project_name

    create_structure(project_path, template_name="default", dry_run=False, verbose=False)

    env_path = project_path / ".env.example"
    docker_path = project_path / "docker-compose.yml"

    assert env_path.exists()
    assert docker_path.exists()

    env_content = env_path.read_text()
    # Check for lowercased and hyphen-replaced project name
    expected_db_name = project_name.lower().replace('-', '_') + "_db"
    assert f"DATABASE_URL=postgresql://user:password@localhost:5432/{expected_db_name}" in env_content
    assert f"KEYCLOAK_URL=http://localhost:8080/realms/{project_name.lower().replace('-', '_')}" in env_content

    docker_content = docker_path.read_text()
    assert f"POSTGRES_DB: {expected_db_name}" in docker_content
    assert f"KC_DB_URL: jdbc:postgresql://db:5432/{expected_db_name}" in docker_content