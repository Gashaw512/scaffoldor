from setuptools import setup, find_packages

setup(
    name="scaffoldor",
    version="0.1.0",
    description="CLI tool to scaffold secure fullstack app structures",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'scaffoldor=scaffoldor.cli:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
