#!/usr/bin/env python3
"""
DarkDork Professional Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read version
version = (this_directory / "VERSION").read_text().strip() if (this_directory / "VERSION").exists() else "1.0.0"

setup(
    name="darkdork-pro",
    version=version,
    author="DarkDork Team",
    author_email="info@darkdork.io",
    description="Professional Google Dorking Tool for Cybersecurity Professionals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/discover-Austin/DarkDork",
    py_modules=[
        "darkdork_pro",
        "darkdork_library",
        "darkdork_db",
        "darkdork_exports",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.6.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "python-dateutil>=2.8.2",
        "reportlab>=4.0.0",
        "python-docx>=1.0.0",
        "openpyxl>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pyinstaller>=5.0.0",
            "pytest>=7.0.0",
        ],
        "full": [
            "shodan>=1.30.0",
            "virustotal-python>=1.0.0",
            "python-nmap>=0.7.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "darkdork=darkdork_pro:main",
        ],
        "gui_scripts": [
            "darkdork-pro=darkdork_pro:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    keywords="security, google dorking, osint, pentesting, reconnaissance",
    project_urls={
        "Bug Reports": "https://github.com/discover-Austin/DarkDork/issues",
        "Source": "https://github.com/discover-Austin/DarkDork",
    },
    include_package_data=True,
    package_data={
        "": [
            "*.json",
            "*.txt",
            "LICENSE",
            "README.md",
        ],
    },
    zip_safe=False,
)
