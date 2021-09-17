from setuptools import find_packages
from setuptools import setup

setup(
    name='pre-commit-hooks-safety',
    description='A pre-commit hook to check your Python dependencies against safety-db',
    url='https://github.com/Lucas-C/pre-commit-hooks-safety',
    version='1.2.2',
    author='Lucas Cimon',
    author_email='lucas.cimon@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages('.'),
    install_requires=[
        'safety',
    ],
    entry_points={
        'console_scripts': [
            'safety_check = pre_commit_hooks.safety_check:main',
        ],
    },
)
