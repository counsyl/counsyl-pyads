from setuptools import setup, find_packages

exec(open('counsyl_pyads/version.py').read())

setup(
    name='counsyl_pyads',
    version=__version__,
    packages=find_packages(),
    scripts=['bin/twincat_plc_info.py'],
    include_package_data=True,
    zip_safe=False,
    author='automation@counsyl.com',
    author_email='automation@counsyl.com',
    maintainer='automation@counsyl.com',
    maintainer_email='automation@counsyl.com',
    url='https://github.counsyl.com/dev/counsyl_pyads.git',
    description=(
        'A library for directly interacting with a Twincat PLC. Based on '
        'https://github.com/chwiede/pyads.'
    ),
)
