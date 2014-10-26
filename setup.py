from distutils.core import setup

exec(open('aeon/version.py').read())  # provides __version__ below

setup(
    name='Aeon',
    url='https://github.com/sMAshdot/aeon',
    author='Marc-Antonio Bisotti',
    author_email='mail@marc-antonio.de',
    version=__version__,
    packages=['aeon', ],
    keywords=['profiling', 'timings', 'benchmark'],
    license='The MIT License (MIT)',
    description=('Runtime and number of calls for designated functions, '
                 'methods, or pieces of code. Optionally output nice report.'),
    long_description=open('README.txt').read(),
    data_files = [("", ["LICENSE", "AUTHORS"])],
)
