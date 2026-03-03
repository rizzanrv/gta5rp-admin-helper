"""Setup script for GTA5RP Admin Tool."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="gta5rp-admin-tool",
    version="1.0.0",
    author="rizzanrv",
    author_email="",
    description="Desktop application for GTA5RP server administrators to track reports using OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rizzanrv/gta5rp-admin-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "PyQt6>=6.6.0",
        "pynput>=1.7.6",
        "requests>=2.31.0",
        "Pillow>=10.0.0",
        "aiosqlite>=0.19.0",
        "python-dotenv>=1.0.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "gta5rp-admin-tool=main:main",
        ],
    },
)
