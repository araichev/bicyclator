from setuptools import setup, find_packages


# Import ``__version__`` variable
exec(open('mustaching/_version.py').read())

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='bicyclator',
    version='3.0.0',
    author='Alex Raichev',
    author_email='alex@raichev.net',
    packages=['bicyclator', 'tests'],
    url='https://github.com/araichev/bicyclator',
    license=license,
    description='A Python 3.4 bicycle calculator',
    long_description=readme,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[],
)

