from distutils.core import setup

dependencies = []
setup(
    name='bicyclator',
    version='3.0.0',
    author='Alex Raichev',
    author_email='alex@raichev.net',
    packages=['bicyclator', 'tests'],
    url='https://github.com/araichev/bicyclator',
    license='LICENSE',
    description='A Python 3.4 bicycle calculator for calculating quantities such as gain ratio, trail, and spoke length.',
    long_description=open('README.rst').read(),
    install_requires=dependencies,
    )

