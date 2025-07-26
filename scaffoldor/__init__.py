# scaffoldor/__init__.py
# This should now be the source of truth for the version for setuptools
__version__ = "0.1.0"

# The pkg_resources part becomes less critical for *setting* the version,
# but can still be used for *reading* it at runtime if you prefer.
# For consistency, you might want to remove pkg_resources here if you
# are relying solely on setuptools.dynamic.
# If you do keep it, ensure the version here matches pyproject.toml for initial publish.
# The 'from . import __version__' in cli.py will pick this up.