from setuptools import setup
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='weldor',

    # Link: https://www.python.org/dev/peps/pep-0440/#version-scheme
    version='v2.7.2022',

    description='weldor - A reactive AI designed to assist you with Wordle variants',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/ayaanhossain/weldor',

    author='ayaanhossain',

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Games/Entertainment :: Turn Based Strategy',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords=' '.join([
        'reactive',
        'ai',
        'artificial',
        'intelligence',
        'entropy',
        'wordle',
        'trees',
        'sets',
        'wordle-solver',
        'wordle-python',
        'wordle-assistant',
        'wordle-solution',
        'wordle-game',
        'wordle-helper']),

    packages=['weldor', 'weldor.wordbase'],

    package_dir={
        'weldor': './weldor'
    },

    package_data={
        'weldor': ['wordbase/*.txt']
    },

    entry_points={
        'console_scripts': [
            'weldor = weldor:weldor'],
    },

    python_requires=', '.join([
        '!=2.7',
        '!=3.0.*',
        '!=3.1.*',
        '!=3.2.*',
        '!=3.3.*',
        '!=3.4.*',
        '!=3.5.*',
        '>=3.6.*',
        '<4.0.*']),

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ayaanhossain/weldor/issues',
        'Source'     : 'https://github.com/ayaanhossain/weldor/tree/master/weldor',
    },
)