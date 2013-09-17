from distutils.core import setup

setup(
    name='Aeon',
    url='https://github.com/sMAshdot/aeon',
    author='Marc-Antonio Bisotti',
    author_email='mail@marc-antonio.de',
    version='1.0.2',
    packages=['aeon', ],
    license='The MIT License (MIT)',
    description=('Runtime and number of calls for designated functions, '
                 'methods, or pieces of code. Optionally output nice report.'),
    long_description=open('README.txt').read(),
)
