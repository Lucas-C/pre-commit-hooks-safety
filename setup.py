from setuptools import find_packages
from setuptools import setup

setup(
    name='pre-commit-hooks-safety',
    description='A pre-commit hook to check your Python dependencies against safety-db',
    url='https://github.com/Lucas-C/pre-commit-hooks-safety',
    version='1.4.2',
    author='Lucas Cimon',
    author_email='lucas.cimon@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages('.'),
    install_requires=[
        'safety<=2.3.5',
    ],
    entry_points={
        'console_scripts': [
            'safety_check = pre_commit_hooks.safety_check:main',
        ],
    },
)
