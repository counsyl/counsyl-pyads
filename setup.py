from setuptools import setup, find_packages

exec(open('counsyl_pyads/version.py').read())

setup(
    name='counsyl-pyads',
    version=__version__,
    packages=find_packages(),
    scripts=['bin/twincat_plc_info.py'],
    include_package_data=True,
    zip_safe=False,
    author='Counsyl Inc.',
    author_email='opensource@counsyl.com',
    description='A library for directly interacting with a Twincat PLC.',
    url='https://github.com/counsyl/counsyl_pyads/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
