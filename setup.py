from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'ivoy/version.py').load_module()

test_requires = [
    'pytest==5.4.3',
    'pytest-vcr==1.0.2',
    'pycodestyle==2.6.0',
    'pytest-cov==2.10.0',
    'black==19.10b0',
    'isort[pipfile]==4.3.21',
    'flake8==3.8.3',
    'mypy==0.782',
    'iso8601==0.1.12',
]

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='ivoy',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Client library for iVoy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/ivoy-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(ivoy=['py.typed']),
    python_requires='>=3.6',
    install_requires=[
        'requests==2.24.0',
        'iso8601==0.1.12',
        'dataclasses>=0.6;python_version<"3.7"',
    ],
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
