#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='ODB-2 Utils',
    version='1.0',
    description="Tools for interfacing to OBD2 reader",
    url='https://github.com/peter1010/obd2_utils',
    author='Peter1010',
    author_email='peter1010@localnet',
    license='GPL',
    package_dir={'obd2_lib': 'obd2_lib'},
    packages=['obd2_lib'],
    data_files=[
        ('/usr/bin/', ('obd2_reader.sh',))],
)
