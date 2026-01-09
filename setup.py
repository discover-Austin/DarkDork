#!/usr/bin/env python3
"""
DarkDork - Professional Google Dorking Tool
Setup script for packaging and distribution
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='darkdork',
    version='1.0.0',
    description='Professional Google Dorking Tool for Forensic and Cybersecurity Organizations',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Your Organization',
    author_email='contact@yourorganization.com',
    url='https://github.com/yourusername/darkdork',
    license='Apache License 2.0',

    # Package configuration
    py_modules=['darkdork'],
    python_requires='>=3.7',

    # Dependencies
    install_requires=[
        # tkinter is included with Python
    ],

    # Optional dependencies
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pylint>=2.15.0',
        ],
        'full': [
            'requests>=2.31.0',
            'beautifulsoup4>=4.12.0',
            'selenium>=4.15.0',
        ]
    },

    # Entry points for command-line execution
    entry_points={
        'console_scripts': [
            'darkdork=darkdork:main',
        ],
        'gui_scripts': [
            'darkdork-gui=darkdork:main',
        ]
    },

    # Classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],

    # Keywords
    keywords='security osint google-dork dorking penetration-testing cybersecurity forensics',

    # Package data
    include_package_data=True,

    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/darkdork/issues',
        'Source': 'https://github.com/yourusername/darkdork',
        'Documentation': 'https://github.com/yourusername/darkdork/wiki',
    },
)
