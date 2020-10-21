from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # $ pip install cosilico
    name='cosilico',
    version='0.0.1',
    description='A plotting library for visualizing research data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cosilico/cosilico',
    author='Cosilico',
    author_email='epstorrs@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='plotting library research biology physics',  # Optional
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'altair>=4.1.0',
        'anndata>=0.7.4',
        'pandas>=1.0.0',
        'seaborn>=0.10.0',
        'scipy>=1.4.1',
        'matplotlib>=3.2.1',
        ],
    include_package_data = True,
    package_data = {'cosilico': ['datasets/data/*']},

#    entry_points={ 
#        'console_scripts': [
#            'pollock=pollock.pollock:main',
##             'pollock-setup=pollock.pollock_setup:main',
#        ],
#   },
)
