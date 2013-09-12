#!/usr/bin/env python

from setuptools import setup, find_packages

fr8_manpages=[
    'man/fr/man8/isdhcp.8.gz'
]

fr3_manpages=[
    'man/fr/man3/isdhcplib.3.gz',
    'man/fr/man3/isdhcplib.DhcpBasicPacket.3.gz',
    'man/fr/man3/isdhcplib.DhcpPacket.3.gz',
    'man/fr/man3/isdhcplib.hwmac.3.gz',
    'man/fr/man3/isdhcplib.ipv4.3.gz',
    'man/fr/man3/isdhcplib.strlist.3.gz'
]

en3_manpages=[
    'man/man3/isdhcplib.strlist.3.gz',
    'man/man3/isdhcplib.3.gz',
    'man/man3/isdhcplib.ipv4.3.gz'
]

en8_manpages=[
    'man/man8/isdhcp.8.gz'
]

packages = [
    'isdhcplib',
]

setup(
    name='isdhcplib',
    version="1.0.1",
    license='GPL v3',
    description='Dhcp client/server library',
    author='Alexander Ignatyev / based on pydhcplib by Mathieu Ignacio',
    author_email='ialx84@ya.ru',
    url='https://github.com/ialx/isdhcplib',
    packages=find_packages(),
    scripts=['scripts/isdhcp'],
    test_suite='tests.alltests',
    data_files=[
        ("share/man/man8",en8_manpages),
        #            ("share/man/fr/man8",fr8_manpages),
        ("share/man/fr/man3",fr3_manpages),
        ("share/man/man3",en3_manpages)
    ]
)
