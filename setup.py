from distutils.core import setup

dependencies = []
setup(
    name='bicycle_calculator',
    version='2.1.0',
    author='Alex Raichev',
    author_email='alex@raichev.net',
    packages=['bicycle_calculator', 'tests'],
    url='https://github.com/araichev/bicycle_calculator',
    license='LICENSE',
    description='A Python 3.4 program for calculating various bicycle-related quantities, such as gain ratios, trail, and spoke length.',
    long_description=open('README.rst').read(),
    install_requires=dependencies,
    )

